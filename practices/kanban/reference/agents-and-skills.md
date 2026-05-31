# Agents and Skills — Concepts

## Skill progress

Per-skill execution and review state created on a ticket when an agent starts work — lazily populated, never pre-populated.

### Skill status flow

Each skill within a ticket follows: **not_started → in_progress → done**

Each skill also has a review cycle: **review_status: null → in_progress → done** (or **failed** → rework)

A ticket's stage is **done** when ALL skills defined in the kanban board for that stage have a `skill_progress` entry with `execution_status: done` AND `review_status: done`.

## Agents

Four **delivery roles** — one **executor session** per role (configurable count on `team`). Each executor **pulls** skills from active tickets across **all stages** and executes **and** reviews in one pass. See [../agents/reference/pull-model.md](../agents/reference/pull-model.md).

- **product-owner**
- **business-expert**
- **ux-designer**
- **engineer**

An agent starts work when the pull scan finds an eligible skill:

1. Walk the ticket's stage skill list from `kanban.json` — find the **next** skill whose prior skills all have `execution_status: done` **AND** `review_status: done`
2. That skill's `role` matches the agent's **delivery role**
3. The skill is unclaimed (`not_started` or no `skill_progress` entry)
4. Scan **all stages** on all active tickets; downstream stage wins (reverse order from `kanban.json`)

## Progress authority

- **kanban board** — `board.json`; updated by `sync_kanban_board.py` (from ticket state)
- **Board stage configuration, strategy, and team** — `kanban.json`; written by kanban lead at setup
- **Ticket state** — `board.json` tickets array; updated by agents (skill progress) + kanban lead (scatter, stage transitions)
- **Metrics** — `board.json` metrics + `metrics-log.jsonl`; updated by `track_metrics.py`
- **Audit trail** — `metrics-log.jsonl`; written by kanban lead

## Workspace layout

```text
<workspace>/docs/
  end-to-end/
    shaping/ · discovery/ · exploration/ · specification/ · engineering/
  increments/
    <n>-<slug>/
      exploration/ · specification/ · engineering/
  planning/delivery-war-room/
```

**Canonical artifact paths:** [artifact-layout.md](artifact-layout.md)

## Kanban lead — setup

After strategy selection:

1. Create `<workspace>/docs/planning/delivery-war-room/` if missing.
2. Create `<workspace>/docs/end-to-end/{shaping,discovery,exploration,specification,engineering}/` and `<workspace>/docs/increments/` if missing.
3. Copy **`templates/INSTRUCTIONS.md`** → `INSTRUCTIONS.md`.
4. Write **`kanban.json`** from strategy (or custom) — stages, stage work required, strategy (scatter rules, checkpoint policy, autonomy), and team.
5. Initialize **`board.json`** with first ticket (scope: all, stage: shaping).
6. Initialize `metrics-log.jsonl`.
7. **Arm the tick loop** per [../agents/reference/session-bootstrap.md](../agents/reference/session-bootstrap.md) — **before** the first scan cycle.

## Kanban lead — scan cycle

**Prerequisite:** Tick loop armed with `notify_on_output` (see session-bootstrap.md). One scan cycle per tick; do not exit after scan cycle 1.

Each tick:

1. Read `board.json` and `kanban.json` — tickets, backlog, team configuration, stage skill definitions.
2. **Detect completed skills** — compare each in-progress ticket's `skill_progress` against the stage's skill list in `kanban.json`.
3. **Stage transitions** — if all required skills are done on a ticket, either scatter or advance to next stage (clear skill progress).
4. **Scatter** — run `scatter_ticket.py` when scope changes; archive ticket, create children in backlog.
5. **Pull from backlog** — move next-priority tickets from backlog to active (respecting team configuration).
6. **Bottleneck analysis** — which stage/skill has the most waiting work? Report to operator.
7. **Agent pool** — spawn/scale agents per team configuration.
8. **Sync** — write `board.json`, append `metrics-log.jsonl`.

## Agent — work cycle

1. Read `board.json` and `kanban.json`.
2. For each ticket, walk the stage's ordered skill list in `kanban.json` — find the **next** skill whose prior skills all have `execution_status: done` AND `review_status: done`, and whose `role` matches your delivery role.
3. **Priority**: rightmost stage first (engineering > spec > explore > discovery > shaping).
4. Start work: write a `skill_progress` entry on the ticket (`execution_status: in_progress`, `agent: <role>`, `start: <now>`).
5. Execute the practice skill per executor or reviewer workflow.
6. Mark done (`execution_status: done`, `end: <now>`).
7. Pull next eligible skill.
