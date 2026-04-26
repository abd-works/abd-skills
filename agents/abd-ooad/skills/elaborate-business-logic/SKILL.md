---
name: elaborate-business-logic
description: >-
  After CRC, elaborate state/lifecycle and declarative invariants per stateful class
  (skills/ooad/content/parts/phases/state-and-lifecycle.md and invariants.md).
  Input: crc.md, object-sketch.md. Output: abd-ooad/business-logic.md. Run before
  scenario-walkthrough so walks can reference guards and always-true rules.
---

# elaborate-business-logic

## Purpose

**Second pass after lean CRC:** for each class in `crc.md` that owns **state changes**, **threshold ladders**, **supersession**, **spend/recover**, or other **lifecycle-shaped** mechanics, add:

1. **State / lifecycle** - Named states, allowed transitions, illegal transitions (one line each), terminal states where relevant.
2. **Invariants** - Short **declarative** rules ("must", "cannot", "only if") that the type enforces - not procedures. Tie each to a state or transition when obvious.

**Invariants** are the **constraints that make transitions legal** and the **facts that must remain true** in each state; they are a subset of the lifecycle picture.

Skip a class subsection entirely when it is **stateless** in the source and has no mechanics bullets that imply always-true constraints.

## Pipeline position

| Before | This skill | After |
| --- | --- | --- |
| `class-responsibility-collaborator` (`crc.md`) | `business-logic.md` | `scenario-walkthrough` |

## Inputs / outputs

| Input | Output |
| --- | --- |
| `abd-ooad/crc.md`, `abd-ooad/object-sketch.md` | `abd-ooad/business-logic.md` |

Mirror `## Module: [Name]` from `crc.md` when present.

## Canon

- **State / lifecycle** - `skills/ooad/content/parts/phases/state-and-lifecycle.md`
- **Invariants (p9)** - `skills/ooad/content/parts/phases/invariants.md`

## Rules

- Only elaborate classes that **appear in crc.md**; do not introduce new types here.
- English only; no method signatures (those belong to **properties-methods-and-relationships**).
- Derive detail from **mechanics bullets** and carry-forward extracts in `object-sketch.md`, not from inventing rules.

## Templates

Use `templates/business-logic-module-template.md` per module section.

## Validate

- Every CRC class that the sketch marks as stateful (or that has mechanics implying state) has either a **State / lifecycle** block or an explicit **(stateless - no lifecycle block)** line.
- For classes with a **State / lifecycle** block, at least one **Invariant** line **or** explicit **(none yet)**.
- No duplicate of CRC **Responsible for** / **Collaborators** prose - only lifecycle and invariant elaboration.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. -->
<!-- execute_rules:bundle_rules:end -->
