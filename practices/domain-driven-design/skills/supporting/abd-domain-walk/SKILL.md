---
name: scenario-walkthrough
catalog_garden_order: 7
catalogue_one_liner: >-
  Walk scenarios through domain model or domain spec; validate class-operation ownership end-to-end.
description: >-
  Walk concrete scenarios through the domain model or spec. Every step maps to a class and operation; lifecycle guards and invariants come from the
  prior phase. Use when a domain model or domain spec exists and the team needs to validate that
  the model can express realistic flows end-to-end.
---

# abd-domain-walk

## Purpose

**Walk** concrete scenarios through the typed Class Model (or domain model where the Class Model is not yet built). Each step must map to a **class** and an **operation** from the prior phase's file. When a step crosses a state change or must respect a guard, align with the invariants and interactions captured upstream. If a step has no owner, record a gap and revise upstream artifacts.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `walkthrough.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-walkthrough.md`.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — prerequisites, the consistent scenario/walk shape, and the flat heading structure.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-walkthrough-scaffold.md` | The walkthrough file with scenarios grouped under KAs, pseudocode walks, references, and decisions. |

**Scenarios per KA:** Cover at minimum one happy path, one failure or edge path, one path involving cooperation or shared resources. Use real domain values, not placeholders. Every pseudocode line that performs domain logic must trace to a class and operation in the prior-phase file.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-domain-walk \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

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
