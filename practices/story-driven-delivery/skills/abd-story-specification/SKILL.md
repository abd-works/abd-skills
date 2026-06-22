---
name: abd-story-specification
catalog_garden_tier: practice
catalog_garden_order: 40
catalogue_one_liner: >-
  Turn acceptance criteria into concrete, testable examples — so behaviors are unambiguous before code.
description: >-
  Produce Given/When/Then specification scenarios with realistic domain values from acceptance criteria. Use when making story behavior concrete and testable before code.
context-perspective: stories
context-fidelity:
  - level: specification
    mode: spec-by-example
---
# abd-story-specification

## Purpose

Make story behavior unambiguous — concrete examples with real values so devs and domain experts agree on exactly what happens before code is written.

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File name:** `specification-by-example.md` — a single file for all stories in the module. Add a `<name>-` prefix only when disambiguation is needed.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Concrete enough to disagree** — if you showed these examples to a domain expert and a developer, would they argue about whether the output is correct? If not, the examples might be too vague to catch real misunderstandings.
- **Values from where** — are the example values representative of real domain data, or generic placeholders? Realistic values surface edge cases that "John Doe, $100" never will.
- **Missing state combinations** — what combinations of Given conditions have we not explored? The dangerous bugs live in states nobody thought to combine.
- **Assumed preconditions** — what has to be true before each scenario starts — and does everyone agree on that starting state, or are there hidden setup assumptions?
- **Boundary behaviors** — what happens at the edges — zero, one, many, max, just-over-max? Have we specified what the system does at the limits, or just in the comfortable middle?

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what specification by example is, Given/When/Then, scenarios vs outlines, domain concept grounding, quick checklist.
- **`reference/examples.md`** — worked examples showing plain Scenarios, Scenario Outlines with relationship-based tables, and Background.

Also check whether any of the following domain model content exists in the workspace:
- **Class Model** — typed classes with attributes and typed relationships. Use it first.
- **domain model** — each concept listed with responsibilities and collaborators. Use when no Class Model exists.
- **Domain language or key abstractions** — a glossary, list of defined terms. Use as fallback.

Check for `domain.json` in the workspace. If it does not exist and a domain model markdown file is present, produce `domain.json` before running the scanner.

### 2. Generate

**Choose notation first:**
- **Scenarios** (plain): each scenario has distinct context; all values inline. Use for main flow, failure, edge cases.
- **Scenario Outlines**: same Given/When/Then steps across multiple data rows; `{column_name}` tokens bound to an **Examples** block. Use only when steps are genuinely identical across every row.

If not specified, determine based on the nature of the requirements and confirm with the user.

**Produce the template:**

| Template | What to produce |
| --- | --- |
| `templates/specification-by-example.md` | Given/When/Then scenarios for each story, using the chosen notation. No template `## Instructions` in deliverables. |

**While writing:**
- Use **Background** when three or more scenarios share identical starting state (Given/And only).
- Name each scenario by its **outcome**, not its action.
- Cover at least one happy path, one failure or rejection, and any edge cases implied by the story.
- If *Acceptance Criteria* exist, use the main-flow AC as your spine: convert WHEN → When, THEN → Then, add Given preconditions.
- If you find yourself writing the same steps three or more times with only values changing, switch to **Scenario Outlines**.

**Domain grounding:**
- Use exact concept names from the domain model source; do not paraphrase, abbreviate, or rename.
- Make relationships deliberate in step language and table column sets.

Generated artifacts contain only scenario content; template instructions stay in `templates/` for maintainers.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.


---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Given/When/Then structure** — correct keywords; Background is state-only; multiple When/Then beats where the flow requires.
- **Domain emphasis** — domain-significant terms use *italics* consistently; concept names match the domain model exactly.
- **Scenario vs Outline choice** — Outlines used only when steps are genuinely identical across all rows.
- **Coverage** — happy path, failure path, and edge cases implied by story or AC are visible.
- **Domain model grounding** — `domain.json` matches or has been produced if a domain model file exists.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
