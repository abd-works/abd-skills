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

## Agent Instructions

**MANDATORY:** [`common/reference/skill-workflow.md`](../../../../../common/reference/skill-workflow.md) — read in full; complete § Bootstrap and § Read-gates before generating or validating.

## Bootstrap

§ Bootstrap — [`common/reference/skill-workflow.md`](../../../../../common/reference/skill-workflow.md).

## Read

§ Read-gates — all of [`rules/`](rules/), [`reference/`](reference/), [`templates/`](templates/).

## Input traps

[`reference/input-traps.md`](reference/input-traps.md).

## Grill me

[`reference/grill-me.md`](reference/grill-me.md) — only when the invocation includes "grill me".

## Generate

[`reference/generate.md`](reference/generate.md).

## Validate

[`common/reference/rule-checklist.md`](../../../../../common/reference/rule-checklist.md).
