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

**Deliverables folder:** see `../common/story-driven-delivery/skill-extensions.md` — Output file resolution.

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
- **Stubbed services** — if the scenario involves an external service or system whose response is hardcoded in a stub, is the stub declared in Given, the invocation and response expressed in When, and only the business outcome in Then? Or has the service response leaked into Then as though it were a business result?

---

## Agent Instructions

Follow `../common/story-driven-delivery/skill-extensions.md` and `common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what specification by example is, Given/When/Then, scenarios vs outlines, domain concept grounding, quick checklist.
- **`reference/examples.md`** — worked examples showing plain Scenarios, Scenario Outlines with relationship-based tables, and Background.

**Default input — domain model outline:** Read `../common/story-driven-delivery/domain-input-priority.md` before writing any scenario.

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

Run scanners and emit per-rule verdicts — see `../common/story-driven-delivery/skill-extensions.md` § Validate output and `../common/story-driven-delivery/validate-checklist.md`.


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

---
