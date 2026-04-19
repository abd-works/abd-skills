<#
.SYNOPSIS
  Create a directory junction so Cursor discovers the abd-team-member agent
  globally (user-level) under ~/.cursor/skills/.

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

$agentRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot  = Split-Path -Parent (Split-Path -Parent $agentRoot)

$userSkills    = "$env:USERPROFILE\.cursor\skills"
$projectSkills = "$repoRoot\.cursor\skills"

function New-JunctionSafe {
    param([string]$Link, [string]$Target)
    if (Test-Path $Link) {
        $item = Get-Item $Link -Force
        if ($item.LinkType -eq "Junction" -or $item.Attributes -match "ReparsePoint") {
            Write-Host "  exists (junction): $Link"
            return
        }
        Write-Warning "  $Link exists but is NOT a junction -- skipping (remove manually if safe)"
        return
    }
    $parent = Split-Path $Link -Parent
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    New-Item -ItemType Junction -Path $Link -Target $Target | Out-Null
    Write-Host "  created: $Link -> $Target"
}

if (-not $ProjectOnly) {
    Write-Host "User-level junction (~/.cursor/skills/):"
    New-JunctionSafe -Link "$userSkills\abd-team-member" -Target $agentRoot
}

if (-not $UserOnly) {
    Write-Host "Project-level junction (.cursor/skills/):"
    New-JunctionSafe -Link "$projectSkills\abd-team-member" -Target $agentRoot
}

Write-Host ""
Write-Host "Done. Restart Cursor or open Settings > Rules to verify the agent is loaded."
