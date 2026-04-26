---
name: class-responsibility-collaborator
description: >-
  Class-Responsibility-Collaborator (CRC): produce crc.md from object-sketch.md
  - Responsible for, Not responsible for, Collaborators per type, semi-formal.
  Lean CRC only (no lifecycle or invariants - use elaborate-business-logic after
  this skill). Canon in skills/ooad/content/parts/phases/responsibilities-and-collaborators.md.
  Input: object-sketch.md. Output: abd-ooad/crc.md.
---

# class-responsibility-collaborator

## Purpose

Turn **`object-sketch.md`** sketch heads into a **CRC** list. **Layout:** domain-outline style (see `bots/crc_bot/.../domain_outline.md`): each concept is a **name line**, then four-space-indented **`responsible:`**, **`not_responsible:`**, **`collaborators:`** lines. Subtype / generalization: **`Child : Parent`** on the concept name line. Stereotypes optional (`<< kind? >>` allowed) if the team uses them at CRC stage — default is plain concept names.

**Lifecycle and invariants** are **not** in scope for this skill. After `crc.md` is stable enough for review, run **`elaborate-business-logic`** to add **State / lifecycle** and **Invariants** per stateful class (see `state-and-lifecycle.md` and `invariants.md` in the OOAD skill).

## Inputs / outputs

| Input | Output |
| --- | --- |
| `abd-ooad/object-sketch.md` | `abd-ooad/crc.md` |

Mirror `## Module: [Name]` from the sketch when present.

## Rules

- Derive **Collaborators** from sketch `uses` and subtype edges.
- **Not responsible for** must reject at least one plausible misplaced concern.
- Do not add method signatures here; English only.

## Templates

Primary: `templates/crc-outline-template.md` (outline layout + instructions). Same structural idea as **`agile_bots`** `bots/crc_bot/behaviors/domain/content/render/templates/domain_outline.md`, extended for CRC’s three responsibility lines.

## Validate

- Every sketch **base** that owns mechanics has a CRC block.
- Subtypes either have their own outline block with **`Child : Parent`** on the name line, or an explicit inherit note under the base.
- Older engagements may still use legacy `### Heading` + bold **Responsible for** triplets; new work should prefer **`crc-outline-template.md`**.

## Next step

**`elaborate-business-logic`** - produces `business-logic.md` from `crc.md` + `object-sketch.md` before **`scenario-walkthrough`**.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. -->
<!-- execute_rules:bundle_rules:end -->
