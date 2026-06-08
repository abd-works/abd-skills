<#
.SYNOPSIS
  Remove skill and agent deployments created by deploy-skills.ps1.

.DESCRIPTION
  Removes all IDE links, junctions, and family-package copies deployed by deploy-skills.ps1.
  Never touches the user profile area.

  Family packages (grouped under foundational/, practices/, utilities/) deploy as copies.
  Standalone skills/ and agents/ at repo root deploy as junctions.

  Always cleans both IDE targets:
    <deploy-root>/.cursor/rules/               — Cursor rules
    <deploy-root>/.cursor/commands/            — Cursor commands
    <deploy-root>/.cursor/skills/<name>        — skill copies/junctions
    <deploy-root>/.cursor/agents/<name>        — agent copies/junctions
    <deploy-root>/.cursor/content/             — merged content
    <deploy-root>/.cursor/lib/                 — shared Python packages
    <deploy-root>/.github/instructions/        — VS Code instructions
    <deploy-root>/.github/prompts/             — VS Code prompts
    <deploy-root>/.github/skills/<name>        — skill copies/junctions
    <deploy-root>/.github/agents/<name>        — agent copies/junctions
    <deploy-root>/.vscode/tasks.json           — merged tasks
    <deploy-root>/.vscode/settings.json        — merged settings

.PARAMETER DeployRoot
  Explicit root to clean from (e.g. C:\dev\abd-pet-store-demo).
  When omitted, falls back to skill-config.json -> workspace.active_skill_workspace.

#>
param(
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
Write-Host "Deploy root : $CursorRoot" -ForegroundColor Cyan
Write-Host "Cleaning    : .cursor/ + .github/ + .vscode/`n" -ForegroundColor Cyan

# --- Discover family packages — same logic as deploy-skills.ps1 Get-PackageRoots ---
$FamilyPackagePaths = @()
foreach ($top in @('practices', 'foundational')) {
    $topPath = Join-Path $RepoRoot $top
    if (-not (Test-Path -LiteralPath $topPath -PathType Container)) { continue }
    Get-ChildItem -LiteralPath $topPath -Directory | ForEach-Object {
        $FamilyPackagePaths += (Resolve-Path -LiteralPath $_.FullName | Select-Object -ExpandProperty Path)
    }
}
$utilitiesPath = Join-Path $RepoRoot 'utilities'
if (Test-Path -LiteralPath $utilitiesPath -PathType Container) {
    $FamilyPackagePaths += (Resolve-Path -LiteralPath $utilitiesPath | Select-Object -ExpandProperty Path)
}

# --- Discover standalone skill/agent folders (legacy: skills/ and agents/ at repo root) ---
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

    Get-ChildItem -Path $idePayload -Filter '*.mdc'       -File -EA SilentlyContinue |
        ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".cursor\rules\$($_.Name)") }
    Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -EA SilentlyContinue |
        ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".cursor\commands\$($_.Name)") }
    Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -EA SilentlyContinue |
        ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".github\instructions\$($_.Name)") }
    Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -EA SilentlyContinue |
        ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".github\prompts\$($_.Name)") }
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

$skillJunctionRoot_cursor = Join-Path $CursorRoot '.cursor\skills'
$skillJunctionRoot_github = Join-Path $CursorRoot '.github\skills'
$agentJunctionRoot_cursor = Join-Path $CursorRoot '.cursor\agents'
$agentJunctionRoot_github = Join-Path $CursorRoot '.github\agents'

Write-Host "`n-- Skills --" -ForegroundColor DarkMagenta
foreach ($folder in $skillFolders) {
    Clean-GlobalEntry -Folder $folder -JunctionRoot $skillJunctionRoot_cursor
    Clean-GlobalEntry -Folder $folder -JunctionRoot $skillJunctionRoot_github
}

Write-Host "`n-- Agents --" -ForegroundColor DarkMagenta
foreach ($folder in $agentFolders) {
    Clean-GlobalEntry -Folder $folder -JunctionRoot $agentJunctionRoot_cursor
    Clean-GlobalEntry -Folder $folder -JunctionRoot $agentJunctionRoot_github
}

# === Family package copies ===
Write-Host "`n=== Family packages ===" -ForegroundColor Magenta

$cursorRoot_ide = Join-Path $CursorRoot '.cursor'
$githubRoot_ide = Join-Path $CursorRoot '.github'

foreach ($pkgDir in $FamilyPackagePaths) {
    if (-not (Test-Path -LiteralPath $pkgDir -PathType Container)) { continue }
    $pkgName = Split-Path $pkgDir -Leaf
    Write-Host "[$pkgName]" -ForegroundColor White

    # Skills deployed by this package
    $skillsSrc = Join-Path $pkgDir 'skills'
    if (Test-Path -LiteralPath $skillsSrc -PathType Container) {
        Get-ChildItem -Path $skillsSrc -Directory -ErrorAction SilentlyContinue |
            Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') -PathType Leaf } |
            ForEach-Object {
                Remove-Entry (Join-Path $cursorRoot_ide "skills\$($_.Name)")
                Remove-Entry (Join-Path $githubRoot_ide "skills\$($_.Name)")
            }
    }

    # Agents deployed by this package
    $agentsSrc = Join-Path $pkgDir 'agents'
    if (Test-Path -LiteralPath $agentsSrc -PathType Container) {
        Get-ChildItem -Path $agentsSrc -Directory -ErrorAction SilentlyContinue |
            Where-Object {
                (Test-Path (Join-Path $_.FullName 'AGENT.md') -PathType Leaf) -or
                (Test-Path (Join-Path $_.FullName 'AGENTS.md') -PathType Leaf) -or
                $_.Name.StartsWith('_')
            } |
            ForEach-Object {
                Remove-Entry (Join-Path $cursorRoot_ide "agents\$($_.Name)")
                Remove-Entry (Join-Path $githubRoot_ide "agents\$($_.Name)")
            }
    }

    # Instructions and prompts — both IDEs
    $instrSrc   = Join-Path $pkgDir 'instructions'
    $promptsSrc = Join-Path $pkgDir 'prompts'
    if (Test-Path -LiteralPath $instrSrc -PathType Container) {
        Get-ChildItem -Path $instrSrc -Filter '*.mdc' -File -EA SilentlyContinue |
            ForEach-Object { Remove-Entry (Join-Path $cursorRoot_ide "rules\$($_.Name)") }
        Get-ChildItem -Path $instrSrc -Filter '*.instructions.md' -File -EA SilentlyContinue |
            ForEach-Object { Remove-Entry (Join-Path $githubRoot_ide "instructions\$($_.Name)") }
    }
    if (Test-Path -LiteralPath $promptsSrc -PathType Container) {
        Get-ChildItem -Path $promptsSrc -Filter '*.prompt.md' -File -EA SilentlyContinue |
            ForEach-Object {
                Remove-Entry (Join-Path $cursorRoot_ide "commands\$($_.Name)")
                Remove-Entry (Join-Path $githubRoot_ide "prompts\$($_.Name)")
            }
    }
}

# Content and lib — clean from both IDE roots
foreach ($ideRoot in @($cursorRoot_ide, $githubRoot_ide)) {
    $contentDir = Join-Path $ideRoot 'content'
    if (Test-Path -LiteralPath $contentDir -PathType Container) {
        Write-Host "`n-- Content ($ideRoot) --" -ForegroundColor DarkMagenta
        Remove-Entry $contentDir
    }
    $libDir = Join-Path $ideRoot 'lib'
    if (Test-Path -LiteralPath $libDir -PathType Container) {
        Write-Host "`n-- Lib ($ideRoot) --" -ForegroundColor DarkMagenta
        Remove-Entry $libDir
    }
}

# .vscode/ files merged from package vscode/ folders — remove if any package contributed them
$vscodeDst = Join-Path $CursorRoot '.vscode'
$anyVscode = $false
foreach ($pkgDir in $FamilyPackagePaths) {
    if (Test-Path -LiteralPath (Join-Path $pkgDir 'vscode') -PathType Container) {
        $anyVscode = $true
        break
    }
}
if ($anyVscode) {
    Write-Host "`n-- .vscode --" -ForegroundColor DarkMagenta
    Remove-Entry (Join-Path $vscodeDst 'tasks.json')
    Remove-Entry (Join-Path $vscodeDst 'settings.json')
}

# Remove container folders only if empty
Write-Host "`n=== Removing empty IDE container folders ===" -ForegroundColor Magenta
foreach ($folder in @(
    (Join-Path $CursorRoot '.cursor\rules'),
    (Join-Path $CursorRoot '.cursor\commands'),
    (Join-Path $CursorRoot '.cursor\skills'),
    (Join-Path $CursorRoot '.cursor\agents'),
    (Join-Path $CursorRoot '.cursor'),
    (Join-Path $CursorRoot '.github\instructions'),
    (Join-Path $CursorRoot '.github\prompts'),
    (Join-Path $CursorRoot '.github\skills'),
    (Join-Path $CursorRoot '.github\agents'),
    (Join-Path $CursorRoot '.github')
)) {
    if (Test-Path -LiteralPath $folder) {
        $children = Get-ChildItem -LiteralPath $folder -Recurse -Force -ErrorAction SilentlyContinue
        if (-not $children) {
            Remove-Item -LiteralPath $folder -Recurse -Force
            Write-Host "  DEL : $folder" -ForegroundColor Red
        } else {
            Write-Host "  SKIP (not empty): $folder" -ForegroundColor DarkGray
        }
    }
}

Write-Host "`nDone." -ForegroundColor Cyan
