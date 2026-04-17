#Requires -Version 5.1
<#
.SYNOPSIS
  Download all wheels for agents/abd-context-engine/requirements-all.txt into vendor/wheels (for offline pip install).

.PARAMETER Python
  Python executable (default: python on PATH).

.PARAMETER Requirements
  Path to requirements-all.txt (default: ../requirements-all.txt next to this script).

.PARAMETER OutDir
  Output directory for wheels (default: ../vendor/wheels).
#>
param(
 [string] $Python = "python",
    [string] $Requirements = (Join-Path (Split-Path $PSScriptRoot -Parent) "requirements-all.txt"),
    [string] $OutDir = (Join-Path (Split-Path $PSScriptRoot -Parent) "vendor" "wheels")
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path $Requirements)) {
    Write-Error "Requirements file not found: $Requirements"
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
& $Python -m pip download -r $Requirements -d $OutDir
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
Write-Host "Wheels written to: $OutDir"
