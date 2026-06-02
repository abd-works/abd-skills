# War room — PawPlace stubs (fixture mode)



**Workspace:** `tests/e2e/data/pawplace-stubs`



## Fixture mode



**`fixture_mode: true`** — read `<workspace>/AGENT-SEED.md` and `<workspace>/skill-fixtures.json`.



**Team member agents** (`product-owner`, `business-expert`, `ux-designer`, `engineer`) apply harness data — kanban-lead does not. After pull or manual drop, run `apply_skill_fixture.py`. See `practices/kanban/agents/reference/skill-fixture-mode.md`.



## Manual handoff test



1. Reset: `scripts/reset-e2e-fixture.ps1 -Fixture pawplace-stubs`

2. Board UI → **Use stubs** (or confirm planning root points at `tests/e2e/data/pawplace-stubs`)

3. Drop a role + skill onto ticket `project-all` (Manual mode)

4. Run kanban-lead tick OR spawn the role agent using `EXECUTOR-PROMPT.md`

5. **Team member agent** runs `apply_skill_fixture.py apply-claim` (or `apply` after `board_skill.py pull`)

6. Board shows skill done; artifacts appear under `docs/`



## Scope



Three modules, four increments (two in Product Catalog). Full skill rails on increment 1 of module 1. Examples trimmed from `abd-pet-store-demo/docs` Increment 1.

**Scatter path:** `project-all` (shaping done) → 3 partition tickets → thin-slicing → increment tickets per module.



## War room paths



| File | Purpose |

| --- | --- |

| `board.json` | Tickets, skill_progress |

| `kanban.json` | Stages, stage work required, team |

| `action-state.json` | Manual drop intents |

| `metrics-log.jsonl` | Events |



Initial ticket: `project-all` in **shaping** (scope: all).



Reset live data: `scripts/reset-e2e-fixture.ps1 -Fixture pawplace-stubs`

