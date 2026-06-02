# Delivery Agent Kanban

Live Kanban board for **delivery-war-room** progress. **Read-only** — polls `board.json`, `kanban.json`, checklist, and ticket files from disk. Does **not** create planning artifacts; **kanban-lead** + skills own the plan, system of work, and board sync.

Part of the kanban practice package: `practices/kanban/apps/abd-delivery-agent-kanban/`.

## Quick start

```powershell
cd C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban
npm install
npm run dev
```

Open http://localhost:3000/board — default planning folder is `tests/e2e/data/pawplace-stubs/docs/planning` (fixture mode; see `config.default.json`).

Reset the live fixture workspace before testing:

```powershell
.\scripts\reset-e2e-fixture.ps1 -Fixture pawplace-stubs   # fast UI / handoff (default)
.\scripts\reset-e2e-fixture.ps1 -Fixture pawplace-mini    # real agent skill runs
```

E2E: `npm run test:e2e` (stubs) · `npm run test:e2e:mini` (mini profile).

## What it reads

| Source | Purpose |
| --- | --- |
| `delivery-war-room/board.json` | Ticket columns — **written by kanban-lead** (`sync_kanban_board.py`), **read here** |
| `delivery-war-room/kanban.json` | Stages, stage work required, team |
| `delivery-war-room/INSTRUCTIONS.md` | Agent bootstrap |
| `delivery-war-room/metrics-log.jsonl` | Agent-ready and pull events |

## What it writes

**Only one thing:** `delivery-war-room/wip-policy.json` — when the operator uses **+ / −** on the agent pool bar to add or remove role agents.

Everything else (plan, system of work, tickets, `board.json`) is **read only**. **kanban-lead** runs `sync_kanban_board.py` after stage events; the file watcher only invalidates the poll cache so the UI re-reads disk.

## Board rules

- **One ticket per scope unit** — exactly **one column** at a time per active ticket.
- **Stage flow** on each ticket: in progress → review → done; ticket stays in **stage done** between stages until picked up.
- **Backlog** holds not-started work; **complete** section shows finished tickets from `board.json`.
- Polls every 3s; **Refresh** re-reads disk.
- **+ / −** on agent avatars writes `wip-policy.json` only.
- Does **not** run `sync_kanban_board.py` or edit planning artifacts.

## Architecture

Domain-first MERN layout under `packages/delivery-board/` (`shared` · `server` · `client`). See `docs/domain/` for ubiquitous language and CRC.
