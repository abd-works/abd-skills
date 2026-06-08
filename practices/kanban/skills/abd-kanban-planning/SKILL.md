---
name: abd-kanban-planning
catalog_garden_tier: practice
catalog_garden_order: 70
catalogue_one_liner: >-
  Strategy selection and system of work configuration â€” no pre-planned runs or slot tables.
description: >-
  Select delivery strategy, configure system of work (stages, scope progression,
  skill order), and define scatter/decomposition rules. Planning drives the Kanban
  board via strategy â€” not by pre-authoring runs, slots, or assignments.
  Use when selecting a delivery strategy, configuring a system of work, defining
  scatter rules, or saving a reusable strategy under reference/strategies/.
---
# abd-kanban-planning

## Purpose

Kanban Planning configures *how* delivery flows â€” not *what* to build. It selects a **strategy** based on context and risk, configures the **kanban board** (stages, scope levels, stage work required), and defines **scatter rules** (how and when tickets decompose at scope boundaries). The result drives the JIT kanban board without pre-authoring every assignment.

Do **not** use this skill to produce artifacts (maps, slices, AC, tests, code). This skill is strictly about the delivery lifecycle spine â€” the kanban board stage configuration, strategy, and decomposition rules.

---

## Output file

**Deliverables folder:** see [artifact-layout.md](../../reference/artifact-layout.md) â€” Output file resolution.

**File names:** Strategy output is written to:

```text
<workspace>/docs/kanban/
  kanban.json                # Stages, scope, stage work required, strategy, team
```

---

## Agent Instructions

> **MANDATORY — read [artifact-layout.md](../../reference/artifact-layout.md) before starting. It defines canonical output paths per stage and increment.**

### 1. Read context

Read these files:
- `reference/strategy.md` - strategy concepts, risk classification, checkpoint granularity, scatter rules.
- `reference/selecting-a-strategy.md` - strategy selection procedure.
- `reference/strategy-catalog.md` - available strategies, how to add and adapt.
- **`reference/strategies/*.md`** â€” one prepackaged strategy per file; read each strategy's "When to use" section to match context.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

Follow the **strategy selection procedure** from `reference/selecting-a-strategy.md`:

1. **Context analysis** â€” identify known domains, risky domains, integration points, complexity drivers, existing assets.
2. **Select strategy** â€” match context and risks to a strategy from `reference/strategies/` (or blend/custom).
3. **Configure kanban board** â€” write `kanban.json` (stages, stage work required, strategy, team).
4. **Present and confirm** â€” present context assessment, kanban board configuration, scatter rules. **CHECKPOINT** â€” wait for user confirm.

**Scripts:** Use `scripts/append_plan_revision.py` to append revisions to the strategy.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-kanban-planning \
  --workspace <path-to-output>
```

Then emit per-rule verdicts (PASS / FAIL with reason) for every rule in `rules/`.

---

## Validate

**Goal:** Inspect what was built â€” read the artifacts as reviewers.

- **Strategy named** â€” a specific strategy from `reference/strategies/` is cited (or a custom one is defined).
- **System of work complete** â€” stages, scope per stage, and ordered skills per stage are all populated.
- **Risks classified** â€” context assessment names risk types with signals.
- **Scatter rules explicit** â€” scope transitions, sprint grouping, and JIT policy are stated.
- **Checkpoints match risk** â€” high-risk areas have tighter checkpoints.
- **Not a default six-stage copy** â€” the plan reflects context, not a rote template.
- **No bundle markers** â€” `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
