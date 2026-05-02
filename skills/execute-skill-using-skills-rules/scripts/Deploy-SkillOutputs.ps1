<#
.SYNOPSIS
  Deploy this skill's IDE files (rule, instruction, command) to a target project.

.DESCRIPTION
  Canonical IDE helpers live under **`ide-files/`**. The Cursor skill junction name is
  **`execute-skill-using-skills-rules`** (matches this folder — see **SKILL.md**).

  Default **`-IDE Cursor`**: `.mdc` → `.cursor/rules/`, `.prompt.md` → `.cursor/commands/`.
  **`-IDE VSCode`** or **`-IDE Both`** also links `.instructions.md` → `.vscode/` and
  `.prompt.md` → `.github/prompts/`.

.PARAMETER ProjectRoot
  Target project where rule/instruction/command hard links are created.

.PARAMETER IDE
  Cursor, VSCode, or Both. Default: Cursor (VS Code / `.github/prompts` only with VSCode or Both).

.PARAMETER SkillJunction
  Create ~/.cursor/skills/execute-skill-using-skills-rules → this skill folder. Default: true.

.PARAMETER Force
  Replace existing links.
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
$SkillName = 'execute-skill-using-skills-rules'

function Get-IdePayloadRoot {
    param([string]$SkillRoot)
    $ide = Join-Path $SkillRoot 'ide-files'
    if (Test-Path -LiteralPath $ide -PathType Container) {
        return $ide
    }
    return $SkillRoot
}
$idePayload = Get-IdePayloadRoot -SkillRoot $source

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

if ($SkillJunction) {
    Write-Host "`n[Skill] $SkillName -> Cursor skills..."
    $dest = Join-Path $CursorSkillsRoot $SkillName
    New-LinkSafe -Path $dest -Target $source
}

$mdcFiles = Get-ChildItem -Path $idePayload -Filter '*.mdc' -File -ErrorAction SilentlyContinue
if ($mdcFiles -and ($IDE -eq "Cursor" -or $IDE -eq "Both")) {
    Write-Host "`n[Rules] .mdc -> .cursor/rules/..."
    foreach ($f in $mdcFiles) {
        $ruleDest = Join-Path $ProjectRoot ".cursor\rules\$($f.Name)"
        New-LinkSafe -Path $ruleDest -Target $f.FullName -IsFile
    }
}

$instrFiles = Get-ChildItem -Path $idePayload -Filter '*.instructions.md' -File -ErrorAction SilentlyContinue
if ($instrFiles -and ($IDE -eq "VSCode" -or $IDE -eq "Both")) {
    Write-Host "`n[Instructions] .instructions.md -> .vscode/..."
    foreach ($f in $instrFiles) {
        $instrDest = Join-Path $ProjectRoot ".vscode\$($f.Name)"
        New-LinkSafe -Path $instrDest -Target $f.FullName -IsFile
    }
}

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
