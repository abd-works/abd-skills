---
scanner: war-room-shape
---

# Rule: Kanban ticket — one column; stage flow IP → Review → Done

War room progress for **runs** (work tickets) follows a Kanban board. See [`../../../content/kanban.md`](../../../content/kanban.md).

## DO

- Model each **run** as one **ticket** in **`board.json`** with a single **`column`** at a time.
- Use columns: **`backlog`** (not-started runs only), **`in_progress`**, **`review`**, **`done`**, **`blocked`**, **`stalled`**.
- Cycle each **stage** on a ticket: **in_progress → review → done** (executor slot → reviewer slot → stage exit).
- Leave ticket in **`done`** after stage exit until the **next stage** can start; then set **`in_progress`** on that stage — **not** backlog, **not** ready.
- Pull the next run ticket from **`backlog`** when cross-run `depends_on` allows (prior run **specification exit**, not engineering exit).
- Run **`sync_kanban_board.py`** after slot finish, block, claim aging, or stage gate — **delivery-lead** after checklist sync. **Kanban UI does not run sync.**
- Map executor claim → **`in_progress`**; reviewer claim → **`review`**; stage gate → **`done`**.
- **Kanban UI** may write **`wip-policy.json` only** (operator +/− to add/remove role agents). No other war-room writes from Kanban.

## DO NOT

- Put one ticket in multiple columns at once (no per-stage column map on a single ticket).
- Add a **Ready** column or a per-stage **backlog** after the run has left engagement backlog.
- Move a ticket to the next stage's backlog while waiting — **done** holds until next stage pulls to **in_progress**.
- Treat `depends_on` slot scanning as the board — **`board.json`** is the snapshot; slots are card detail.
- Use **`sync_kanban_board.py`** to author **`agile-delivery-plan.md`**, **`run-catalog.json`**, **`system-of-work.json`**, or **`slot-NN-start.md`** — those are **delivery-lead** + **`abd-delivery-planning`** + **`generate_run_slots.py`**.

## Example (wrong)

```json
"tickets": {
  "6": {
    "stages": {
      "exploration": { "column": "in_progress" },
      "specification": { "column": "backlog" }
    }
  }
}
```

One ticket, multiple stage columns — not this model.

## Example (correct)

```json
"tickets": {
  "5": { "run": 5, "stage": "engineering", "column": "review", "active_slot": "116" },
  "6": { "run": 6, "stage": "exploration", "column": "in_progress", "active_slot": "119" },
  "backlog": [{ "run": 7, "priority": 1 }]
}
```

Run 6 exploration finished → `"column": "done", "stage": "exploration"` until specification slot 127 deps met → `"column": "in_progress", "stage": "specification"`.
