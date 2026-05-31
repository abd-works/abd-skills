# Reset PawPlace mini E2E workspace
# Copies immutable seed to tests/e2e/data/pawplace-mini/
# Removes war-room state and docs written during a manual run.

param(
    [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Seed = (Resolve-Path (Join-Path $ScriptDir (Join-Path '..' (Join-Path '_seed' 'pawplace-mini')))).Path
$DestParent = Join-Path $ScriptDir (Join-Path '..' 'data')
$Dest = Join-Path $DestParent 'pawplace-mini'

Write-Host "Seed: $Seed"
Write-Host "Dest: $Dest"

if ($WhatIf) {
    Write-Host 'WhatIf: would remove and recopy' -ForegroundColor Yellow
    exit 0
}

if (Test-Path $Dest) {
    Remove-Item -LiteralPath $Dest -Recurse -Force
}

New-Item -ItemType Directory -Force -Path (Split-Path $Dest) | Out-Null
Copy-Item -LiteralPath $Seed -Destination $Dest -Recurse -Force

$KanbanDir = Join-Path $Dest "docs\planning\kanban"
$WarRoomLink = Join-Path $Dest "docs\planning\delivery-war-room"
if (Test-Path $WarRoomLink) {
    cmd /c "rmdir `"$WarRoomLink`"" 2>$null | Out-Null
}
if (Test-Path $KanbanDir) {
    cmd /c "mklink /J `"$WarRoomLink`" `"$KanbanDir`"" | Out-Null
    Write-Host "Linked delivery-war-room -> kanban (agent compatibility)" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "PawPlace mini reset complete." -ForegroundColor Green
Write-Host ""
Write-Host "Workspace (kanban-lead):" -ForegroundColor Cyan
Write-Host "  $Dest"
Write-Host ""
Write-Host "Planning root (board UI):" -ForegroundColor Cyan
Write-Host "  $Dest\docs\planning"
Write-Host ""
Write-Host "Next: run kanban-lead with workspace above (Step 1 strategy, Step 2 war room)." -ForegroundColor Yellow
