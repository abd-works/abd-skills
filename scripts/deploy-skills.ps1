<#
.SYNOPSIS
  Deploy all skills and agents in this repo to Cursor or VS Code.

.DESCRIPTION
  Scans <repo>/skills/ for folders containing SKILL.md.
  Scans <repo>/agents/ for folders containing AGENT.md or AGENTS.md.

  Repo root is always derived from the script location (parent of scripts/), not cwd.

  Cursor mode:
    Flat junction per skill  → <repo>/.cursor/skills/<skill-name>
    Flat junction per agent  → <repo>/.cursor/agents/<agent-name>
    guidance/*.mdc          → <repo>/.cursor/rules/           (hard link)
    guidance/*.prompt.md    → <repo>/.cursor/commands/        (hard link)

  VSCode mode:
    Flat junction per skill  → %APPDATA%\Code\User\skills\<skill-name>
    Flat junction per agent  → %APPDATA%\Code\User\agents\<agent-name>
    guidance/*.instructions.md → %APPDATA%\Code\User\instructions\ (hard link)
                               → <repo>/.github/               (hard link)
    guidance/*.prompt.md    → %APPDATA%\Code\User\prompts\    (hard link)
                             → <repo>/.github/prompts/         (hard link)

  guidance/ is preferred; falls back to the skill/agent root for legacy layouts.

.PARAMETER IDE
  Target IDE: cursor or vscode. Default: vscode.

.PARAMETER Force
  Remove existing junctions and hard links before creating new ones.
#>
param(
    [ValidateSet("cursor", "vscode")]
    [string] $ide = "vscode",

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

# Repo root = parent of scripts/
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..') | Select-Object -ExpandProperty Path

# Walk up from StartPath to find the highest ancestor that has a .cursor\ folder.
# If none is found above the repo, creates .cursor\ one level above the repo (unless
# that level is a drive root), then returns that parent. Falls back to USERPROFILE.
function Find-HighestCursorRoot {
    param([string]$StartPath)
    $highest = $null
    $dir = [System.IO.DirectoryInfo]::new($StartPath)
    while ($dir -ne $null) {
        if (Test-Path -LiteralPath (Join-Path $dir.FullName '.cursor') -PathType Container) {
            $highest = $dir.FullName
        }
        $dir = $dir.Parent
    }
    if ($highest) { return $highest }

    # Bootstrap: create .cursor one level above the repo if that level isn't a drive root
    $parent = Split-Path $StartPath -Parent
    if ($parent -and ($parent -notmatch '^[A-Za-z]:\\?$')) {
        New-Item -ItemType Directory -Path (Join-Path $parent '.cursor\rules')    -Force | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $parent '.cursor\commands') -Force | Out-Null
        Write-Host "  Bootstrapped: $parent\.cursor" -ForegroundColor DarkCyan
        return $parent
    }
    return $env:USERPROFILE
}

$CursorRoot = Find-HighestCursorRoot -StartPath $RepoRoot

Write-Host "`nRepo root   : $RepoRoot"   -ForegroundColor Cyan
Write-Host "Cursor root : $CursorRoot"  -ForegroundColor Cyan
Write-Host "IDE         : $ide`n"       -ForegroundColor Cyan

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
        $userInstr   = Join-Path $env:APPDATA 'Code\User\instructions'
        $userPrompts = Join-Path $env:APPDATA 'Code\User\prompts'

        # .instructions.md → user scope + <cursor-root>/.github/
        Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $userInstr   $_.Name)                        -Target $_.FullName -IsFile
                New-LinkSafe -Path (Join-Path $CursorRoot  ".github\$($_.Name)")           -Target $_.FullName -IsFile
            }

        # .prompt.md → user scope + <cursor-root>/.github/prompts/
        Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $userPrompts  $_.Name)                       -Target $_.FullName -IsFile
                New-LinkSafe -Path (Join-Path $CursorRoot   ".github\prompts\$($_.Name)")  -Target $_.FullName -IsFile
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
        Join-Path $env:APPDATA 'Code\User\skills'
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
        Join-Path $env:APPDATA 'Code\User\agents'
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
