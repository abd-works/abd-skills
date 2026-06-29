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

**Deliverables folder:** see `common/skill-workflow.md` — Output file resolution.

**File name:** `specification-by-example.md` — a single file for all stories in the module. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

Follow `common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what specification by example is, Given/When/Then, scenarios vs outlines, domain concept grounding, quick checklist.
- **`reference/examples.md`** — worked examples showing plain Scenarios, Scenario Outlines with relationship-based tables, and Background.

**Default input — domain model outline:** Always read the domain model before writing any scenario. The domain model outline is the structural spine for all scenarios: concept names, relationships, invariants, and constraints come from there verbatim.

Read in this priority order:
- **Class Model** (`domain-specification.md`) — typed classes with invariants and typed relationships. Use first when present.
- **Domain model** (`domain-model.md`) — concepts with responsibilities and collaborators. **Default source** when no Class Model exists.
- **Domain language** (`domain-language.md`) — defined terms and key abstractions. Use for term verification and when no model file exists.

Check for `domain.json` in the workspace. If it does not exist and a domain model markdown file is present, produce `domain.json` before running the scanner.

### 2. Generate

**Default notation: Scenario Outline.**

Use **Scenario Outline** with normalised **Examples** tables for every story that has more than one scenario. This is the default — do not use plain Scenario blocks for multi-scenario stories.

- **Scenario Outline** (default): `{column_name}` tokens in steps bound to per-concept Examples tables above (Given data) and below (When/Then data). Use for all stories with data variation — happy path, failure, edge cases share the same step structure and differ only in row data.
- **Plain Scenario** (exception only): use only when a story has exactly one scenario AND parameterising it with a one-row table adds no value.

Never use a plain `Scenario` block when a story covers multiple paths. If paths differ in data, use Outline rows. If paths differ structurally, model each structural variant as its own Scenario Outline.

**Produce the template:**

| Template | What to produce |
| --- | --- |
| `templates/specification-by-example.md` | Given/When/Then scenarios for each story, using the chosen notation. No template `## Instructions` in deliverables. |

**While writing:**
- Use the **domain model outline** as the structural spine: concept names in bold, relationships made explicit in step language, invariants exercised by at least one scenario.
- Use **Background** when three or more scenarios share identical starting state (Given/And only).
- Name each scenario by its **outcome**, not its action.
- Cover at least one happy path, one failure or rejection, and any edge cases implied by the story.
- If *Acceptance Criteria* exist, use the main-flow AC as your spine: convert WHEN → When, THEN → Then, add Given preconditions.
- **Start with Scenario Outline** for every story with more than one scenario. Only fall back to plain Scenario when a story has a single, non-parameterisable path.
- **Stubbed external services:** When a scenario involves a stubbed service (hardcoded request + response), apply `rules/stub-service-interaction-structure.md`: declare the stub in **Given**, express the system-captures → system-forwards → service-returns sequence in **When**, assert only the business outcome in **Then**. Never put a stub response in **Then**. For every new stub input/output pair introduced, note it for stub fixture update (see `abd-story-acceptance-test` rule `stub-data-sync-with-scenarios`).

**Domain grounding:**
- Use exact concept names from the domain model source; do not paraphrase, abbreviate, or rename.
- Make relationships deliberate in step language and table column sets.

Generated artifacts contain only scenario content; template instructions stay in `templates/` for maintainers.

### 3. Validate

Run scanners and emit per-rule verdicts — see `common/skill-workflow.md` § Validate output.


---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Given/When/Then structure** — correct keywords; Background is state-only; multiple When/Then beats where the flow requires.
- **Trailing spaces** — every step line (Given, When, Then, And, But) ends with two trailing spaces so markdown preview renders each step on its own line.
- **Domain emphasis** — domain-significant terms use *italics* consistently; concept names match the domain model exactly.
- **Scenario Outline is the default** — every multi-scenario story uses Scenario Outline with Examples tables. Plain Scenario only for truly single-path stories with no data variation.
- **Coverage** — happy path, failure path, and edge cases implied by story or AC are visible.
- **Domain model grounding** — `domain.json` matches or has been produced if a domain model file exists.
- **Stub structure** — if any scenario involves a stubbed service: stub declared in Given, invocation + response in When, business outcome only in Then. No stub response in Then.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
