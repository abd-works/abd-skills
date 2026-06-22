---
name: abd-kanban-planning
catalog_garden_tier: practice
catalog_garden_order: 70
catalogue_one_liner: >-
  Strategy selection and system of work configuration ” no pre-planned runs or slot tables.
description: >-
  Select a delivery strategy and configure the system of work — stages, scope progression, and scatter rules. Use when choosing how work flows through the kanban board.
---
# abd-kanban-planning

## Purpose

Choose how work flows — strategy, stage structure, and scatter rules — so delivery has a spine before tickets start moving.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these:

- **Strategy fit** — Does the chosen strategy match the team's actual risks, or is it the one you always use?
- **Stage bloat** — Do you have stages that exist because "we've always had them," not because they protect against a named risk?
- **Checkpoint granularity** — Are checkpoints tight enough for risky work and loose enough for known work — or uniformly heavy?
- **Scatter rules** — When a ticket crosses a scope boundary, does the team know exactly how many children appear and who pulls them?
- **Missing risk** — What risk has the team not named that could stall flow — a shared dependency, an approval gate, a skill gap?

---

## Output file

**Deliverables folder:** see [artifact-layout.md](../../reference/artifact-layout.md) ” Output file resolution.

**File names:** Strategy output is written to:

```text
<workspace>/docs/kanban/
  kanban.json                # Stages, scope, stage work required, strategy, team
```

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- `reference/strategy.md` - strategy concepts, risk classification, checkpoint granularity, scatter rules.
- `reference/selecting-a-strategy.md` - strategy selection procedure.
- `reference/strategy-catalog.md` - available strategies, how to add and adapt.
- **`reference/strategies/*.md`** ” one prepackaged strategy per file; read each strategy's "When to use" section to match context.

### 2. Generate

Follow the **strategy selection procedure** from `reference/selecting-a-strategy.md`:

1. **Context analysis** ” identify known domains, risky domains, integration points, complexity drivers, existing assets.
2. **Select strategy** ” match context and risks to a strategy from `reference/strategies/` (or blend/custom).
3. **Configure kanban board** ” write `kanban.json` (stages, stage work required, strategy, team).
4. **Present and confirm** ” present context assessment, kanban board configuration, scatter rules. **CHECKPOINT** ” wait for user confirm.

**Scripts:** Use `scripts/append_plan_revision.py` to append revisions to the strategy.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built ” read the artifacts as reviewers.

- **Strategy named** ” a specific strategy from `reference/strategies/` is cited (or a custom one is defined).
- **System of work complete** ” stages, scope per stage, and ordered skills per stage are all populated.
- **Risks classified** ” context assessment names risk types with signals.
- **Scatter rules explicit** ” scope transitions, sprint grouping, and JIT policy are stated.
- **Checkpoints match risk** ” high-risk areas have tighter checkpoints.
- **Not a default six-stage copy** ” the plan reflects context, not a rote template.
- **No bundle markers** ” `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
