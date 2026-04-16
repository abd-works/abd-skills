<#
.SYNOPSIS
  Links a skill folder from agilebydesign-skills into Cursor's global skills folder via a directory junction.

.PARAMETER SkillName
  Folder name under skills/ (e.g. story-graph-ops).

.PARAMETER SkillsRepoRoot
  Path to the agilebydesign-skills repo root (the folder that contains skills/). If omitted, inferred from this script's location.

.PARAMETER CursorSkillsRoot
  Cursor user skills directory. Default: $env:USERPROFILE\.cursor\skills

.PARAMETER Force
  Remove an existing entry at the junction path before creating the link.
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $SkillName,

    [string] $SkillsRepoRoot = "",

    [string] $CursorSkillsRoot = $(Join-Path $env:USERPROFILE '.cursor\skills'),

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

if ($SkillsRepoRoot) {
    $skillsDir = Join-Path $SkillsRepoRoot 'skills'
} else {
    # .../skills/deploy-skill-to-cursor/scripts -> .../skills
    $skillsDir = Resolve-Path (Join-Path $PSScriptRoot '..\..')
}

$source = Join-Path $skillsDir $SkillName
if (-not (Test-Path -LiteralPath $source -PathType Container)) {
    throw "Skill folder not found: $source"
}

$dest = Join-Path $CursorSkillsRoot $SkillName
if (Test-Path -LiteralPath $dest) {
    if (-not $Force) {
        throw "Already exists: $dest (use -Force to replace)"
    }
    Remove-Item -LiteralPath $dest -Recurse -Force
}

if (-not (Test-Path -LiteralPath $CursorSkillsRoot -PathType Container)) {
    New-Item -ItemType Directory -Path $CursorSkillsRoot -Force | Out-Null
}

New-Item -ItemType Junction -Path $dest -Target $source | Out-Null
Write-Host "Junction: $dest -> $source"
