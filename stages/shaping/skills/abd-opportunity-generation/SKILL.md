---
name: abd-opportunity-canvas
catalog_garden_tier: practice
catalog_garden_order: 16
catalogue_one_liner: >-
  Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build.
description: >-
  Frame a candidate opportunity, align stakeholders on a shared bet, and make assumptions
  explicit before committing to build. Use when starting a new initiative that needs stakeholder
  alignment on problems, users, solutions, and success criteria before delivery begins, or when
  co-creating a common model across multiple voices.
---
# abd-opportunity-canvas

## Purpose

This skill exists so you **do not start "building a solution"** while people are thinking about **a different problem**, **a different customer**, or **a different definition of success**.

It makes an **opportunity** explicit — who it is for, why the organisation should care, what you might build or buy, how you would know it worked, and what the effort looks like. You finish with enough alignment that **downstream build and delivery work** is based on a shared model. Every part of the canvas is also a candidate **assumption** — beliefs about customers, value, and capability that teams often turn into falsifiable statements and run through a lightweight validation path (see **abd-simple-validated-learning**).

---

## Output file

**Deliverables folder:** see `../common/reference/skill-workflow.md` — Output file resolution.

**File name:** `opportunity-canvas.md`, `opportunity-canvas-sections.md`, and `opportunity-canvas.txt`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../common/reference/skill-workflow.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what an opportunity canvas is, the eight fixed sections with guiding questions, section definitions, assumptions (hypothesis types and mining approach), and the build method (prepare inputs, fill sections, trace spine, ensure parity).

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/opportunity-canvas.md` | **Table** canvas: one markdown table row per section, columns for individual items. `OPPORTUNITY:`, `ALTERNATIVES:`, and `ASSUMPTION:` fields sit outside the table. |
| `templates/opportunity-canvas-sections.md` | **Section** canvas: for each row, a heading + guiding questions + `PREFIX:` answer lines. Use when prose depth is needed. |
| `templates/opportunity-canvas.txt` | Plain-text parity with the section `.md` — same sections, same prefix lines, same content for the same engagement. |

**Method:** Follow the build method in `reference/concepts.md` — prepare inputs, fill each section with intent, trace the spine, ensure parity across all three files.

**Parity:** Table and section/text files must match for the same engagement — same Opportunity, same row coverage, same Assumptions with the same validate-by intent. No drift between files.

### 3. Validate

Run the scanners:

```bash
python skills/common/scripts/run_scanners.py \
  --skill-root skills/abd-opportunity-generation \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../common/reference/skill-workflow.md`.

---

## Validate

**Goal:** Inspect what was built — would another facilitator trust this canvas to drive the next learning conversation?

- **Sponsor and product** — Can see clear Customer Problems and Solution Features, and a business case through Key Metrics of Success, Revenue Drivers, and Cost Drivers.
- **Engineering and design** — Can see Key Activities and Resources, Key Partners, and testable Assumptions with validate-by clauses.
- **Parity** — Table and section/text files match for the same engagement; no extra row or Assumption in one file only.
- **Honest bar** — Do not claim this practice requires steps or wording that this page and the rules do not actually set.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
