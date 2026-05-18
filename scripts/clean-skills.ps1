<#
.SYNOPSIS
  Remove skill and agent junctions/links deployed by deploy-skills.ps1.

.DESCRIPTION
  Removes all IDE links and junctions deployed by deploy-skills.ps1.
  Never touches the user profile area.

  Cursor:
    <cursor-root>/.cursor/rules/         — hard links sourced from this repo
    <cursor-root>/.cursor/commands/      — hard links sourced from this repo
    <cursor-root>/.cursor/skills/<name>  — junctions pointing into this repo
    <cursor-root>/.cursor/agents/<name>  — junctions pointing into this repo

  VSCode:
    <cursor-root>/.github/               — hard links sourced from this repo
    <cursor-root>/.github/prompts/       — hard links sourced from this repo
    <cursor-root>/.github/skills/<name>  — junctions pointing into this repo
    <cursor-root>/.github/agents/<name>  — junctions pointing into this repo

.PARAMETER ide
  Target IDE: cursor or vscode. Default: cursor.

.PARAMETER DeployRoot
  Explicit root to clean from (e.g. C:\hero-desktop\city-of-heroes-virtual-tabletop).
  When omitted, falls back to skill-config.json -> workspace.active_skill_workspace,
  then Find-HighestCursorRoot walking up from the repo.

#>
param(
    [ValidateSet("cursor", "vscode")]
    [string] $ide = "cursor",
    [string] $DeployRoot = ""
)

$ErrorActionPreference = 'Stop'

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..') | Select-Object -ExpandProperty Path

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

    $parent = Split-Path $StartPath -Parent
    if ($parent -and ($parent -notmatch '^[A-Za-z]:\\?$') -and (Test-Path -LiteralPath (Join-Path $parent '.cursor') -PathType Container)) {
        return $parent
    }
    return $env:USERPROFILE
}

# Resolve CursorRoot: explicit -DeployRoot > skill-config.json; no fallback — crash if missing
if ($DeployRoot -and (Test-Path -LiteralPath $DeployRoot -PathType Container)) {
    $CursorRoot = $DeployRoot
} else {
    $skillConfig = Join-Path $RepoRoot 'skill-config.json'
    if (-not (Test-Path -LiteralPath $skillConfig -PathType Leaf)) {
        Write-Error "No skill-config.json found at '$skillConfig'. Run set_workspace.py or pass -DeployRoot explicitly."
        exit 1
    }
    $cfg = Get-Content $skillConfig -Raw | ConvertFrom-Json
    $configured = $cfg.workspace.active_skill_workspace
    if (-not $configured) {
        Write-Error "skill-config.json has no workspace.active_skill_workspace. Run set_workspace.py or pass -DeployRoot explicitly."
        exit 1
    }
    if (-not (Test-Path -LiteralPath $configured -PathType Container)) {
        Write-Error "workspace.active_skill_workspace '$configured' does not exist on disk. Run set_workspace.py or pass -DeployRoot explicitly."
        exit 1
    }
    $CursorRoot = $configured
}

Write-Host "`nRepo root   : $RepoRoot"  -ForegroundColor Cyan
Write-Host "Cursor root : $CursorRoot" -ForegroundColor Cyan
Write-Host "IDE         : $ide"        -ForegroundColor Cyan
Write-Host "Global      : $($global.IsPresent)`n" -ForegroundColor Cyan

# --- Discover skill/agent folders (same logic as deploy-skills.ps1) ---
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

$skillFolders    = Find-MarkedFolders -Root (Join-Path $RepoRoot 'skills')   -Markers @('SKILL.md')
$agentFolders    = Find-MarkedFolders -Root (Join-Path $RepoRoot 'agents')   -Markers @('AGENT.md', 'AGENTS.md')
$guidanceFolders = Find-MarkedFolders -Root (Join-Path $RepoRoot 'guidance') -Markers @()
$allFolders      = @($skillFolders) + @($agentFolders) + @($guidanceFolders)

function Get-IdePayloadRoot {
    param([string]$Root)
    $ideDir = Join-Path $Root 'guidance'
    if (Test-Path -LiteralPath $ideDir -PathType Container) { return $ideDir }
    return $Root
}

# --- Remove a single path (junction or hard link) ---
function Remove-Entry {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        Write-Host "  MISS: $Path" -ForegroundColor DarkGray
        return
    }
    Remove-Item -LiteralPath $Path -Recurse -Force
    Write-Host "  DEL : $Path" -ForegroundColor Red
}

# --- Clean repo-local IDE links ---
function Clean-LocalLinks {
    param([string]$Folder)

    $name       = (Split-Path $Folder -Leaf) -replace '_', '-'
    $idePayload = Get-IdePayloadRoot -Root $Folder

    Write-Host "[$name]" -ForegroundColor White

    if ($ide -eq "cursor") {
        Get-ChildItem -Path $idePayload -Filter '*.mdc'       -File -EA SilentlyContinue |
            ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".cursor\rules\$($_.Name)") }
        Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -EA SilentlyContinue |
            ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".cursor\commands\$($_.Name)") }
    }

    if ($ide -eq "vscode") {
        Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -EA SilentlyContinue |
            ForEach-Object {
                Remove-Entry (Join-Path $CursorRoot ".github\$($_.Name)")
            }
        Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -EA SilentlyContinue |
            ForEach-Object {
                Remove-Entry (Join-Path $CursorRoot ".github\prompts\$($_.Name)")
            }
    }

    # scripts/.vscode/tasks.json → <cursor-root>/.vscode/tasks.json (shared, not per-repo)
    $skillTasksJson = Join-Path $Folder 'scripts\.vscode\tasks.json'
    if (Test-Path -LiteralPath $skillTasksJson -PathType Leaf) {
        Remove-Entry (Join-Path $CursorRoot '.vscode\tasks.json')
    }
}

# --- Clean user-level junctions + user file links ---
function Clean-GlobalEntry {
    param([string]$Folder, [string]$JunctionRoot)

    $name       = (Split-Path $Folder -Leaf) -replace '_', '-'
    $idePayload = Get-IdePayloadRoot -Root $Folder

    Write-Host "[$name]" -ForegroundColor White

    # Junction
    Remove-Entry (Join-Path $JunctionRoot $name)
}

# === Local links ===
Write-Host "=== Local links ===" -ForegroundColor Magenta
foreach ($folder in $allFolders) { Clean-LocalLinks -Folder $folder }

# === Junctions ===
Write-Host "`n=== Junctions ===" -ForegroundColor Magenta

$skillJunctionRoot = if ($ide -eq "cursor") {
    Join-Path $CursorRoot '.cursor\skills'
} else {
    Join-Path $CursorRoot '.github\skills'
}

$agentJunctionRoot = if ($ide -eq "cursor") {
    Join-Path $CursorRoot '.cursor\agents'
} else {
    Join-Path $CursorRoot '.github\agents'
}

Write-Host "`n-- Skills --" -ForegroundColor DarkMagenta
foreach ($folder in $skillFolders) {
    Clean-GlobalEntry -Folder $folder -JunctionRoot $skillJunctionRoot
}

Write-Host "`n-- Agents --" -ForegroundColor DarkMagenta
foreach ($folder in $agentFolders) {
    Clean-GlobalEntry -Folder $folder -JunctionRoot $agentJunctionRoot
}

Write-Host "`nDone." -ForegroundColor Cyan
