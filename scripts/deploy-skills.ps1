<#
.SYNOPSIS
  Deploy all skills and agents in this repo to Cursor or VS Code.

.DESCRIPTION
  Scans <repo>/skills/ for folders containing SKILL.md.
  Scans <repo>/agents/ for folders containing AGENT.md or AGENTS.md.

  Repo root is always derived from the script location (parent of scripts/), not cwd.

  Deploy root logic (when -DeployRoot is omitted), aligned with guidance/workspace
  (guidance/workspace/README.md):
    1. Read $RepoRoot/skill-config.json -> workspace.active_skill_workspace when set and path exists.
    2. Else walk upward from $PWD for the nearest *.code-workspace folder (workspace-level deploy).
    3. Else deploy at $RepoRoot (skills repo).

  To pin engagement/deploy targets without overrides: maintain skill-config.json via guidance/workspace/scripts.

  Cursor mode:
    Flat junction per skill  → <deploy-root>/.cursor/skills/<skill-name>
    Flat junction per agent  → <deploy-root>/.cursor/agents/<agent-name>
    guidance/*.mdc           → <deploy-root>/.cursor/rules/           (hard link)
    guidance/*.prompt.md     → <deploy-root>/.cursor/commands/        (hard link)

  VSCode mode:
    Flat junction per skill  → <deploy-root>/.github/skills/<skill-name>
    Flat junction per agent  → <deploy-root>/.github/agents/<agent-name>
    guidance/*.instructions.md → <deploy-root>/.github/          (hard link)
    guidance/*.prompt.md       → <deploy-root>/.github/prompts/  (hard link)

  guidance/ is preferred; falls back to the skill/agent root for legacy layouts.

.PARAMETER IDE
  Target IDE: cursor or vscode. Default: cursor.

.PARAMETER Force
  Remove existing junctions and hard links before creating new ones.
#>
param(
    [ValidateSet("cursor", "vscode")]
    [string] $ide = "cursor",

    # Override the deploy root (where .cursor/ or .github/ is written).
    # When omitted: skill-config.json workspace.active_skill_workspace -> *.code-workspace walk -> repo root.
    [string] $DeployRoot = "",

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

# Repo root = parent of scripts/
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..') | Select-Object -ExpandProperty Path

# Find the deploy root:
#   1. Walk up from StartPath looking for a *.code-workspace file.
#      If found → that directory is the root (workspace-level deploy).
#   2. Otherwise → StartPath itself is the root (single-repo deploy).
function Find-DeployRoot {
    param(
        # Directory to start walking upward from (normally the shell's current directory).
        [string]$StartPath,
        # When no *.code-workspace exists in any ancestor, deploy into the skills repo itself.
        [string]$FallbackRepoRoot
    )
    $dir = [System.IO.DirectoryInfo]::new($StartPath)
    while ($null -ne $dir) {
        $wsFiles = Get-ChildItem -Path $dir.FullName -Filter '*.code-workspace' -File -ErrorAction SilentlyContinue
        if ($wsFiles) {
            return $dir.FullName
        }
        $dir = $dir.Parent
    }
    return $FallbackRepoRoot
}

function Get-DeployRootFromSkillConfig {
    param([string]$RepoRoot)
    $cfgPath = Join-Path $RepoRoot 'skill-config.json'
    if (-not (Test-Path -LiteralPath $cfgPath -PathType Leaf)) {
        return $null
    }
    try {
        $j = Get-Content -LiteralPath $cfgPath -Raw | ConvertFrom-Json
        $ws = $null
        if ($null -ne $j.workspace) {
            $ws = $j.workspace.active_skill_workspace
        }
        if ([string]::IsNullOrWhiteSpace([string]$ws)) {
            return $null
        }
        if (-not (Test-Path -LiteralPath $ws -PathType Container)) {
            Write-Warning "skill-config.json workspace.active_skill_workspace not found on disk: $ws"
            return $null
        }
        return (Resolve-Path -LiteralPath $ws).Path
    }
    catch {
        Write-Warning "Could not read workspace from skill-config.json: $($_.Exception.Message)"
        return $null
    }
}

# Repo root = agilebydesign-skills (parent of scripts/). Deploy destination follows guidance/workspace (skill-config) first.
$CursorRoot = if ($DeployRoot) {
    $DeployRoot
}
elseif (($cfgRoot = Get-DeployRootFromSkillConfig $RepoRoot)) {
    $cfgRoot
}
else {
    Find-DeployRoot -StartPath ((Get-Location).Path) -FallbackRepoRoot $RepoRoot
}

Write-Host "`nRepo root   : $RepoRoot"   -ForegroundColor Cyan
Write-Host "Deploy root : $CursorRoot"  -ForegroundColor Cyan
Write-Host "IDE         : $ide`n"       -ForegroundColor Cyan

# --- Ensure workspace directories exist ---
$deployFolder = if ($ide -eq "cursor") { '.cursor' } else { '.github' }
$subDirs = if ($ide -eq "cursor") {
    @('.cursor\skills', '.cursor\agents', '.cursor\rules', '.cursor\commands')
} else {
    @('.github\skills', '.github\agents', '.github\prompts')
}
foreach ($sub in $subDirs) {
    $dir = Join-Path $CursorRoot $sub
    if (-not (Test-Path -LiteralPath $dir -PathType Container)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor DarkCyan
    }
}

# --- Add deploy folder to .code-workspace if present and not already listed ---
$workspaceFile = Get-ChildItem -Path $CursorRoot -Filter '*.code-workspace' -File -ErrorAction SilentlyContinue | Select-Object -First 1
if ($workspaceFile) {
    $ws = Get-Content $workspaceFile.FullName -Raw | ConvertFrom-Json
    $alreadyPresent = $ws.folders | Where-Object { $_.path -eq $deployFolder }
    if (-not $alreadyPresent) {
        $newEntry = [pscustomobject]@{ path = $deployFolder }
        $ws.folders = @($newEntry) + $ws.folders
        $ws | ConvertTo-Json -Depth 10 | Set-Content $workspaceFile.FullName -Encoding UTF8
        Write-Host "  Added '$deployFolder' to $($workspaceFile.Name)" -ForegroundColor DarkCyan
    }
}

# --- Discover folders ---
# A deployable folder has SKILL.md/AGENT.md/AGENTS.md OR an guidance/ subdirectory.
function Find-MarkedFolders {
    param([string]$Root, [string[]]$Markers)
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) { return @() }
    $results = @()
    # By marker file (SKILL.md, AGENT.md, AGENTS.md)
    foreach ($marker in $Markers) {
        Get-ChildItem -Path $Root -Recurse -Filter $marker -File -ErrorAction SilentlyContinue |
            ForEach-Object { $results += $_.DirectoryName }
    }
    # By guidance/ subdirectory (skills with IDE outputs but no SKILL.md)
    Get-ChildItem -Path $Root -Recurse -Filter 'guidance' -Directory -ErrorAction SilentlyContinue |
        ForEach-Object { $results += $_.Parent.FullName }

    # By direct .mdc presence (guidance folders with ide-files at root, no subfolder)
    # Exclude paths ending in 'guidance' — those are already captured by the guidance/ scan above
    Get-ChildItem -Path $Root -Recurse -Filter '*.mdc' -File -ErrorAction SilentlyContinue |
        Where-Object { (Split-Path $_.DirectoryName -Leaf) -ne 'guidance' } |
        ForEach-Object { $results += $_.DirectoryName }

    # By direct .prompt.md presence (command-only guidance folders with no .mdc)
    Get-ChildItem -Path $Root -Recurse -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue |
        Where-Object { (Split-Path $_.DirectoryName -Leaf) -ne 'guidance' } |
        ForEach-Object { $results += $_.DirectoryName }

    $results | Sort-Object -Unique
}

$skillsRoot   = Join-Path $RepoRoot 'skills'
$agentsRoot   = Join-Path $RepoRoot 'agents'
$guidanceRoot = Join-Path $RepoRoot 'guidance'

$skillFolders   = Find-MarkedFolders -Root $skillsRoot   -Markers @('SKILL.md')
$agentFolders   = Find-MarkedFolders -Root $agentsRoot   -Markers @('AGENT.md', 'AGENTS.md')
$guidanceFolders = Find-MarkedFolders -Root $guidanceRoot -Markers @()

Write-Host "Skills   : $($skillFolders.Count)"   -ForegroundColor Cyan
Write-Host "Agents   : $($agentFolders.Count)"   -ForegroundColor Cyan
Write-Host "Guidance : $($guidanceFolders.Count)`n" -ForegroundColor Cyan

# --- Helpers ---
function Get-IdePayloadRoot {
    param([string]$Root)
    $ideDir = Join-Path $Root 'guidance'
    if (Test-Path -LiteralPath $ideDir -PathType Container) { return $ideDir }
    return $Root
}

function New-LinkSafe {
    param([string]$Path, [string]$Target, [switch]$IsFile)

    if (Test-Path -LiteralPath $Path) {
        if (-not $Force) {
            Write-Host "  SKIP (exists): $Path  -- use -Force to replace" -ForegroundColor Yellow
            return
        }
        Remove-Item -LiteralPath $Path -Recurse -Force
    }

    $parent = Split-Path $Path -Parent
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if ($IsFile) {
        New-Item -ItemType HardLink -Path $Path -Target $Target | Out-Null
    } else {
        New-Item -ItemType Junction  -Path $Path -Target $Target | Out-Null
    }
    Write-Host "  OK : $Path" -ForegroundColor Green
}

# --- Deploy one folder (skill or agent) ---
function Deploy-Folder {
    param(
        [string] $Folder,       # source: folder containing SKILL.md or AGENT.md
        [string] $JunctionRoot  # flat junction destination root
    )

    $name       = (Split-Path $Folder -Leaf) -replace '_', '-'
    $idePayload = Get-IdePayloadRoot -Root $Folder

    Write-Host "[$name]" -ForegroundColor White

    # Flat junction — skipped for guidance folders (no junction root)
    if ($JunctionRoot) {
        New-LinkSafe -Path (Join-Path $JunctionRoot $name) -Target $Folder
    }

    if ($ide -eq "cursor") {
        # .mdc → <cursor-root>/.cursor/rules/
        Get-ChildItem -Path $idePayload -Filter '*.mdc' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".cursor\rules\$($_.Name)") `
                             -Target $_.FullName -IsFile
            }

        # .prompt.md → <cursor-root>/.cursor/commands/
        Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".cursor\commands\$($_.Name)") `
                             -Target $_.FullName -IsFile
            }
    }

    if ($ide -eq "vscode") {
        # .instructions.md → <cursor-root>/.github/
        Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".github\$($_.Name)") -Target $_.FullName -IsFile
            }

        # .prompt.md → <cursor-root>/.github/prompts/
        Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".github\prompts\$($_.Name)") -Target $_.FullName -IsFile
            }
    }

    # scripts/.vscode/tasks.json → <cursor-root>/.vscode/tasks.json (shared, not per-repo)
    $skillTasksJson = Join-Path $Folder 'scripts\.vscode\tasks.json'
    if (Test-Path -LiteralPath $skillTasksJson -PathType Leaf) {
        New-LinkSafe -Path (Join-Path $CursorRoot '.vscode\tasks.json') `
                     -Target $skillTasksJson -IsFile

        # Enable automatic tasks so the watcher starts on folderOpen without a prompt
        $settingsPath = Join-Path $CursorRoot '.vscode\settings.json'
        $settingsDir  = Split-Path $settingsPath -Parent
        if (-not (Test-Path -LiteralPath $settingsDir)) {
            New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
        }
        $rawJson = if (Test-Path -LiteralPath $settingsPath) {
            Get-Content $settingsPath -Raw
        } else { '{}' }
        $obj = $rawJson | ConvertFrom-Json
        if ($obj.'task.allowAutomaticTasks' -ne 'on') {
            $obj | Add-Member -NotePropertyName 'task.allowAutomaticTasks' -NotePropertyValue 'on' -Force
            $obj | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8
            Write-Host "  OK : task.allowAutomaticTasks=on -> $settingsPath" -ForegroundColor Green
        }
    }
}

# --- Skills ---
if ($skillFolders.Count -gt 0) {
    Write-Host "=== Skills ===" -ForegroundColor Magenta

    $junctionRoot = if ($ide -eq "cursor") {
        Join-Path $CursorRoot '.cursor\skills'
    } else {
        Join-Path $CursorRoot '.github\skills'
    }

    foreach ($folder in $skillFolders) {
        Deploy-Folder -Folder $folder -JunctionRoot $junctionRoot
    }
}

# --- Agents ---
if ($agentFolders.Count -gt 0) {
    Write-Host "`n=== Agents ===" -ForegroundColor Magenta

    $junctionRoot = if ($ide -eq "cursor") {
        Join-Path $CursorRoot '.cursor\agents'
    } else {
        Join-Path $CursorRoot '.github\agents'
    }

    foreach ($folder in $agentFolders) {
        Deploy-Folder -Folder $folder -JunctionRoot $junctionRoot
    }
}

# --- Guidance (no junctions — ide-files only) ---
if ($guidanceFolders.Count -gt 0) {
    Write-Host "`n=== Guidance ===" -ForegroundColor Magenta

    foreach ($folder in $guidanceFolders) {
        Deploy-Folder -Folder $folder -JunctionRoot ""
    }
}

Write-Host "`nDone." -ForegroundColor Cyan
