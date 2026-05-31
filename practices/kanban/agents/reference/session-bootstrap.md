# Session bootstrap — mandatory first turn

**Every kanban agent reads this file on turn 1 before any board work, scan cycle, or skill execution.**

Also read **[pull-model.md](pull-model.md)** — all stages, all roles, continuous pull.

A tick shell without `notify_on_output`, or a single scan cycle with no loop, leaves the board frozen. **Infrastructure first — orchestration second — deliverables last.**

---

## Resolve paths (all agents)

| Item | Path |
| --- | --- |
| War room | `<workspace>/docs/planning/delivery-war-room/` |
| Artifact layout | [artifact-layout.md](../../reference/artifact-layout.md) — read before every write |
| Shaping | `<workspace>/docs/end-to-end/shaping/` |
| Discovery | `<workspace>/docs/end-to-end/discovery/{domain,stories,ux,architecture}/` |
| Increment (active) | `<workspace>/docs/increments/<n>-<slug>/{exploration,specification,engineering}/` — exploration uses same four subfolders as end-to-end |
| Roll-up | Merge increment stage → `docs/end-to-end/<same-stage>/` |
| Board | `.../board.json` |
| Stage config | `.../kanban.json` |
| Metrics | `.../metrics-log.jsonl` |
| Heartbeat | `.../heartbeat-<role>.json` (team members; optional instance suffix e.g. `be2`) |
| Draw.io (background) | [drawio-sync-background.md](drawio-sync-background.md) — queued after story/domain skills; non-blocking |

If `workspace` is missing from bootstrap → ask once and **stop**. Do not guess paths.

---

## Kanban lead — board UI (turn 1, kanban lead only)

**After** `workspace` is resolved and **before** Step 1 strategy or tick-loop wiring, use the **AskQuestion** tool — do not ask only in chat prose.

| Field | Value |
| --- | --- |
| **id** | `start-board-ui` |
| **prompt** | Start the kanban board UI in the IDE to watch delivery progress? |
| **options** | **Yes** — start board UI · **No** — orchestrate from files only · **Already running** |

### If **Yes**

1. **Resolve board app root** — `practices/kanban/apps/abd-delivery-agent-kanban` under the agilebydesign-skills repo (typical: `C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban`). If missing, glob `**/abd-delivery-agent-kanban/scripts/restart.ps1` from `C:/dev`.
2. **Check terminals** — if `restart.ps1` or `npm run dev` is already running from that app root and http://localhost:3000/board responds, skip start; tell operator the URL and planning root.
3. **Port conflict** — board uses **3000** (client) and **3001** (API). If another app (e.g. engagement `npm run dev`) already owns 3000, warn the operator before `restart.ps1` (it kills processes on those ports).
4. **Start in IDE** — from board app root, run once if needed: `npm install`. Then Shell **background**: `.\scripts\restart.ps1` with `block_until_ms: 0` (see [kanban-board.md](../../reference/kanban-board.md)).
5. **Open board** — tell operator to open **http://localhost:3000/board** (Cursor Simple Browser or external browser). **Planning root:** `<workspace>/docs/planning` (war room lives under `delivery-war-room/`).
6. If war room exists, append `{ "event": "board_ui_started", "ts": "<iso>", "planning_root": "<workspace>/docs/planning" }` to `metrics-log.jsonl`.

### If **No**

Continue orchestration; board state remains in `board.json` only.

### If **Already running**

Confirm URL and planning root; continue orchestration.

---

## Kanban lead — arm the tick loop **before** Step 3

**DO NOT** read the board for orchestration, spawn role agents, or declare scan complete until the loop below is armed **and** wired to wake this session.

### 1. Check for an existing loop

Search running terminals for `AGENT_LOOP_TICK_kanban_lead`. If one is running **and** was started with `notify_on_output` in **this** session, reuse its `shell_id`. If a loop runs but nothing wakes on tick → treat as **not armed**; start a new one with `notify_on_output`.

### 2. Start the loop (PowerShell — run directly, not nested)

**DO NOT** wrap in `powershell -Command "while ($true) ..."` — nested `-Command` breaks `$true` on Windows and the loop dies immediately.

```powershell
while ($true) { Start-Sleep -Seconds 30; Write-Output 'AGENT_LOOP_TICK_kanban_lead {"prompt":"Scan cycle: read board, advance tickets, manage agents."}' }
```

Shell tool parameters:

- `block_until_ms: 0` (background)
- `notify_on_output`: pattern `^AGENT_LOOP_TICK_kanban_lead`, reason `Kanban lead scan tick`

### 3. Smoke-check

Await the first tick (~35s) to confirm the loop is alive.

### 4. Run scan cycle immediately

Perform **one** full Step 3 scan cycle (read board → advance → pull → spawn → log) **now**, without waiting for the first tick.

### 5. End of **every** turn — do not exit the engagement

- Update `heartbeat-kanban-lead.json` with fresh `ts` and `status: working`.
- Confirm in chat: loop `shell_id`, that scan cycle N completed, and that **the next tick** will wake the next scan.
- **DO NOT** say "I'll continue when agents report back" and stop — the tick loop is the wake signal.
- **DO NOT** finish turn after scan cycle 1 only.

### Subagent / Task spawn rules

| Pattern | Rule |
| --- | --- |
| Lead in **main chat** | Arm loop in main session; ticks wake main agent. **Preferred.** |
| Lead as **Task subagent** | Subagent **must** arm loop in its own turn 1 with `notify_on_output`. Parent **must not** spawn `run_in_background: true` lead without loop wiring in the same turn. |
| Parent spawns lead | Parent arms loop first, then spawns lead with: "Loop armed — perform scan cycle; end turn waiting for next tick." |
| Parent only starts loop | **Broken** — ticking shell with no agent listening. Never do this alone. |

### Stop

Kill the loop shell PID when all tickets are archived or the operator says stop.

---

## Delivery role agents — turn 1 (continuous pull)

**Arm the pull loop first**, then scan:

1. Read [work-queue.md](work-queue.md) and [pull-model.md](pull-model.md).
2. Write or refresh `heartbeat-<role>.json` with `status: working` and current ISO `ts`.
3. Read `board.json` and `kanban.json`.
4. **Arm `AGENT_LOOP_TICK_<role>`** (see below) — **before** first pull scan.
5. Run pull scan immediately (all stages, downstream first per `kanban.json`).

If eligible work → [executor-workflow.md](executor-workflow.md) Step 1.

If **no** eligible work → signal `agent_ready`, heartbeat `status: ready`, **keep pull loop armed**. Do not exit.

---

## Pull loop (delivery roles — always on)

Arm on **turn 1**. Keep running across skills and idle periods. Kill only when operator says stop or engagement complete.

```powershell
while ($true) { Start-Sleep -Seconds 30; Write-Output 'AGENT_LOOP_TICK_<role> {"prompt":"Pull: scan all active tickets all stages (downstream first per kanban.json); claim eligible skill or refresh agent_ready."}' }
```

Replace `<role>` with `business-expert`, `product-owner`, `ux-designer`, or `engineer`.

- `block_until_ms: 0`
- `notify_on_output`: pattern `^AGENT_LOOP_TICK_<role>`

On each tick: pull scan per pull-model.md → work → execute → pull again. No work → refresh heartbeat, stay in loop.

**DO NOT** pull tickets from `backlog` to `active` yourself.

---

## Idle poll loop (deprecated name — same as pull loop above)

The pull loop **is** the idle poll loop. Do not use a separate loop only when idle.

---

## Spawning role agents (kanban lead)

Every spawn prompt **must** include:

```text
Read practices/kanban/agents/reference/session-bootstrap.md FIRST.

Bootstrap:
  workspace: <absolute-path>
  delivery-role: <role>

Then read agents/<role>/AGENT.md, agents/reference/pull-model.md, agents/reference/work-queue.md, and reference/artifact-layout.md.
Arm AGENT_LOOP_TICK_<role> pull loop on turn 1. Pull eligible skills — all stages — execute and review per executor-workflow.md.
Write artifacts only to paths in artifact-layout.md. Never exit after one skill. Never spawn *-reviewer agents.
```

Spawn with `run_in_background: true` only when the role agent will arm its own idle poll loop per above.

---

## Common failures (DO NOT)

| Wrong | Why it breaks |
| --- | --- |
| Scan cycle 1 then exit | No conductor for cycle 2+ |
| Loop shell without `notify_on_output` | Ticks go to a log file; no agent wakes |
| Nested `powershell -Command while ($true)` | `$true` stripped; loop never runs |
| Heartbeat file without live session | Board shows stale liveness |
| `run_in_background` lead with no loop | One-shot subagent dies after one turn |
