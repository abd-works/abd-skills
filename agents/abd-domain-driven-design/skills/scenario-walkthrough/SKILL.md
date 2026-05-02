---
name: scenario-walkthrough
description: >-
  Produce domain-walkthrough.md: indented scenario walks where every step maps to a
  class and responsibility from crc.md; lifecycle guards and invariants come from the
  CRC lifecycle fields. Fix gaps before object-model. Input: crc.md, domain-sketch.md.
  Output: abd-domain-driven-design/domain-walkthrough.md.
---

# scenario-walkthrough

## Purpose

**Walk** concrete scenarios through the CRC model. Each step must map to a **class** (or role) and a **responsibility** from `crc.md`. When a step crosses a **state change** or must respect a **guard**, align with the `lifecycle:` and `invariants:` fields in the CRC block for that concept. If a step has no owner, record a **Scenario gap** and revise upstream artifacts.

## Inputs / outputs

| Input | Output |
| --- | --- |
| `abd-domain-driven-design/crc.md`, `abd-domain-driven-design/domain-sketch.md` | `abd-domain-driven-design/domain-walkthrough.md` |

## Shape

Use `skills/ooad/templates/domain walkthrough template.md` for each scenario: **Purpose**, **Concepts traced**, then **Walk N** with indented pseudocode (`object`, `method`, collaborators).

Minimum coverage (adapt to domain):

- One happy path
- One failure or edge path
- One path involving cooperation or resources (e.g. team check, hero point)

## Rules

- Do not require full lifecycle from upstream; validate **ownership** of each step first.
- When the scenario implies a transition, check the concept's **`lifecycle:`** field in `crc.md` for illegal edges and invariants.
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
