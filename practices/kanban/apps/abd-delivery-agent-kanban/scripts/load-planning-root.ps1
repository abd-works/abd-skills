# Load planningRoot from config.default.json into dev server env

param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot '..\config.default.json')
)

if (-not (Test-Path $ConfigPath)) {
    Write-Warning "config.default.json not found at $ConfigPath"
    return
}

$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$root = [string]$config.planningRoot
if (-not $root) {
    Write-Warning 'planningRoot missing in config.default.json'
    return
}

$env:PLANNING_ROOT = $root
$env:VITE_PLANNING_ROOT = $root
Write-Host "Planning root: $root" -ForegroundColor DarkGray
