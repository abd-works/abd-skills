<#
.SYNOPSIS
  Create directory junctions so Cursor discovers the module-partition skill globally
  (~/.cursor/skills/) and under agilebydesign-skills/.cursor/skills/.

.DESCRIPTION
  Canonical source: skills/abd-domain-driven-design/module-partition/. Junctions point here — no copies.

.PARAMETER UserOnly
  Only create the user-level junction.

.PARAMETER ProjectOnly
  Only create the project-level junction under the repo .cursor/skills/.
#>
[CmdletBinding()]
param(
    [switch]$UserOnly,
    [switch]$ProjectOnly
)

$ErrorActionPreference = "Stop"

$skillRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
# module-partition -> skills -> abd-domain-driven-design -> agents -> repo root
$repoRoot  = (Get-Item (Join-Path $skillRoot "..\..\..\..")).FullName

$userSkills    = "$env:USERPROFILE\.cursor\skills"
$projectSkills = Join-Path $repoRoot ".cursor\skills"

function New-JunctionSafe {
    param([string]$Link, [string]$Target)
    if (Test-Path $Link) {
        $item = Get-Item $Link -Force
        if ($item.LinkType -eq "Junction" -or $item.Attributes -match "ReparsePoint") {
            $currentTarget = $item.Target
            if ($currentTarget -eq $Target) {
                Write-Host "  exists (junction, correct target): $Link" -ForegroundColor DarkGray
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

if (-not $ProjectOnly) {
    Write-Host "User-level junction (~/.cursor/skills/):" -ForegroundColor Cyan
    New-JunctionSafe -Link "$userSkills\module-partition" -Target $skillRoot
}

if (-not $UserOnly) {
    Write-Host "Project-level junction (.cursor/skills/):" -ForegroundColor Cyan
    New-JunctionSafe -Link "$projectSkills\module-partition" -Target $skillRoot
}

Write-Host ""
Write-Host "Done. Restart Cursor or open Settings > Rules to verify the skill is loaded." -ForegroundColor Green
