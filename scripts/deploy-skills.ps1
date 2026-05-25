<#
.SYNOPSIS
  Deploy capability family packages and remaining skills/agents to Cursor or VS Code.

.DESCRIPTION
  **Family packages** (repo root — canonical source, copied into the engagement):

    delivery/
    story-driven-delivery/
    domain-driven-design/
    architecture-centric-engineering/
    user-experience-design/
    context-to-memory/
    idea-shaping/
    skill-builder/
    skill-helpers/
    utilities/

  Each package may contain agents/, skills/, content/, lib/, instructions/, prompts/.
  Deployed via ``scripts/deploy_family_package.py`` (copy/merge into .cursor/ or .github/).
  Infra rules and slash commands deploy with the **skill-helpers** family package
  (``skill-helpers/instructions/``, ``skill-helpers/prompts/``).

  Deploy root (when -DeployRoot omitted): skill-config.json → *.code-workspace walk → repo root.
#>
param(
    [ValidateSet("cursor", "vscode")]
    [string] $ide = "cursor",

    [string] $DeployRoot = "",

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..') | Select-Object -ExpandProperty Path

$FamilyPackages = @(
    'delivery',
    'story-driven-delivery',
    'domain-driven-design',
    'architecture-centric-engineering',
    'user-experience-design',
    'context-to-memory',
    'idea-shaping',
    'skill-builder',
    'skill-helpers',
    'utilities'
)

function Find-DeployRoot {
    param(
        [string]$StartPath,
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

$deployFolder = if ($ide -eq "cursor") { '.cursor' } else { '.github' }
$subDirs = if ($ide -eq "cursor") {
    @('.cursor\skills', '.cursor\agents', '.cursor\rules', '.cursor\commands', '.cursor\content', '.cursor\lib')
} else {
    @('.github\skills', '.github\agents', '.github\instructions', '.github\prompts', '.github\content', '.github\lib')
}
foreach ($sub in $subDirs) {
    $dir = Join-Path $CursorRoot $sub
    if (-not (Test-Path -LiteralPath $dir -PathType Container)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor DarkCyan
    }
}

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

# --- Family packages (copy/merge) ---
Write-Host "=== Family packages ===" -ForegroundColor Magenta
$deployPy = Join-Path $RepoRoot 'scripts\deploy_family_package.py'
if (-not (Test-Path -LiteralPath $deployPy)) {
    throw "Missing $deployPy"
}
$ideArg = if ($ide -eq 'vscode') { 'vscode' } else { 'cursor' }
& python $deployPy --to $CursorRoot --package all --ide $ideArg
if ($LASTEXITCODE -ne 0) {
    throw "deploy_family_package.py failed with exit code $LASTEXITCODE"
}

function Find-MarkedFolders {
    param([string]$Root, [string[]]$Markers)
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) { return @() }
    $results = @()
    foreach ($marker in $Markers) {
        Get-ChildItem -Path $Root -Recurse -Filter $marker -File -ErrorAction SilentlyContinue |
            ForEach-Object { $results += $_.DirectoryName }
    }
    Get-ChildItem -Path $Root -Recurse -Filter 'guidance' -Directory -ErrorAction SilentlyContinue |
        ForEach-Object { $results += $_.Parent.FullName }
    Get-ChildItem -Path $Root -Recurse -Filter '*.mdc' -File -ErrorAction SilentlyContinue |
        Where-Object { (Split-Path $_.DirectoryName -Leaf) -ne 'guidance' } |
        ForEach-Object { $results += $_.DirectoryName }
    Get-ChildItem -Path $Root -Recurse -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue |
        Where-Object { (Split-Path $_.DirectoryName -Leaf) -ne 'guidance' } |
        ForEach-Object { $results += $_.DirectoryName }
    $results | Sort-Object -Unique
}

function Get-IdePayloadRoot {
    param([string]$Root)
    $ideDir = Join-Path $Root 'guidance'
    if (Test-Path -LiteralPath $ideDir -PathType Container) { return $ideDir }
    $ideFiles = Join-Path $Root 'ide-files'
    if (Test-Path -LiteralPath $ideFiles -PathType Container) { return $ideFiles }
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

function Deploy-Folder {
    param(
        [string] $Folder,
        [string] $JunctionRoot
    )

    $name       = (Split-Path $Folder -Leaf) -replace '_', '-'
    $idePayload = Get-IdePayloadRoot -Root $Folder

    Write-Host "[$name]" -ForegroundColor White

    if ($JunctionRoot) {
        New-LinkSafe -Path (Join-Path $JunctionRoot $name) -Target $Folder
    }

    if ($ide -eq "cursor") {
        Get-ChildItem -Path $idePayload -Filter '*.mdc' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".cursor\rules\$($_.Name)") `
                             -Target $_.FullName -IsFile
            }
        Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".cursor\commands\$($_.Name)") `
                             -Target $_.FullName -IsFile
            }
    }

    if ($ide -eq "vscode") {
        Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".github\$($_.Name)") -Target $_.FullName -IsFile
            }
        Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue |
            ForEach-Object {
                New-LinkSafe -Path (Join-Path $CursorRoot ".github\prompts\$($_.Name)") -Target $_.FullName -IsFile
            }
    }

    $skillTasksJson = Join-Path $Folder 'scripts\.vscode\tasks.json'
    if (Test-Path -LiteralPath $skillTasksJson -PathType Leaf) {
        New-LinkSafe -Path (Join-Path $CursorRoot '.vscode\tasks.json') `
                     -Target $skillTasksJson -IsFile
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

# --- Standalone skills (skills/ — junction) ---
$skillsRoot = Join-Path $RepoRoot 'skills'
$skillFolders = Find-MarkedFolders -Root $skillsRoot -Markers @('SKILL.md')

if ($skillFolders.Count -gt 0) {
    Write-Host "`n=== Standalone skills (skills/) ===" -ForegroundColor Magenta
    $junctionRoot = if ($ide -eq "cursor") {
        Join-Path $CursorRoot '.cursor\skills'
    } else {
        Join-Path $CursorRoot '.github\skills'
    }
    foreach ($folder in $skillFolders) {
        Deploy-Folder -Folder $folder -JunctionRoot $junctionRoot
    }
}

# --- Legacy agents/ at repo root (junction) ---
$agentsRoot = Join-Path $RepoRoot 'agents'
$agentFolders = Find-MarkedFolders -Root $agentsRoot -Markers @('AGENT.md', 'AGENTS.md')
if ($agentFolders.Count -gt 0) {
    Write-Host "`n=== Agents (agents/) ===" -ForegroundColor Magenta
    $junctionRoot = if ($ide -eq "cursor") {
        Join-Path $CursorRoot '.cursor\agents'
    } else {
        Join-Path $CursorRoot '.github\agents'
    }
    foreach ($folder in $agentFolders) {
        Deploy-Folder -Folder $folder -JunctionRoot $junctionRoot
    }
}

# --- Guidance (repo root) ---
$guidanceRoot = Join-Path $RepoRoot 'guidance'
$guidanceFolders = Find-MarkedFolders -Root $guidanceRoot -Markers @()
if ($guidanceFolders.Count -gt 0) {
    Write-Host "`n=== Guidance ===" -ForegroundColor Magenta
    foreach ($folder in $guidanceFolders) {
        Deploy-Folder -Folder $folder -JunctionRoot ""
    }
}

Write-Host "`nDone." -ForegroundColor Cyan
