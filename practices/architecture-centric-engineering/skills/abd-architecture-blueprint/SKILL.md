---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-architecture-blueprint
catalogue_one_liner: >-
  Show what every mechanism and module means in code — so the whole team sees what a change touches.
description: >-
  Name every mechanism's code constraint and every module's scope so the team sees what a change touches. Use when deepening an outline into build-ready architecture.
context-perspective: architecture
context-fidelity:
  - level: discovery
    mode: blueprint
---
# abd-architecture-blueprint

## Purpose

Make architecture legible by naming every mechanism that constrains how code is built, listing every module with its business scope and dependencies, and defining diagrams that show how requests flow through mechanisms at runtime — including test flow.

---

## Agent Instructions

**MANDATORY:** [`common/reference/skill-workflow.md`](../../../../common/reference/skill-workflow.md) — read in full; complete § Bootstrap and § Read-gates before generating or validating.

## Bootstrap

§ Bootstrap — [`common/reference/skill-workflow.md`](../../../../common/reference/skill-workflow.md).

## Read

§ Read-gates — all of [`rules/`](rules/), [`reference/`](reference/), [`templates/`](templates/).

## Input traps

[`reference/input-traps.md`](reference/input-traps.md) — pre-flight in every run, not grill-only.

## Grill me

[`reference/grill-me.md`](reference/grill-me.md) — only when the invocation includes "grill me".

## Generate

[`reference/generate.md`](reference/generate.md).

## Validate

[`common/reference/rule-checklist.md`](../../../../common/reference/rule-checklist.md).

## Diagram workflow

[`reference/diagram-workflow.md`](reference/diagram-workflow.md).
