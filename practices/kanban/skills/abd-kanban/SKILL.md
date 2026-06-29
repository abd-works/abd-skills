---
name: abd-kanban
catalog_garden_tier: practice
catalog_garden_order: 60
catalogue_one_liner: >-
  JIT kanban board — tickets flow through stages, scatter at scope boundaries, agents pull work.
description: >-
  Configure a delivery kanban board with stages, scope levels, and ticket flow rules. Use when initialising a board or defining how tickets flow through delivery stages.
---
# abd-kanban

## Purpose

Make delivery work visible and flow-governed — so nothing hides and bottlenecks surface immediately.

---

## Grill prompts

Read `common/reference/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these:

- **WIP invisibility** — What work is actually in progress that the board does not show — side tasks, rework, blocked items waiting silently?
- **Stage definition** — Can every team member state what "done" means at each stage, or do items drift forward by feel?
- **Scatter confusion** — When a ticket scatters into children, does the team know who owns the children and when the parent moves?
- **Flow vs batch** — Are you pulling one item at a time to completion, or pushing batches through each stage?
- **Bottleneck blindness** — Where is work piling up right now, and would the board make that obvious to a newcomer?

---

## Output

Files to `<workspace>/docs/kanban/`:

- `kanban.json` — board config (stages, stage work required, strategy, team)
- `board.json` — initial board state (empty backlog/active/done/archived)
---

## Agent Instructions

Read [../../reference/kanban-board.md](../../reference/kanban-board.md) and [../../reference/artifact-layout.md](../../reference/artifact-layout.md) before starting.

### 1. Generate

Produce output from the templates:

- **`templates/kanban.json`** — board config
- **`templates/board.json`** — initial board state

### 2. Validate

Review output against the rules in **`rules/`** and the checklist below.

---

## Validate

- **Ticket shape** — tickets carry `skill_progress` map only, no `skills` key; `kanban.json` is the source of truth for stage skills.
- **Scattering** — scope transitions produce children at finer scope; parent follows children on the board.
- **Backlog order** — hierarchical, ordered by story map priority + thin-slicing.
- **Workspace layout** — kanban board under `docs/kanban/`; `docs/end-to-end/<stage>/` and `docs/increments/` per [artifact-layout.md](../../reference/artifact-layout.md).

---
