<#
.SYNOPSIS
  Create directory junctions so Cursor discovers the abd-answers agent
  and its skills globally (user-level).
.PARAMETER UserOnly
  Only create user-level junctions.
.PARAMETER ProjectOnly
  Only create project-level junctions under the repo .cursor/skills/.
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
    Write-Host "User-level junctions (~/.cursor/skills/):"
    foreach ($j in $junctions) {
        New-JunctionSafe -Link "$userSkills\$($j.Name)" -Target $j.Source
    }
}

if (-not $UserOnly) {
    Write-Host "Project-level junctions (.cursor/skills/):"
    foreach ($j in $junctions) {
        New-JunctionSafe -Link "$projectSkills\$($j.Name)" -Target $j.Source
    }
}

Write-Host ""
Write-Host "Done. Restart Cursor or open Settings > Rules to verify skills are loaded."
