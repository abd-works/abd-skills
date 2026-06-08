# Stop all AGENT_LOOP_TICK PowerShell shells (kanban-lead + role executors).
# Safe to run anytime — idempotent.

$ErrorActionPreference = 'Continue'

function Stop-KanbanAgentLoopShells {
    $killed = [System.Collections.Generic.List[string]]::new()
    $seen = @{}

    foreach ($shellName in @('powershell.exe', 'pwsh.exe')) {
        $procs = Get-CimInstance Win32_Process -Filter "Name='$shellName'" -ErrorAction SilentlyContinue
        foreach ($p in $procs) {
            $cmd = $p.CommandLine
            if (-not $cmd -or $cmd -notmatch 'AGENT_LOOP_TICK') { continue }
            $id = [int]$p.ProcessId
            if ($seen[$id]) { continue }
            $role = 'agent'
            if ($cmd -match 'AGENT_LOOP_TICK_([a-z-]+)') { $role = $Matches[1] }
            if (Get-Process -Id $id -ErrorAction SilentlyContinue) {
                Stop-Process -Id $id -Force -ErrorAction SilentlyContinue
                $killed.Add("killed pid $id ($role) [process cmdline]")
            }
            $seen[$id] = $true
        }
    }

    $termGlobs = @(
        (Join-Path $env:USERPROFILE '.cursor\projects\c-dev-abd-pet-store-demo\terminals'),
        (Join-Path $env:USERPROFILE '.cursor\projects\c-dev-agilebydesign-skills\terminals')
    )
    foreach ($root in $termGlobs) {
        if (-not (Test-Path $root)) { continue }
        Get-ChildItem -Path $root -Filter '*.txt' -ErrorAction SilentlyContinue | ForEach-Object {
            $text = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
            if (-not $text -or $text -notmatch 'AGENT_LOOP_TICK') { return }
            if ($text -notmatch '(?m)^pid:\s*(\d+)') { return }
            $id = [int]$Matches[1]
            if ($seen[$id]) { return }
            $role = 'agent'
            if ($text -match 'AGENT_LOOP_TICK_([a-z-]+)') { $role = $Matches[1] }
            if (Get-Process -Id $id -ErrorAction SilentlyContinue) {
                Stop-Process -Id $id -Force -ErrorAction SilentlyContinue
                $killed.Add("killed pid $id ($role) [$($_.Name)]")
            }
            $seen[$id] = $true
        }
    }

    return $killed
}

$result = Stop-KanbanAgentLoopShells
if ($result.Count -eq 0) {
    Write-Host 'No AGENT_LOOP_TICK shells were running.'
} else {
    $result | ForEach-Object { Write-Host $_ }
    Write-Host "Stopped $($result.Count) agent loop shell(s)."
}
