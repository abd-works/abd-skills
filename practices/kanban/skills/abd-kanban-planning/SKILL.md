---
name: abd-kanban-planning
catalog_garden_tier: practice
catalog_garden_order: 70
catalogue_one_liner: >-
  Strategy selection and system of work configuration — no pre-planned runs or slot tables.
description: >-
  Select delivery strategy, configure system of work (stages, scope progression,
  skill order), and define scatter/decomposition rules. Planning drives the Kanban
  board via strategy — not by pre-authoring runs, slots, or assignments.
  Use when selecting a delivery strategy, configuring a system of work, defining
  scatter rules, or saving a reusable strategy under strategies/.
---
# abd-kanban-planning

## Purpose

Delivery planning configures *how* delivery flows — not *what* to build. It selects a **strategy** based on context and risk, configures the **kanban board** (stages, scope levels, stage work required), and defines **scatter rules** (how and when tickets decompose at scope boundaries). The result drives the JIT kanban board without pre-authoring every assignment.

Do **not** use this skill to produce artifacts (maps, slices, AC, tests, code). This skill is strictly about the delivery lifecycle spine — the kanban board stage configuration, strategy, and decomposition rules.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File names:** Strategy output is written to:

```text
<workspace>/docs/planning/delivery-war-room/
  kanban.json                # Stages, scope, stage work required, strategy, team
```

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — kanban board stage configuration, strategy, backlog, risk classification, strategy selection procedure, delivery flow stages, checkpoint granularity, scatter rules, bootcamp stages, delivery roles, strategy catalog.
- **`strategies/*.md`** — one prepackaged strategy per file; read each strategy's "When to use" section to match context.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

Follow the **strategy selection procedure** from `reference/concepts.md`:

1. **Context analysis** — identify known domains, risky domains, integration points, complexity drivers, existing assets.
2. **Select strategy** — match context and risks to a strategy from `strategies/` (or blend/custom).
3. **Configure kanban board** — write `kanban.json` (stages, stage work required, strategy, team).
4. **Present and confirm** — present context assessment, kanban board configuration, scatter rules. **CHECKPOINT** — wait for user confirm.

**Scripts:** Use `scripts/append_plan_revision.py` to append revisions to the strategy.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-kanban-planning \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Strategy named** — a specific strategy from `strategies/` is cited (or a custom one is defined).
- **System of work complete** — stages, scope per stage, and ordered skills per stage are all populated.
- **Risks classified** — context assessment names risk types with signals.
- **Scatter rules explicit** — scope transitions, sprint grouping, and JIT policy are stated.
- **Checkpoints match risk** — high-risk areas have tighter checkpoints.
- **Not a default six-stage copy** — the plan reflects context, not a rote template.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
