# Bootstrap kanban-lead after reset — cycle 1 + REARM instructions for Cursor agent.

param(
    [ValidateSet('pawplace-mini', 'pawplace-stubs')]
    [string]$Fixture = 'pawplace-stubs'
)

$ErrorActionPreference = 'Stop'
$appRoot = Split-Path -Parent $PSScriptRoot
$workspace = Join-Path $appRoot "tests/e2e/data/$Fixture"
$planningRoot = Join-Path $workspace 'docs/planning'
$kanbanDir = Join-Path $planningRoot 'kanban'
$kanbanPracticeRoot = (Resolve-Path (Join-Path $appRoot '..\..')).Path
$tickScript = Join-Path $kanbanPracticeRoot 'skills/abd-kanban/scripts/kanban_cli.py lead tick'
$fixtureMode = $Fixture -eq 'pawplace-stubs'

if (-not (Test-Path $workspace)) {
    throw "Fixture workspace missing - run reset-e2e-fixture.ps1 first: $workspace"
}

$now = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssK')

if (Test-Path $kanbanDir) {
    Get-ChildItem -Path $kanbanDir -Filter 'heartbeat-*.json' -ErrorAction SilentlyContinue | Remove-Item -Force
    @(
        'executor-spawns.json',
        'lead-session.json',
        'lead-cursor-session.json',
        'metrics-log.jsonl',
        'REARM-INSTRUCTIONS.md'
    ) | ForEach-Object {
        $p = Join-Path $kanbanDir $_
        if (Test-Path $p) { Remove-Item -Force $p }
    }
}

Write-Host 'Running kanban-lead cycle 1...'
$reportJson = python $tickScript --workspace $workspace --json | Out-String
$report = $reportJson | ConvertFrom-Json

$spawnLines = @()
if ($report.spawns) {
    foreach ($s in $report.spawns) {
        $spawnLines += "- $($s.role) instance $($s.instance) ($($s.reason))"
    }
}
if ($spawnLines.Count -eq 0) {
    $spawnLines += '- (none yet - wait for operator drops on board)'
}
$spawnSummary = $spawnLines -join [Environment]::NewLine

$fixtureBlock = if ($fixtureMode) {
    @(
        'FIXTURE MODE + MANUAL BOARD:',
        '- CONTEXT.md has fixture_mode: true',
        '- Operator drops role agents on tickets; action-state gets intents only (no in_progress on drop)',
        '- Spawn executors when lead tick reports must_spawn after a drop',
        '- Executors: kanban_cli.py member intent then kanban_cli.py member fixture',
        '- Do NOT spawn pull-loop executors proactively after reset'
    ) -join [Environment]::NewLine
} else {
    @(
        'AUTOMATIC BOARD (pawplace-mini):',
        '- Spawn executors when must_spawn is true',
        '- Executors pull via kanban_cli.py\ member pull'
    ) -join [Environment]::NewLine
}

$skillFixtureLine = if ($fixtureMode) { '- practices/kanban/agents/reference/skill-fixture-mode.md' } else { '' }

$kanbanLeadPromptLines = @(
    "You are kanban-lead for $Fixture E2E. Fresh reset - lead cycle $($report.cycle) already ran from rearm-delivery-team.ps1.",
    '',
    'Read FIRST:',
    '- practices/kanban/agents/kanban-lead/AGENT.md',
    '- practices/kanban/agents/reference/session-bootstrap.md'
)
if ($skillFixtureLine) { $kanbanLeadPromptLines += $skillFixtureLine }
$kanbanLeadPromptLines += @(
    '',
    "workspace: $workspace",
    "planning root: $planningRoot",
    "board_mode: $($report.board_mode)",
    'Board UI: http://localhost:3000/board',
    '',
    $fixtureBlock,
    '',
    'Turn 1 (mandatory - do not exit after):',
    '1. Arm AGENT_LOOP_TICK_kanban_lead (5s, block_until_ms:0, notify_on_output ^AGENT_LOOP_TICK_kanban_lead)',
    "2. python practices/kanban/skills/abd-kanban/scripts/kanban_cli.py lead tick --workspace $workspace --json",
    '3. If must_spawn - Task-spawn EVERY spawn_prompts entry (run_in_background: true)',
    '4. Update docs/planning/kanban/heartbeat-kanban-lead.json and lead-cursor-session.json',
    '5. Stay alive on ticks - run lead tick first on every wake, then spawn if needed',
    '',
    "Current tick: must_spawn=$($report.must_spawn)",
    'Pending spawns from last tick:',
    $spawnSummary
)
$kanbanLeadPromptText = $kanbanLeadPromptLines -join [Environment]::NewLine
$fence = ([char]96).ToString() * 3

$operatorInstructions = @(
    '# Rearm delivery team (paste to Cursor operator agent)',
    '',
    "E2E fixture **$Fixture** was reset. Agent loops were killed. Lead cycle $($report.cycle) ran on disk.",
    '',
    '## Operator agent - do this now',
    '',
    '1. **Task-spawn kanban-lead** (run_in_background: true) using the **Kanban lead prompt** below.',
    '2. **Do not** spawn PO / BE / UX / engineer unless lead tick reports must_spawn after an operator drop.',
    '3. Tell the user to **close stale** kanban-lead and executor agent chats from before this reset.',
    "4. Board: http://localhost:3000/board (planning root: ``$planningRoot``)",
    '',
    '## Kanban lead prompt (Task subagent)',
    '',
    "${fence}text",
    $kanbanLeadPromptText,
    $fence,
    '',
    '## Last lead tick summary',
    '',
    '| Field | Value |',
    '| --- | --- |',
    "| cycle | $($report.cycle) |",
    "| board_mode | $($report.board_mode) |",
    "| must_spawn | $($report.must_spawn) |",
    "| active_tickets | $($report.active_tickets) |",
    '',
    '### Spawns',
    $spawnSummary,
    '',
    '---',
    "Generated: $now"
) -join [Environment]::NewLine

$session = @{
    mode        = 'awaiting_cursor_agent'
    armed_at    = $now
    workspace   = $workspace
    fixture     = $Fixture
    board_mode  = $report.board_mode
    cycle       = $report.cycle
    must_spawn  = [bool]$report.must_spawn
    spawn_count = @($report.spawns).Count
    rearm_file  = 'REARM-INSTRUCTIONS.md'
} | ConvertTo-Json -Depth 4

$session | Set-Content -Path (Join-Path $kanbanDir 'lead-cursor-session.json') -Encoding utf8

@{
    agent  = 'kanban-lead'
    status = 'working'
    ts     = $now
    detail = "rearm-delivery-team cycle $($report.cycle); must_spawn=$($report.must_spawn)"
} | ConvertTo-Json | Set-Content -Path (Join-Path $kanbanDir 'heartbeat-kanban-lead.json') -Encoding utf8

$operatorInstructions | Set-Content -Path (Join-Path $kanbanDir 'REARM-INSTRUCTIONS.md') -Encoding utf8

Write-Host ''
Write-Host "Kanban lead cycle $($report.cycle) complete (board_mode=$($report.board_mode), must_spawn=$($report.must_spawn))."
Write-Host "Wrote: $kanbanDir\REARM-INSTRUCTIONS.md"
Write-Host ''
Write-Host '<<<REARM_INSTRUCTIONS_FOR_CURSOR_AGENT>>>'
Write-Host $operatorInstructions
Write-Host '<<<END_REARM_INSTRUCTIONS>>>'
