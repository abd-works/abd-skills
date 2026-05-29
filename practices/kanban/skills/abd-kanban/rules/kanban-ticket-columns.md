---
scanner: war-room-shape
---

# Rule: Kanban ticket — skill-level progress within stage

War room tickets flow through stages defined by the system of work. Each ticket tracks per-skill progress (to_do, in_progress, done) and per-skill review (null, in_progress, done, failed).

## DO

- Track each ticket's progress as **per-skill status** within its current stage.
- Use skill statuses: **`to_do`**, **`in_progress`**, **`done`**.
- Use review statuses: **`null`** (not started), **`in_progress`**, **`done`**, **`failed`** (needs rework).
- Place tickets in exactly one board list: **`backlog`**, **`active`**, **`done`**, **`archived`**.
- A ticket is **active** when at least one skill has `status: in_progress` or `review_status: in_progress`.
- A ticket is **done** when ALL skills have `status: done` AND `review_status: done`.
- When a done ticket's next stage has **finer scope**, scatter it (archive parent, create children in backlog).
- When a done ticket's next stage has **same scope**, advance it (reset skills from system of work, move to active or backlog).
- Maintain **lineage** on every ticket — full path from project through increment, sprint, story.
- Skills within a stage execute **in order** per system of work; an agent may only claim a skill when prior skills in the list are done.
- Record **start** and **end** timestamps on every skill claim and completion.

## DO NOT

- Use slot files (`slot-NN-start.md`, `slot-NN-finished.md`, `slot-NN-claim.md`) — those are removed.
- Pre-plan work assignments — agents pull from tickets per system of work skill order.
- Put a ticket in multiple board lists simultaneously.
- Allow an agent to claim a skill that is out of order (prior skills in the stage must be done first).
- Scatter a ticket when the next stage has the same scope level — advance it instead.
- Remove lineage from child tickets after scatter — children carry their full ancestry.

## Example (wrong)

```json
{
  "tickets": {
    "inc-1": {
      "stage": "exploration",
      "column": "in_progress",
      "active_slot": "19"
    }
  }
}
```

Slot-based tracking with a single column — not this model.

## Example (correct)

```json
{
  "active": [
    {
      "ticket_id": "inc-1",
      "lineage": ["Hero VTT", "Increment 1"],
      "scope_level": "increment",
      "stage": "exploration",
      "priority": 1,
      "skills": {
        "abd-ubiquitous-language": { "status": "done", "role": "business-expert", "review_status": "done" },
        "abd-acceptance-criteria": { "status": "in_progress", "role": "product-owner", "review_status": null },
        "abd-ux-mockup": { "status": "to_do", "role": "ux-designer", "review_status": null },
        "abd-architecture-template": { "status": "to_do", "role": "engineer", "review_status": null }
      }
    }
  ],
  "backlog": [
    {
      "ticket_id": "inc-2",
      "lineage": ["Hero VTT", "Increment 2"],
      "scope_level": "increment",
      "stage": "exploration",
      "priority": 2
    }
  ]
}
```

Ticket with per-skill tracking; inc-2 waiting in backlog at priority 2.
