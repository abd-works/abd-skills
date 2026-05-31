# E2E manual fixtures

Tiny engagement workspaces for manual kanban-lead + board UI runs. **No automated tests** — reset, point the board, run agents by hand.

## PawPlace mini

| | |
| --- | --- |
| **Workspace** | `tests/e2e/data/pawplace-mini/` |
| **Planning root** (board UI) | `…/pawplace-mini/docs/planning` |
| **Scope** | 2 increments, 2–3 sprints each (see `thin-slicing.md`) |

### Reset to pristine seed

```powershell
.\tests\e2e\scripts\reset-pawplace-mini.ps1
```

### Board UI

1. Reset (above).
2. Start dev server: `.\scripts\restart.ps1`
3. Connect planning root (or set in UI):

   `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-mini\docs\planning`

   Board reads `docs/planning/kanban/board.json` — exists only **after** kanban-lead Step 2.

### Kanban lead (manual)

Open `@kanban-lead` with:

```text
workspace: C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-mini
context: Read CONTEXT.md and docs/end-to-end/discovery/stories/thin-slicing.md
strategy: default-new-build (or new-thin-slice — 2 increments only)
```

Step 1 → confirm strategy. Step 2 → war room under `docs/planning/kanban/` (board app path).

Seed state: war room under `docs/planning/kanban/` with `project-all` in **shaping** (kanban-lead Step 2 baseline). Re-run reset to restore.
