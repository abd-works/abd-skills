<#
.SYNOPSIS
  Create directory junctions so Cursor discovers the abd-answers agent
  and its skills globally (user-level) and optionally in the abd-answers project.

.DESCRIPTION
  This skill tree under agilebydesign-skills is the canonical source.
  Junctions point Cursor and the abd-answers project here — no file copies.

.PARAMETER UserOnly
  Only create user-level junctions (~/.cursor/skills/).

.PARAMETER ProjectOnly
  Only create project-level junctions under the skills-repo .cursor/skills/.

.PARAMETER AbdAnswersRepo
  Path to the abd-answers repo. When provided (or auto-detected at
  C:\dev\abd-answers), creates junctions under <abd-answers>/.cursor/skills/
  pointing back to this skill tree.

.PARAMETER SkipAbdAnswers
  Skip abd-answers project junctions even when the repo is detected.
#>
[CmdletBinding()]
param(
    [switch]$UserOnly,
    [switch]$ProjectOnly,
    [string]$AbdAnswersRepo,
    [switch]$SkipAbdAnswers
)

$ErrorActionPreference = "Stop"

$agentRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot  = Split-Path -Parent (Split-Path -Parent $agentRoot)

$userSkills    = "$env:USERPROFILE\.cursor\skills"
$projectSkills = "$repoRoot\.cursor\skills"

$skillsDir = "$agentRoot\skills"

$junctions = @(
    @{ Name = "abd-answers";      Source = $agentRoot }
    @{ Name = "convert-content";  Source = "$skillsDir\convert-content" }
    @{ Name = "chunk-content";    Source = "$skillsDir\chunk-content" }
    @{ Name = "embed-pinecone";   Source = "$skillsDir\embed-pinecone" }
    @{ Name = "query-pinecone";   Source = "$skillsDir\query-pinecone" }
)

function New-JunctionSafe {
    param([string]$Link, [string]$Target)
    if (Test-Path $Link) {
        $item = Get-Item $Link -Force
        if ($item.LinkType -eq "Junction" -or $item.Attributes -match "ReparsePoint") {
            $currentTarget = $item.Target
            if ($currentTarget -eq $Target) {
                Write-Host "  exists (junction, correct target): $Link"
                return
            }
            Write-Host "  removing stale junction: $Link -> $currentTarget" -ForegroundColor Yellow
            $item.Delete()
        } else {
            Write-Warning "  $Link exists but is NOT a junction -- skipping (remove manually if safe)"
            return
        }
    }
    $parent = Split-Path $Link -Parent
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    New-Item -ItemType Junction -Path $Link -Target $Target | Out-Null
    Write-Host "  created: $Link -> $Target" -ForegroundColor Green
}

# ── User-level junctions ────────────────────────────────────────────────────
if (-not $ProjectOnly) {
    Write-Host "User-level junctions (~/.cursor/skills/):" -ForegroundColor Cyan
    foreach ($j in $junctions) {
        New-JunctionSafe -Link "$userSkills\$($j.Name)" -Target $j.Source
    }
}

# ── Project-level junctions (agilebydesign-skills repo) ────────────────────
if (-not $UserOnly) {
    Write-Host "Project-level junctions (.cursor/skills/):" -ForegroundColor Cyan
    foreach ($j in $junctions) {
        New-JunctionSafe -Link "$projectSkills\$($j.Name)" -Target $j.Source
    }
}

# ── abd-answers project junctions ──────────────────────────────────────────
if (-not $SkipAbdAnswers) {
    if (-not $AbdAnswersRepo) {
        $defaultAbdPath = "C:\dev\abd-answers"
        if (Test-Path $defaultAbdPath) {
            $AbdAnswersRepo = $defaultAbdPath
        }
    }
    if ($AbdAnswersRepo -and (Test-Path $AbdAnswersRepo)) {
        $abdSkills = "$AbdAnswersRepo\.cursor\skills"
        Write-Host "abd-answers project junctions ($abdSkills):" -ForegroundColor Cyan
        foreach ($j in $junctions) {
            New-JunctionSafe -Link "$abdSkills\$($j.Name)" -Target $j.Source
        }
    } else {
        Write-Host "abd-answers repo not found - skipping project junctions." -ForegroundColor DarkGray
        Write-Host '  Pass -AbdAnswersRepo <path> to create them.' -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host 'Done. Restart Cursor or open Settings > Rules to verify skills are loaded.' -ForegroundColor Green
