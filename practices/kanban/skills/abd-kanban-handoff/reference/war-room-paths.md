# War room path resolution

Resolve `<workspace>` first (`get_workspace.py` or user).

## War room directory (first match)

1. `<workspace>/docs/planning/kanban/`
2. `<workspace>/docs/planning/delivery-war-room/`

Same rule as `war_room_dir()` in [../abd-kanban/scripts/delivery_model.py](../abd-kanban/scripts/delivery_model.py).

## Files

| File | Path |
| --- | --- |
| Board state | `<war-room>/board.json` |
| Stage configuration | `<war-room>/kanban.json` (or `system-of-work.json`) |
| Metrics | `<war-room>/metrics-log.jsonl` |
| Agent bootstrap | `<war-room>/INSTRUCTIONS.md` |

## Manual mode (delivery board app)

Planning root is often `<workspace>/docs/planning`:

- `action-state.json` — pending drop intents
- Board may symlink or duplicate under `kanban/` for the UI seed

## Handoff documents

| File | Path |
| --- | --- |
| Dated resume | `<workspace>/docs/planning/handoffs/handoff-abd-kanban-<slug>-<YYYY-MM-DD>.md` |
| Latest (overwrite) | `<workspace>/docs/planning/handoffs/handoff-latest.md` |

Produced by **`abd-kanban-handoff`** (`/abd-kanban-handoff`). Not in OS temp — lives with planning artifacts.

## Delivery docs (always under workspace)

- `docs/end-to-end/<stage>/`
- `docs/increments/<n>-<slug>/`

See [../../reference/artifact-layout.md](../../reference/artifact-layout.md).
