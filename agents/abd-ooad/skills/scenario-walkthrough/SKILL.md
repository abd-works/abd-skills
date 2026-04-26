---
name: scenario-walkthrough
description: >-
  Produce domain-walkthrough.md: indented scenario walks using skills/ooad/templates/domain
  walkthrough template.md; validate each step maps to a class and responsibility from
  crc.md (scenario-validation rules in skills/ooad/content/parts/phases/scenario-validation.md).
  Use business-logic.md for lifecycle guards and invariants when stepping transitions.
  Fix gaps before properties-methods-and-relationships. Input: crc.md, business-logic.md,
  object-sketch.md. Output: abd-ooad/domain-walkthrough.md.
---

# scenario-walkthrough

## Purpose

**Walk** concrete scenarios through the CRC model. Each step must map to a **class** (or role) and a **responsibility** from `crc.md`. When a step crosses a **state change** or must respect a **guard**, align with `business-logic.md` (from **`elaborate-business-logic`**). If a step has no owner, record a **Scenario gap** and revise upstream artifacts.

## Inputs / outputs

| Input | Output |
| --- | --- |
| `abd-ooad/crc.md`, `abd-ooad/business-logic.md`, `abd-ooad/object-sketch.md` | `abd-ooad/domain-walkthrough.md` |

If `business-logic.md` is missing, run **`elaborate-business-logic`** first, or note **Open gap: no business-logic.md** in the walkthrough header.

## Shape

Use `skills/ooad/templates/domain walkthrough template.md` for each scenario: **Purpose**, **Concepts traced**, then **Walk N** with indented pseudocode (`object`, `method`, collaborators).

Minimum coverage (adapt to domain):

- One happy path
- One failure or edge path
- One path involving cooperation or resources (e.g. team check, hero point)

## Rules

- Do not require full lifecycle from upstream; validate **ownership** of each step first.
- When the scenario implies a transition, check **business-logic.md** for illegal edges and invariants.
- Tag-style `term-registry` / `[pN]` notes from stock scenario-validation are **optional** unless the engagement uses them.

## Templates

`templates/domain-walkthrough-scaffold.md`

## Validate

- Every walk line that performs game logic ties to a CRC **Responsible for** line.
- Gaps listed in a **Gaps resolved** or **Open gaps** subsection at file end.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. -->
<!-- execute_rules:bundle_rules:end -->
