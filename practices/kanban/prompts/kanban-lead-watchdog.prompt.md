# Kanban lead watchdog (parent chat)

Run in the **operator / parent** chat while kanban-lead runs as a **Task subagent**.

Ticks on the lead only work while that subagent session is **alive and listening**. Assign on the board does **not** spawn executors by itself.

## Arm once per engagement

```text
/loop 5s Kanban lead watchdog for <workspace>: run check_lead_wake.py --json --apply-tick. If wake_lead and cursor_agent_id in lead-cursor-session.json, Task resume that id (interrupt if running) with: run lead tick, spawn all must_spawn, re-arm 5s lead tick loop, stay alive. Never spawn role agents from parent — only resume kanban-lead.
```

Replace `<workspace>` with the engagement root (folder above `docs/planning`).

## Scripts

```powershell
python practices/kanban/skills/abd-kanban/scripts/check_lead_wake.py --workspace "<workspace>" --json --apply-tick
```

## lead-cursor-session.json

`docs/planning/kanban/lead-cursor-session.json` — parent or lead updates `cursor_agent_id` after each lead spawn/resume.
