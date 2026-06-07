---
scanner: war-room-shape
---

# Rule: Kanban ticket — skill progress tracking within stage

War room tickets flow through stages defined by the kanban board. The **kanban board** (`system-of-work.json`) is the single source of truth for which skills a stage requires. Tickets carry only a `skill_progress` map — lazily populated when agents start work on skills.

## DO

- Track each ticket's execution state in a **`skill_progress`** map (keyed by skill name).
- Populate `skill_progress` entries **lazily** — only when an agent starts or completes a skill.
- Use execution statuses: **`not_started`**, **`in_progress`**, **`done`**.
- Use review statuses: **`null`** (not started), **`in_progress`**, **`done`**, **`failed`** (needs rework).
- Place tickets in exactly one board list: **`backlog`**, **`active`**, **`done`**, **`archived`**.
- A ticket is **active** when at least one skill has `execution_status: in_progress` or `review_status: in_progress`.
- A ticket's stage is **done** when ALL skills listed in the kanban board for that stage have a `skill_progress` entry with `execution_status: done` AND `review_status: done`.
- When a done ticket's next stage has **finer scope**, scatter it (archive ticket, create children in backlog).
- When a done ticket's next stage has **same scope**, advance it (clear skill progress, move to active or backlog).
- Maintain **lineage** on every ticket — full path from project through increment, sprint, story.
- Skills within a stage execute **in order** per the kanban board stage configuration; an agent may only start a skill when prior skills in the list are done.
- Record **start** and **end** timestamps on every skill start and completion.
- Look up the `role` for each skill from `system-of-work.json` (kanban board stage configuration) — not from the ticket.

## DO NOT

- Put a `skills` key on tickets — skill definitions live in the kanban board (`system-of-work.json`) only.
- Pre-populate `skill_progress` with all skills at stage entry — let agents start work lazily.
- Use slot files (`slot-NN-start.md`, `slot-NN-finished.md`, `slot-NN-claim.md`) — those are removed.
- Pre-plan work assignments — agents pull from tickets per kanban board skill order.
- Put a ticket in multiple board lists simultaneously.
- Allow an agent to start a skill that is out of order (prior skills in the stage must be done first).
- Scatter a ticket when the next stage has the same scope level — advance it instead.
- Remove lineage from child tickets after scatter — children carry their full ancestry.

## Example (wrong)

```json
{
  "ticket_id": "inc-1",
  "stage": "exploration",
  "skills": {
    "abd-domain-language": { "status": "not_started", "role": "business-expert" },
    "abd-acceptance-criteria": { "status": "not_started", "role": "product-owner" }
  }
}
```

Ticket declares `skills` — duplicates kanban board stage configuration; brittle.

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
      "skill_progress": {
        "abd-domain-language": { "execution_status": "done", "agent": "business-expert", "review_status": "done" },
        "abd-acceptance-criteria": { "execution_status": "in_progress", "agent": "product-owner", "review_status": null }
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

Active ticket with lazily-populated `skill_progress`; backlog ticket with no skill progress yet. Skills for "exploration" are defined in `system-of-work.json` (kanban board stage configuration).
