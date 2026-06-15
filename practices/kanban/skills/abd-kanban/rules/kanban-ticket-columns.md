---
scanner: war-room-shape
---

# Rule: Kanban ticket — progress tracking within stage

War room tickets flow through stages defined by the system of work. The **system-of-work.json** is the single source of truth for which skills a stage requires. Tickets carry only a `progress` map — lazily populated when agents claim skills.

## DO

- Track each ticket's execution state in a **`progress`** map (keyed by skill name).
- Populate `progress` entries **lazily** — only when an agent claims or completes a skill.
- Use skill statuses: **`to_do`**, **`in_progress`**, **`done`**.
- Use review statuses: **`null`** (not started), **`in_progress`**, **`done`**, **`failed`** (needs rework).
- Place tickets in exactly one board list: **`backlog`**, **`active`**, **`done`**, **`archived`**.
- A ticket is **active** when at least one skill has `status: in_progress` or `review_status: in_progress`.
- A ticket's stage is **done** when ALL skills listed in `system-of-work.json` for that stage have a `progress` entry with `status: done` AND `review_status: done`.
- When a done ticket's next stage has **finer scope**, scatter it (archive parent, create children in backlog).
- When a done ticket's next stage has **same scope**, advance it (clear progress, move to active or backlog).
- Maintain **lineage** on every ticket — full path from project through increment, sprint, story.
- Skills within a stage execute **in order** per system of work; an agent may only claim a skill when prior skills in the list are done.
- Record **start** and **end** timestamps on every skill claim and completion.
- Look up `role` for each skill from `system-of-work.json` — not from the ticket.

## DO NOT

- Put a `skills` key on tickets — skill definitions live in `system-of-work.json` only.
- Pre-populate `progress` with all skills at stage entry — let agents claim lazily.
- Use slot files (`slot-NN-start.md`, `slot-NN-finished.md`, `slot-NN-claim.md`) — those are removed.
- Pre-plan work assignments — agents pull from tickets per system of work skill order.
- Put a ticket in multiple board lists simultaneously.
- Allow an agent to claim a skill that is out of order (prior skills in the stage must be done first).
- Scatter a ticket when the next stage has the same scope level — advance it instead.
- Remove lineage from child tickets after scatter — children carry their full ancestry.

## Example (wrong)

```json
{
  "ticket_id": "inc-1",
  "stage": "exploration",
  "skills": {
    "abd-ubiquitous-language": { "status": "to_do", "role": "business-expert" },
    "abd-acceptance-criteria": { "status": "to_do", "role": "product-owner" }
  }
}
```

Ticket declares `skills` — duplicates system of work; brittle.

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
      "progress": {
        "abd-ubiquitous-language": { "status": "done", "agent": "business-expert", "review_status": "done" },
        "abd-acceptance-criteria": { "status": "in_progress", "agent": "product-owner", "review_status": null }
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

Active ticket with lazily-populated `progress`; backlog ticket with no progress yet. Skills for "exploration" are defined in `system-of-work.json`.
