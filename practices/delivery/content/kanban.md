# Delivery Kanban — war room model

The war room models delivery as a **Kanban board**. Progress snapshot: `delivery-war-room/board.json` (written **only** by `sync_kanban_board.py`).

## Planning vs board sync

| Layer | Who | Writes |
| --- | --- | --- |
| **Plan** | **delivery-lead** + **`abd-delivery-planning`** | `abd-delivery-lead/agile-delivery-plan.md` |
| **System of work + runs** | **delivery-lead** + **`abd-delivery-war-room`** (Step 2b) | `system-of-work.json`, `run-catalog.json`, `run-state.json`, `manifest.md` |
| **Slots (per run)** | **delivery-lead** + **`generate_run_slots.py`** when a run **opens** | `slot-NN-start.md` |
| **Board snapshot** | **`sync_kanban_board.py`** only | `board.json` |

The **Kanban UI** (`abd-delivery-agent-kanban`) **just reads** plan, catalog, checklist, slots, and `board.json`. Its **only write** is **`wip-policy.json`** when the operator adds or removes agents (+/−). **`sync_kanban_board.py`** is run by **delivery-lead** — not the Kanban app.

## Work ticket

One **run** from `run-catalog.json` = one **ticket** (increment scope, story list).

- A ticket is in **exactly one column** at a time.
- History lives in `slot-NN-finished.md` and `run-log.jsonl` — not duplicate columns.

## Columns

| Column | When |
| --- | --- |
| **`backlog`** | Run not yet on the board — ordered by plan priority; **only column that holds not-started runs** |
| **`in_progress`** | Active **executor** slot (claimed or next pullable executor work in current stage) |
| **`review`** | Active **reviewer** slot for the current stage |
| **`done`** | Current **stage exit** passed — ticket **stays here** until the **next stage** can start; then moves to **`in_progress`** (no Ready, no per-stage backlog) |
| **`blocked`** | `slot-NN-blocked.md` open on the ticket |
| **`stalled`** | Claim open longer than `manifest.md` `stall_timeout_minutes` without finish |

There is **no Ready** column. There is **no backlog** after a run leaves backlog — only **`backlog` → (board columns) → run complete**.

## Stage flow (per ticket, per stage)

Each bootcamp stage on a ticket cycles:

```text
in_progress  →  review  →  done
     ↑              │          │
     └── rework ────┘          └── wait in done until next stage → in_progress
```

Maps to slots:

| Column | Slot signal |
| --- | --- |
| `in_progress` | Executor `slot-NN-claim.md` or next claimable executor slot |
| `review` | Reviewer `slot-NN-claim.md` |
| `done` | Stage `stage_exit_gate` in `run-log.jsonl`; or all stage slots finished, gate pending |

## Multiple tickets in flight

Cross-run parallelism = **separate tickets**, each in one column:

```text
Run 5 ticket:  in_progress  (engineering)
Run 6 ticket:  in_progress  (exploration)   ← pulled from backlog when Run 5 spec done
```

See **`cross-run-upstream-parallelism.md`** for `depends_on` wiring.

## Sync

**delivery-lead** runs after slot/stage events (Kanban does not):

```bash
python delivery/skills/abd-delivery-war-room/scripts/sync_kanban_board.py --workspace <engagement-root>
```

The Kanban app polls the result — **read only**, except **agent +/−** → `wip-policy.json`. Plan, catalog, system of work, slots, and `board.json` come from **delivery-lead** + skills.
