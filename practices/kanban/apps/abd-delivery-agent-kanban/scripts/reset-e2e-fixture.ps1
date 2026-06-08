# Reset E2E fixture workspace from _seed

param(
    [ValidateSet('pawplace-mini', 'pawplace-stubs')]
    [string]$Fixture = 'pawplace-stubs'
)

$ErrorActionPreference = 'Stop'
$appRoot = Split-Path -Parent $PSScriptRoot
$seed = Join-Path $appRoot "tests/e2e/_seed/$Fixture"
$data = Join-Path $appRoot "tests/e2e/data/$Fixture"

if (-not (Test-Path $seed)) {
    throw "Seed not found: $seed"
}

if (Test-Path $data) {
    Remove-Item -Recurse -Force $data
}

Copy-Item -Recurse $seed $data

# Runtime session files must never survive reset — they create ghost "live" agents.
$kanbanDir = Join-Path $data "docs/planning/kanban"
if (Test-Path $kanbanDir) {
    Get-ChildItem -Path $kanbanDir -Filter 'heartbeat-*.json' -ErrorAction SilentlyContinue | Remove-Item -Force
    @('executor-spawns.json', 'lead-session.json', 'lead-cursor-session.json') | ForEach-Object {
        $p = Join-Path $kanbanDir $_
        if (Test-Path $p) { Remove-Item -Force $p }
    }
}

Write-Host "Reset $Fixture -> $data"
Write-Host "Planning root: $data/docs/planning"
