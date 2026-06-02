# Kanban E2E fixtures

| Fixture | Purpose | Planning root |
| --- | --- | --- |
| **pawplace-mini** | Real skill execution — one increment, full rails | `tests/e2e/data/pawplace-mini/docs/planning` |
| **pawplace-stubs** | **Fixture mode** — agents copy pre-baked outputs, mark done immediately | `tests/e2e/data/pawplace-stubs/docs/planning` |

## Reset from seed

```powershell
cd practices/kanban/apps/abd-delivery-agent-kanban
.\scripts\reset-e2e-fixture.ps1 -Fixture pawplace-stubs   # default — fast UI / handoff testing
.\scripts\reset-e2e-fixture.ps1 -Fixture pawplace-mini    # real agent runs
```

## Playwright profiles

| npm script | Config | Fixture |
| --- | --- | --- |
| `npm run test:e2e` | `playwright.config.mjs` | **pawplace-stubs** (resets seed first) |
| `npm run test:e2e:mini` | `playwright.mini.config.mjs` | pawplace-mini |

Board UI and API default to **pawplace-stubs** via `config.default.json`.

## pawplace-stubs — fixture mode

- `CONTEXT.md` — `fixture_mode: true`
- `skill-fixtures.json` — maps every kanban skill → source files → artifact paths
- `skill-fixtures/` — minimal valid examples (story map, increments, AC, domain, UX, architecture, CRC, spec, engineering)
- Content trimmed from `abd-pet-store-demo/docs` Increment 1

Agents read `practices/kanban/agents/reference/skill-fixture-mode.md` and **do not** execute practice skills.

Point the board UI at the stubs planning root to watch fast handoffs:

```text
tests/e2e/data/pawplace-stubs/docs/planning
```

## Full stack (board + agents)

The board **displays** `board.json`; it does **not** run skills or advance tickets by itself. For handoff testing you need **Cursor agents** too.

### 1. Reset fixture + board UI

```powershell
cd C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban
.\scripts\reset-e2e-fixture.ps1 -Fixture pawplace-stubs
.\scripts\restart.ps1
```

Open http://localhost:3000/board — confirm planning folder ends in `pawplace-stubs/docs/planning`.

### 2. Start kanban-lead (new Cursor chat)

Use agent **`kanban-lead`** with this workspace (engagement **root**, not `docs/planning`):

```text
C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-stubs
```

Paste into the lead chat:

```text
workspace: C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-stubs

FIXTURE MODE: CONTEXT.md has fixture_mode: true. Role agents must read
practices/kanban/agents/reference/skill-fixture-mode.md — copy skill-fixtures
and mark skills done; do not run practice skills.

War room already exists at docs/planning/kanban/. Skip strategy setup — run
scan cycle 1, spawn executors for eligible skills, stay alive on 5s tick loop.
Board UI is already running at http://localhost:3000/board.
```

The lead spawns **product-owner**, **business-expert**, **ux-designer**, and **engineer** subagents as skills become eligible.

### 3. Watch the board

- Skill chips turn done as executors copy fixtures (seconds, not minutes).
- Click the **Kanban Lead** heartbeat pill if it shows inactive (runs `lead-scan` on the API).
- In **Manual** mode you can drag tickets between stage columns; lead still scatters on stage completion.

### UI-only testing

`npm run test:e2e` — Playwright smoke tests (board loads, no agents).

### Real skill runs

Use `pawplace-mini` fixture and omit the FIXTURE MODE block — agents run full practice skills.
