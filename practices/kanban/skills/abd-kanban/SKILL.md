---
name: abd-kanban
catalog_garden_tier: practice
catalog_garden_order: 60
catalogue_one_liner: >-
  JIT kanban board — tickets flow through stages, scatter at scope boundaries, agents pull work.
description: >-
  JIT kanban board for kanban lead and agents. Tickets flow through stages
  defined by the kanban board, scatter into finer-grained tickets at scope
  boundaries, and agents pull skill-level work from tickets.
  Use when setting up a delivery kanban board, initialising a kanban board, configuring
  ticket flow, or tracking delivery progress across stages.
---
# abd-kanban

## Purpose

Configure the kanban board for a delivery engagement. The *kanban board* defines ordered stages, each with a scope level and stage work required. Tickets carry only a lazily-populated `skill_progress` map; the kanban board (`kanban.json`) is the single source of truth for which skills a stage require. The kanban app owns all board mechanics from there.

---

## Output

Files to `<workspace>/docs/kanban/`:

- `kanban.json` — board config (stages, stage work required, strategy, team)
- `board.json` — initial board state (empty backlog/active/done/archived)
---

## Agent Instructions

Read [../../reference/kanban-board.md](../../reference/kanban-board.md) and [../../reference/artifact-layout.md](../../reference/artifact-layout.md) before starting.

### 1. Generate

Read every file in **`rules/`**; author to those rules.

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
