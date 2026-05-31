# Start the abd-delivery-agent-kanban dev server
# API: http://localhost:3001   Board UI: http://localhost:3000
#
# Usage:
#   .\scripts\start.ps1
#   .\scripts\start.ps1 -Port 3001        # override API port
#   .\scripts\start.ps1 -ClientPort 3000  # override client port

param(
    [int]$Port = 3001,
    [int]$ClientPort = 3000
)

Set-Location "$PSScriptRoot\.."

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    npm install
}

$env:PORT = $Port
$env:VITE_PORT = $ClientPort

Write-Host ""
Write-Host "Starting abd-delivery-agent-kanban" -ForegroundColor Green
Write-Host "  API  -> http://localhost:$Port" -ForegroundColor Yellow
Write-Host "  Board -> http://localhost:$ClientPort" -ForegroundColor Yellow
Write-Host ""

npm run dev
