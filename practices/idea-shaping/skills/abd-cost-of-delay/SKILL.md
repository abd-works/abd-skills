---
name: abd-cost-of-delay
catalog_garden_tier: practice
catalog_garden_order: 21
catalogue_one_liner: >-
  Quantify urgency × value for backlog items; score CD3 and rank to prioritize by economic impact of delay.
description: >-
  Estimate Cost of Delay for features or initiatives, classify value type and urgency profile,
  calculate CD3 (Cost of Delay divided by Duration), and rank items to prioritize by economic
  impact. Use when ordering a backlog by value, comparing initiatives, or making trade-off
  decisions about what to build next.
---
# abd-cost-of-delay

## Purpose

Teams routinely prioritize work by gut feel, stakeholder loudness, or first-in-first-out — all of which ignore how much value decays while items wait to be delivered. Cost of Delay puts a price tag on time so teams can make scheduling decisions based on economics rather than politics.

This skill classifies the value type and urgency of each feature or initiative in context, then builds a simple value model that makes assumptions explicit, calculates Cost of Delay per time period (month / week), divides by duration to get CD3, and ranks so the highest-value shortest-duration work goes first.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `cost-of-delay-canvas.md` and `cd3-ranking.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — value types, urgency profiles, CD3 formula, the 7-step method, assumptions guidance, and neighbour skills.
- **`reference/examples.md`** — worked FIFO vs CD3 comparison showing the revenue and opportunity-cost impact of ordering.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/cost-of-delay-canvas.md` | One canvas per item: value type, urgency profile, assumptions table, CoD calculation, CD3 score |
| `templates/cd3-ranking.md` | Ranked list of all scored items with CoD, duration, CD3, and ordering rationale |

**Method:** Follow the 7-step method in `reference/concepts.md`. Each step must be visible in the output — isolate items, check lead time, classify, build value model, calculate CD3, rank, and compare orderings.

**Script invocation:** Use the calculation script for ranking tables and what-if comparisons — do not hand-compute:

```bash
python skills/abd-cost-of-delay/scripts/cd3_table.py \
  --items "Name1:CoD1:Dur1, Name2:CoD2:Dur2, ..." \
  --period-label "Week"
```

For side-by-side ordering comparison:

```bash
python skills/abd-cost-of-delay/scripts/cd3_table.py \
  --items "Name1:CoD1:Dur1, Name2:CoD2:Dur2, ..." \
  --compare "A,B,C" "B,C,A" \
  --period-label "Week"
```

**Parity:** Items that appear in the ranking must have a canvas (or reference one from prior work). CoD and CD3 values must match across both files.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-cost-of-delay \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Assumptions explicit** — Every CoD estimate traces to named assumptions with factors, units, and confidence. No "we think it's worth $X" without showing the model.
- **Value type and urgency assigned** — Each item has exactly one value type and one urgency profile, with rationale.
- **CD3 arithmetic** — CoD / Duration = CD3; check the maths.
- **Ranking is by CD3** — Items ordered highest-first; any deviation from pure CD3 order has stated rationale.
- **Cross-template parity** — Canvas CoD and CD3 match the ranking table values.
- **No invented precision** — Estimates reflect stated confidence; uncertain assumptions are flagged, not hidden behind false precision.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
