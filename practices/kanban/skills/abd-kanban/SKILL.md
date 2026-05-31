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
  Use when setting up a delivery war room, initialising a kanban board, configuring
  ticket flow, or tracking delivery progress across stages.
---
# abd-kanban

## Purpose

Single on-disk home for **skill progress** and **handoffs**. Models delivery as a **JIT kanban board** where tickets flow through stages, scatter into finer-grained tickets at scope boundaries, and agents pull skill-level work from tickets.

The *kanban board* defines ordered stages, each with a scope level and stage work required. Tickets carry only a lazily-populated `skill_progress` map; the kanban board is the single source of truth for which skills a stage requires. When a ticket completes a stage and the next stage's scope is finer, the ticket **scatters** into child tickets at the finer scope. **Four executor agents** (one per delivery role, scalable via `team`) **pull** skill-level work from active tickets across **all stages** — see [../../agents/reference/pull-model.md](../../agents/reference/pull-model.md).

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File names:** War room files — `board.json`, `kanban.json`, `INSTRUCTIONS.md`, `metrics-log.jsonl`. Output to `<workspace>/docs/planning/delivery-war-room/`.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**
>
> **Kanban lead and delivery agents:** read [../../agents/reference/session-bootstrap.md](../../agents/reference/session-bootstrap.md), [../../agents/reference/pull-model.md](../../agents/reference/pull-model.md), and [../../reference/artifact-layout.md](../../reference/artifact-layout.md) on turn 1 and complete loop wiring / continuous pull **before** board work or skill execution.

### 1. Read context

Read these files:
- **`../../reference/kanban-board.md`** — kanban board, tickets (shape, lifecycle, status flow), scattering, backlog, metrics, and limits.
- **`../../reference/agents-and-skills.md`** — skill progress, agents (delivery roles, work cycle), progress authority, workspace layout, kanban lead setup and scan cycle.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

- **`templates/board.json`** — kanban board state (tickets, backlog, active, done, archived)
- **`templates/kanban.json`** — kanban board (stages, stage work required, strategy, team)
- **`templates/INSTRUCTIONS.md`** — agent bootstrap instructions
- **`templates/ticket.json`** — ticket shape reference
- **`templates/brownfield-boundary-gate.md`** — brownfield boundary gate (when applicable)

**Scripts:** Use the following scripts for board operations:

```bash
python kanban/skills/abd-kanban/scripts/sync_kanban_board.py --workspace <workspace>
python kanban/skills/abd-kanban/scripts/scatter_ticket.py --workspace <workspace> --ticket <id>
python kanban/skills/abd-kanban/scripts/track_metrics.py --workspace <workspace>
```

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-kanban \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Ticket shape** — tickets carry `skill_progress` map only, no `skills` key; kanban board is the source of truth for stage skills.
- **Scattering** — scope transitions produce children at finer scope, ticket archived.
- **Backlog order** — hierarchical, ordered by story map priority + thin-slicing.
- **Agents** — agents pull from tickets matching their delivery role in the kanban board stage configuration.
- **Workspace layout** — war room under `docs/planning/delivery-war-room/`; `docs/end-to-end/<stage>/` and `docs/increments/` per [artifact-layout.md](../../reference/artifact-layout.md).
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
