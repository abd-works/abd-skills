# Delivery Kanban — JIT ticket model

The Kanban board models delivery as **tickets flowing through stages**. State: `abd-kanban/board.json` (written by `sync_kanban_board.py` and kanban-lead scan cycle).

## Planning vs board sync

| Layer | Who | Writes |
| --- | --- | --- |
| **Strategy** | **kanban-lead** + **`abd-kanban-planning`** | `strategy.md` |
| **System of work** | **kanban-lead** + **`abd-kanban`** (Step 2) | `system-of-work.json`, `manifest.md` |
| **Board state** | **`sync_kanban_board.py`** + kanban-lead scan | `board.json` |
| **Scatter** | **`scatter_ticket.py`** (triggered by kanban-lead) | `board.json` (archive parent, create children) |
| **Metrics** | **`track_metrics.py`** | `metrics-log.jsonl` |

## Work ticket

One **ticket** = one unit of work at the scope defined by the system of work for its current stage.

- A ticket is in **exactly one list** at a time: `backlog`, `active`, `done`, or `archived`.
- Each ticket tracks **per-skill progress** (to_do, in_progress, done + review status).
- Tickets carry **lineage** (project > increment > sprint > story) for rollup.

## Board lists

| List | When |
| --- | --- |
| **`backlog`** | Ordered by priority; waiting for pull into active |
| **`active`** | At least one skill claimed (in_progress) by an agent |
| **`done`** | All skills complete; awaiting scatter or advance to next stage |
| **`archived`** | Scattered (children created) or final stage complete; carries full timing data |

## Skill progress (per ticket, per stage)

Each skill within a ticket follows:

```text
to_do  →  in_progress  →  done
                              │
                    review_status: null → in_progress → done
                                                    │
                                              (or failed → rework)
```

A ticket's stage is **done** when ALL skills have `status: done` AND `review_status: done`.

## Scattering

When a done ticket's next stage has **finer scope**, it scatters:

- Parent moves to `archived` with timing data
- Children enter `backlog` at the finer scope level
- Children carry lineage from parent

| Transition | Scatter source |
| --- | --- |
| Shaping (all) → Discovery (increment) | Thin-slicing increments |
| Exploration (increment) → Specification (sprint) | Stories grouped into sprints |

## Multiple tickets in flight

Multiple active tickets across stages is normal:

```text
inc-1 ticket:  active  (engineering, sprint-1)
inc-2 ticket:  active  (exploration)
inc-3 ticket:  backlog (waiting for exploration)
```

## Sync

**kanban-lead** scan cycle manages flow. Manual sync:

```bash
python kanban/skills/abd-kanban/scripts/sync_kanban_board.py --workspace <engagement-root>
```
