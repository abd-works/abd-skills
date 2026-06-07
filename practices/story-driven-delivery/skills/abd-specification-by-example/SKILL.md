---
name: abd-specification-by-example
catalog_garden_tier: practice
catalog_garden_order: 40
catalogue_one_liner: >-
  Given/When/Then scenarios with real domain values; plain or outline (data tables) templates.
description: >-
  Produces Given/When/Then specification scenarios with real domain values. Use when
  writing BDD scenarios, refining acceptance criteria into specs, or making story behavior concrete.
---
# abd-specification-by-example

## Purpose

Write **Given/When/Then** scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `specification-by-example.md` — a single file for all stories in the module. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

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

Read every file in **`rules/`**; author to those rules.

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

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-specification-by-example \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.


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
