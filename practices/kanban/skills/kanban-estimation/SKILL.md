---
name: kanban-estimation
catalog_garden_tier: practice
catalog_garden_order: 72
catalogue_one_liner: >-
  Collaborative estimation at any scope level  contributing factors, categories, team vote, and recorded rationale.
description: >-
  Facilitate collaborative estimation — contributing factors, size categories, team vote, and recorded rationale. Use when sizing backlog items or re-estimating after scope changes.
---
# kanban-estimation

**Manual:** `./manual/index.html`

## Purpose

Agree on sizing with recorded rationale — so re-estimation never starts from scratch and assumptions are visible.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these:

- **False precision** — Are you estimating to a precision the team cannot consistently deliver, or using categories everyone understands?
- **Factor blindness** — Which contributing factor is everyone ignoring because it is uncomfortable — regulatory, skill gap, integration risk?
- **Anchoring** — Is the first speaker's estimate biasing the rest of the team, or are votes truly independent?
- **Split avoidance** — Is a large item staying whole because nobody wants to do the work of splitting it, not because it cannot be split?
- **Calibration drift** — Does a "Medium" today mean the same thing it meant two sessions ago — and how would you know?

---

## Output file

**Deliverables folder:** see [artifact-layout.md](../../reference/artifact-layout.md).

**File names:** `estimation-session.md` (one per session) and `estimate-record.md` (one per scope item). Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`**  scope items, contributing factors, estimation categories, split threshold, team vote, estimate records, interactive estimation, backlog changes during estimation, and the shape of estimation output.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/estimation-session.md` | Session scope, coverage boundary, contributing-factors catalog, estimation-category scheme, priority-ordered items, and session summary |
| `templates/estimate-record.md` | One record per scope item: chosen category, factor breakdown, vote rounds, discussion notes, emergent scope |

**Session flow:**

1. **Establish session scope**  agree on granularity (epics / sub-epics / stories / thin slices). Review bootcamp stages and confirm coverage boundary (defaults: exploration, specification, engineering, regression testing). Record in session setup.
2. **Build contributing-factors catalog**  start with seed factors, add/remove per team input.
3. **Define estimation categories**  team picks a scheme (T-shirt, Fibonacci, S/M/L/XL, custom) with rough meanings and split threshold.
4. **Prioritize backlog**  present items, suggest priority order, let team reorder.
5. **Walk item by item**  present, AI suggests starting category, team votes (simultaneous reveal), discuss divergence, check split threshold, record estimate, handle backlog changes.
6. **Save the session**  review for calibration consistency, flag deeply-split items.

**Backlog changes:** When estimation surfaces new AC, new stories, splits, or merges  record in the estimate record's emergent-scope section with the downstream skill tagged, then persist to `story-graph.json` via **`story-graph-ops`**.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect the estimation outputs as a reviewer  check that the session is honest, the records are complete, and the conversation was real.

- **Coverage boundary stated**  the session file names what the estimate includes (bootcamp stages) so estimates are comparable.
- **Contributing factors are specific**  factor notes per item reflect that item's reality, not copy-pasted boilerplate across every record.
- **Categories are calibrated**  a quick scan of all records shows the categories make sense relative to each other.
- **Discussion is visible**  estimate records with divergent votes show what the disagreement was about, not just the final number.
- **Emergent scope captured**  new AC, new stories, splits, merges, and open questions are recorded with the downstream skill tagged.
- **No invented precision**  estimates use the agreed categories, not fake-precise numbers.
- **Split threshold honoured**  every story above the session's split threshold was either decomposed or has a recorded justification for staying whole.
- **Re-estimation path clear**  items flagged as deeply split or uncertain have a next step noted.
- **Interactive, not batch**  each item has its own vote cycle and discussion.
- **No bundle markers**  `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
