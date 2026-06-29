---
name: drawio-domain-sync
catalog_garden_order: 7
catalogue_one_liner: >-
  Keep domain diagrams and source models in sync — so the team reads one truth, not two.
description: >-
  Render domain artifacts to Draw.io class diagrams and sync edits back to the source model. Use when the team needs a visual diagram from a domain model or when text and diagram need reconciliation.
context-perspective: domain
context-role: support
context-fidelity:
  - level: specification
    mode: diagram-sync
---
# drawio-domain-sync

## Purpose

Keep domain diagrams and source models in sync — so the team reads one truth, not two.

---

## Agent Instructions

**MANDATORY:** [`common/reference/skill-workflow.md`](../../../../../common/reference/skill-workflow.md) — read in full; complete § Bootstrap and § Read-gates before generating or validating.

## Bootstrap

§ Bootstrap — [`common/reference/skill-workflow.md`](../../../../../common/reference/skill-workflow.md).

Also read:
- **`common/reference/agentic-repair-loop.md`** — eval loop: archive evals folder, write `violations.md`, capture fail/pass fixtures, iterate until all scanners pass.
- **`common/reference/manual-repair-loop.md`** — log a user-fixed issue back into eval fixtures (fail + pass + cases.json) without running the agentic loop.
- **`reference/repair-tips.md`** — drawio-specific fix patterns (edge routing corridors, anchor placement, drawio_tools API) — read before writing any fix script.

## Read

§ Read-gates — all of [`rules/`](rules/), [`reference/`](reference/), [`templates/`](templates/).

## Input traps

[`reference/input-traps.md`](reference/input-traps.md).

## Grill me

[`reference/grill-me.md`](reference/grill-me.md) — only when the invocation includes "grill me".

## Generate

[`reference/generate.md`](reference/generate.md).

When audit finds definitive violations, follow **`common/reference/agentic-repair-loop.md`**. Read **`reference/repair-tips.md`** before writing any fix code.

## Validate

[`common/reference/rule-checklist.md`](../../../../../common/reference/rule-checklist.md).

## Diagram workflow

[`reference/diagram-workflow.md`](reference/diagram-workflow.md).

## Output

[`reference/output.md`](reference/output.md).
