# Create directory junctions so Cursor discovers domain-language (~/.cursor/skills/ and repo .cursor/skills/).
[CmdletBinding()]
param(
    [switch]$UserOnly,
    [switch]$ProjectOnly
)

$ErrorActionPreference = "Stop"

$skillRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
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
    New-JunctionSafe -Link "$userSkills\domain-language" -Target $skillRoot
}

if (-not $UserOnly) {
    Write-Host "Project-level junction (.cursor/skills/):" -ForegroundColor Cyan
    New-JunctionSafe -Link "$projectSkills\domain-language" -Target $skillRoot
}

Write-Host ""
Write-Host "Done. Restart Cursor or open Settings > Rules to verify the skill is loaded." -ForegroundColor Green
