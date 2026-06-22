---
name: abd-domain-walk
catalog_garden_order: 7
catalogue_one_liner: >-
  Prove the domain model handles real scenarios end-to-end — find gaps before code does.
description: >-
  Walk concrete scenarios through the domain model or spec to validate it handles realistic flows end-to-end. Use when a domain model exists and needs scenario-level validation.
context-perspective: domain
context-fidelity:
  - level: specification
    mode: walkthrough
---

# abd-domain-walk

## Purpose

Prove the domain model handles real scenarios end-to-end — find gaps before code does.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these:

- **Happy-path blindness** — Which scenarios have you walked only as success paths, without testing what happens when a step fails or data is missing?
- **Model gap** — Which pseudocode line required you to invent a method or class that does not exist in the domain model?
- **Cooperation under stress** — What happens when two aggregates need to coordinate and one rejects the request?
- **Real data** — Are your scenario values realistic enough to expose edge cases, or are they "example 1, example 2" placeholders?
- **Missing scenario** — Which business scenario did the domain expert mention that you have not walked yet?

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File name:** `walkthrough.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-walkthrough.md`.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — prerequisites, the consistent scenario/walk shape, and the flat heading structure.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-walkthrough-scaffold.md` | The walkthrough file with scenarios grouped under KAs, pseudocode walks, references, and decisions. |

**Scenarios per KA:** Cover at minimum one happy path, one failure or edge path, one path involving cooperation or shared resources. Use real domain values, not placeholders. Every pseudocode line that performs domain logic must trace to a class and operation in the prior-phase file.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Per-phase output file** — named `[<name>-]walkthrough.md`. No prior or later phase content lives in it.
- **No sub-headings under scenarios** — walk blocks live directly under each `### **Scenario**` heading.
- **References per KA** — one `### references` per KA with fenced `source` blocks.
- **Decisions per KA** — one `### decisions made` per KA listing gaps and ownership calls.
- **Every walk line traces** — every domain-logic pseudocode line maps to a class and operation from the prior-phase file.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
