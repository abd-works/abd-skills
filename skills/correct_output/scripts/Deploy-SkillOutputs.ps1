<#
.SYNOPSIS
  Deploy this skill's IDE files (rule, instruction, command) to a target project.

.DESCRIPTION
  Links this skill's deliverable IDE files into the correct locations for Cursor
  and/or VS Code in any project:

  IDE helper files live under **`ide-files/`** next to **`SKILL.md`**. If that folder is missing,
  the script falls back to the skill root (legacy).

    ide-files/*.mdc              → .cursor/rules/
    ide-files/*.instructions.md  → .vscode/                 (with -IDE VSCode or Both only)
    ide-files/*.prompt.md        → .cursor/commands/         (default -IDE Cursor)
                                 → .github/prompts/        (with -IDE VSCode or Both only)

  Also creates a skill junction in ~/.cursor/skills/ so Cursor can discover the skill.

.PARAMETER ProjectRoot
  Target project where rule/instruction/command hard links are created.
  Required — no default.

.PARAMETER IDE
  Which IDE targets to deploy to: Cursor, VSCode, or Both. Default: Cursor.

.PARAMETER SkillJunction
  Also create the ~/.cursor/skills/ junction. Default: true.

.PARAMETER CursorSkillsRoot
  Cursor user skills directory. Default: $env:USERPROFILE\.cursor\skills

.PARAMETER Force
  Remove existing entries before creating links.
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $ProjectRoot,

    [ValidateSet("Cursor", "VSCode", "Both")]
    [string] $IDE = "Cursor",

    [bool] $SkillJunction = $true,

    [string] $CursorSkillsRoot = $(Join-Path $env:USERPROFILE '.cursor\skills'),

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

$source = Resolve-Path (Join-Path $PSScriptRoot '..')
$SkillName = (Split-Path $source -Leaf) -replace '_', '-'

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
if ($SkillJunction) {
    Write-Host "`n[Skill] $SkillName -> Cursor skills..."
    $dest = Join-Path $CursorSkillsRoot $SkillName
    New-LinkSafe -Path $dest -Target $source
}

# --- 2. .mdc → .cursor/rules/ ---
$mdcFiles = Get-ChildItem -Path $idePayload -Filter '*.mdc' -File -ErrorAction SilentlyContinue
if ($mdcFiles -and ($IDE -eq "Cursor" -or $IDE -eq "Both")) {
    Write-Host "`n[Rules] .mdc -> .cursor/rules/..."
    foreach ($f in $mdcFiles) {
        $ruleDest = Join-Path $ProjectRoot ".cursor\rules\$($f.Name)"
        New-LinkSafe -Path $ruleDest -Target $f.FullName -IsFile
    }
}

# --- 3. .instructions.md → .vscode/ ---
$instrFiles = Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -ErrorAction SilentlyContinue
if ($instrFiles -and ($IDE -eq "VSCode" -or $IDE -eq "Both")) {
    Write-Host "`n[Instructions] .instructions.md -> .vscode/..."
    foreach ($f in $instrFiles) {
        $instrDest = Join-Path $ProjectRoot ".vscode\$($f.Name)"
        New-LinkSafe -Path $instrDest -Target $f.FullName -IsFile
    }
}

# --- 4. .prompt.md → commands/prompts ---
$promptFiles = Get-ChildItem -Path $idePayload -Filter '*.prompt.md' -File -ErrorAction SilentlyContinue
if ($promptFiles) {
    if ($IDE -eq "Cursor" -or $IDE -eq "Both") {
        Write-Host "`n[Commands] .prompt.md -> .cursor/commands/..."
        foreach ($f in $promptFiles) {
            $cmdDest = Join-Path $ProjectRoot ".cursor\commands\$($f.Name)"
            New-LinkSafe -Path $cmdDest -Target $f.FullName -IsFile
        }
    }
    if ($IDE -eq "VSCode" -or $IDE -eq "Both") {
        Write-Host "`n[Prompts] .prompt.md -> .github/prompts/..."
        foreach ($f in $promptFiles) {
            $promptDest = Join-Path $ProjectRoot ".github\prompts\$($f.Name)"
            New-LinkSafe -Path $promptDest -Target $f.FullName -IsFile
        }
    }
}

Write-Host "`nDone." -ForegroundColor Cyan
