<#
.SYNOPSIS
  Links a skill folder from agilebydesign-skills into Cursor's global skills folder via a
  directory junction, and deploys any .mdc rule, .instructions.md, and .prompt.md files
  found under **`ide-files/`** in the skill (or the skill root for legacy packages).

.PARAMETER SkillName
  Folder name under skills/ (e.g. story-graph-ops).

.PARAMETER SkillsRepoRoot
  Path to the agilebydesign-skills repo root (the folder that contains skills/). If omitted,
  inferred from this script's location. Ignored when SkillSourcePath is set.

.PARAMETER SkillSourcePath
  Full path to the skill folder when it is not under skills/<SkillName>
  (e.g. agents/abd-domain-driven-design/skills/domain-scan).

.PARAMETER CursorSkillsRoot
  Cursor user skills directory. Default: $env:USERPROFILE\.cursor\skills

.PARAMETER ProjectRoot
  Target project for rule/instruction/command deployment.
  Defaults to the agilebydesign-skills repo root.

.PARAMETER IDE
  Which IDE targets to deploy rules/instructions/commands to.
  Values: Cursor, VSCode, Both. Default: Cursor.

.PARAMETER Force
  Remove an existing entry at the junction path before creating the directory junction.
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $SkillName,

    [string] $SkillsRepoRoot = "",

    [string] $CursorSkillsRoot = $(Join-Path $env:USERPROFILE '.cursor\skills'),

    [string] $SkillSourcePath = "",

    [string] $ProjectRoot = "",

    [ValidateSet("Cursor", "VSCode", "Both")]
    [string] $IDE = "Cursor",

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

if ($SkillsRepoRoot) {
    $skillsDir = Join-Path $SkillsRepoRoot 'skills'
} else {
    # .../skills/deploy-skill-to-cursor/scripts -> .../skills
    $skillsDir = Resolve-Path (Join-Path $PSScriptRoot '..\..')
}

if ($SkillSourcePath) {
    $source = (Resolve-Path -LiteralPath $SkillSourcePath).Path
} else {
    $source = Join-Path $skillsDir $SkillName
}
if (-not (Test-Path -LiteralPath $source -PathType Container)) {
    throw "Skill folder not found: $source"
}

if (-not $ProjectRoot) {
    # repo root = one level above skills/
    $ProjectRoot = Resolve-Path (Join-Path $skillsDir '..')
}

function Get-IdePayloadRoot {
    param([string]$SkillRoot)
    $ide = Join-Path $SkillRoot 'ide-files'
    if (Test-Path -LiteralPath $ide -PathType Container) {
        return $ide
    }
    return $SkillRoot
}
$idePayload = Get-IdePayloadRoot -SkillRoot $source

# --- Helper ---
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
        New-Item -ItemType Junction -Path $Path -Target $Target | Out-Null
    }
    Write-Host "  OK: $Path -> $Target" -ForegroundColor Green
}

# --- 1. Skill junction ---
Write-Host "`n[Skill] $SkillName -> Cursor skills..."
$dest = Join-Path $CursorSkillsRoot $SkillName
New-LinkSafe -Path $dest -Target $source

# --- 2. Deploy .mdc files (Cursor rules) ---
$mdcFiles = Get-ChildItem -Path $idePayload -Filter '*.mdc' -File -ErrorAction SilentlyContinue
if ($mdcFiles -and ($IDE -eq "Cursor" -or $IDE -eq "Both")) {
    Write-Host "`n[Rules] Deploying .mdc files to .cursor/rules/..."
    foreach ($f in $mdcFiles) {
        $ruleDest = Join-Path $ProjectRoot ".cursor\rules\$($f.Name)"
        New-LinkSafe -Path $ruleDest -Target $f.FullName -IsFile
    }
}

# --- 3. Deploy .instructions.md files (VS Code rules) ---
$instrFiles = Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -ErrorAction SilentlyContinue
if ($instrFiles -and ($IDE -eq "VSCode" -or $IDE -eq "Both")) {
    Write-Host "`n[Instructions] Deploying .instructions.md files to .vscode/..."
    foreach ($f in $instrFiles) {
        $instrDest = Join-Path $ProjectRoot ".vscode\$($f.Name)"
        New-LinkSafe -Path $instrDest -Target $f.FullName -IsFile
    }
}

# --- 4. Deploy .prompt.md files (commands) ---
$promptFiles = Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue
if ($promptFiles) {
    if ($IDE -eq "Cursor" -or $IDE -eq "Both") {
        Write-Host "`n[Commands] Deploying .prompt.md files to .cursor/commands/..."
        foreach ($f in $promptFiles) {
            $cmdDest = Join-Path $ProjectRoot ".cursor\commands\$($f.Name)"
            New-LinkSafe -Path $cmdDest -Target $f.FullName -IsFile
        }
    }
    if ($IDE -eq "VSCode" -or $IDE -eq "Both") {
        Write-Host "`n[Prompts] Deploying .prompt.md files to .github/prompts/..."
        foreach ($f in $promptFiles) {
            $promptDest = Join-Path $ProjectRoot ".github\prompts\$($f.Name)"
            New-LinkSafe -Path $promptDest -Target $f.FullName -IsFile
        }
    }
}

Write-Host "`nDone." -ForegroundColor Cyan
