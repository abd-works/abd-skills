# Restart the abd-delivery-agent-kanban dev server
# Kills anything on ports 3000 (client) and 3001 (API), then starts fresh.
#
# Usage:
#   .\scripts\restart.ps1

param(
    [int]$ApiPort = 3001,
    [int]$ClientPort = 3000
)

Set-Location "$PSScriptRoot\.."

function Stop-Port {
    param([int]$Port)
    $pids = netstat -ano | Select-String ":$Port\s" | ForEach-Object {
        ($_ -split '\s+')[-1]
    } | Where-Object { $_ -match '^\d+$' } | Sort-Object -Unique
    foreach ($p in $pids) {
        try {
            Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
            Write-Host "  Killed PID $p (port $Port)" -ForegroundColor DarkYellow
        } catch {}
    }
}

Write-Host "Stopping processes on ports $ClientPort and $ApiPort..." -ForegroundColor Cyan
Stop-Port $ApiPort
Stop-Port $ClientPort
Start-Sleep -Milliseconds 800

$env:PORT = $ApiPort
$env:VITE_PORT = $ClientPort

Write-Host ""
Write-Host "Restarting abd-delivery-agent-kanban" -ForegroundColor Green
Write-Host "  API   -> http://localhost:$ApiPort" -ForegroundColor Yellow
Write-Host "  Board -> http://localhost:$ClientPort/board" -ForegroundColor Yellow
Write-Host ""

npm run dev
