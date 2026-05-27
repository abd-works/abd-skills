<#
.SYNOPSIS
  Remove skill and agent deployments created by deploy-skills.ps1.

.DESCRIPTION
  Removes all IDE links, junctions, and family-package copies deployed by deploy-skills.ps1.
  Never touches the user profile area.

  Family packages (grouped under foundational/, practices/, utilities/) deploy as copies.
  Standalone skills/ and agents/ at repo root deploy as junctions.

  Cursor:
    <deploy-root>/.cursor/rules/         — hard links sourced from this repo
    <deploy-root>/.cursor/commands/      — hard links sourced from this repo
    <deploy-root>/.cursor/skills/<name>  — copies or junctions from this repo
    <deploy-root>/.cursor/agents/<name>  — copies or junctions from this repo
    <deploy-root>/.cursor/content/       — merged content from family packages
    <deploy-root>/.cursor/lib/           — shared Python packages from family packages

  VSCode:
    <deploy-root>/.github/               — hard links sourced from this repo
    <deploy-root>/.github/prompts/       — hard links sourced from this repo
    <deploy-root>/.github/skills/<name>  — copies or junctions from this repo
    <deploy-root>/.github/agents/<name>  — copies or junctions from this repo
    <deploy-root>/.github/content/       — merged content from family packages
    <deploy-root>/.github/lib/           — shared Python packages from family packages

.PARAMETER ide
  Target IDE: cursor or vscode. Default: cursor.

.PARAMETER DeployRoot
  Explicit root to clean from (e.g. C:\dev\abd-pet-store-demo).
  When omitted, falls back to skill-config.json -> workspace.active_skill_workspace.

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

# --- Discover family packages (grouped under foundational/, practices/, utilities/) ---
# Mirrors the FAMILY_PACKAGES dict in deploy_family_package.py.
$FamilyPackagePaths = @(
    'foundational/context-to-memory',
    'foundational/skill-builder',
    'foundational/skill-helpers',
    'practices/architecture-centric-engineering',
    'practices/delivery',
    'practices/delivery/user-experience-design',
    'practices/domain-driven-design',
    'practices/idea-shaping',
    'practices/story-driven-delivery',
    'utilities'
)

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

# === Family package copies ===
Write-Host "`n=== Family packages ===" -ForegroundColor Magenta

$ideRoot = if ($ide -eq "cursor") { Join-Path $CursorRoot '.cursor' } else { Join-Path $CursorRoot '.github' }

foreach ($relPath in $FamilyPackagePaths) {
    $pkgDir = Join-Path $RepoRoot $relPath
    if (-not (Test-Path -LiteralPath $pkgDir -PathType Container)) { continue }
    $pkgName = Split-Path $relPath -Leaf
    Write-Host "[$pkgName]" -ForegroundColor White

    # Skills deployed by this package
    $skillsSrc = Join-Path $pkgDir 'skills'
    if (Test-Path -LiteralPath $skillsSrc -PathType Container) {
        Get-ChildItem -Path $skillsSrc -Directory -ErrorAction SilentlyContinue |
            Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') -PathType Leaf } |
            ForEach-Object {
                $target = Join-Path $ideRoot "skills\$($_.Name)"
                Remove-Entry $target
            }
    }

    # Agents deployed by this package (markers or _-prefixed shared folders)
    $agentsSrc = Join-Path $pkgDir 'agents'
    if (Test-Path -LiteralPath $agentsSrc -PathType Container) {
        Get-ChildItem -Path $agentsSrc -Directory -ErrorAction SilentlyContinue |
            Where-Object {
                (Test-Path (Join-Path $_.FullName 'AGENT.md') -PathType Leaf) -or
                (Test-Path (Join-Path $_.FullName 'AGENTS.md') -PathType Leaf) -or
                $_.Name.StartsWith('_')
            } |
            ForEach-Object {
                $target = Join-Path $ideRoot "agents\$($_.Name)"
                Remove-Entry $target
            }
    }

    # IDE files (instructions → rules/instructions, prompts → commands/prompts)
    $instrSrc = Join-Path $pkgDir 'instructions'
    $promptsSrc = Join-Path $pkgDir 'prompts'
    if ($ide -eq "cursor") {
        if (Test-Path -LiteralPath $instrSrc -PathType Container) {
            Get-ChildItem -Path $instrSrc -Filter '*.mdc' -File -EA SilentlyContinue |
                ForEach-Object { Remove-Entry (Join-Path $ideRoot "rules\$($_.Name)") }
        }
        if (Test-Path -LiteralPath $promptsSrc -PathType Container) {
            Get-ChildItem -Path $promptsSrc -Filter '*.prompt.md' -File -EA SilentlyContinue |
                ForEach-Object { Remove-Entry (Join-Path $ideRoot "commands\$($_.Name)") }
        }
    } else {
        if (Test-Path -LiteralPath $instrSrc -PathType Container) {
            Get-ChildItem -Path $instrSrc -Filter '*.instructions.md' -File -EA SilentlyContinue |
                ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".github\$($_.Name)") }
        }
        if (Test-Path -LiteralPath $promptsSrc -PathType Container) {
            Get-ChildItem -Path $promptsSrc -Filter '*.prompt.md' -File -EA SilentlyContinue |
                ForEach-Object { Remove-Entry (Join-Path $CursorRoot ".github\prompts\$($_.Name)") }
        }
    }
}

# Content and lib are fully managed by deploy — clean them entirely
$contentDir = Join-Path $ideRoot 'content'
if (Test-Path -LiteralPath $contentDir -PathType Container) {
    Write-Host "`n-- Content --" -ForegroundColor DarkMagenta
    Remove-Entry $contentDir
}

$libDir = Join-Path $ideRoot 'lib'
if (Test-Path -LiteralPath $libDir -PathType Container) {
    Write-Host "`n-- Lib --" -ForegroundColor DarkMagenta
    Remove-Entry $libDir
}

Write-Host "`nDone." -ForegroundColor Cyan
