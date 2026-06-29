---
catalog_garden_tier: practice
catalog_garden_order: 40
name: abd-architecture-specification
catalogue_one_liner: >-
  Tell engineers exactly how domain concepts become files, classes, and tests in a chosen stack.
description: >-
  Specify how domain concepts and stories map to files, classes, and tests in a chosen stack. Use when starting or extending an architecture spec for a project.
context-perspective: architecture
context-fidelity:
  - level: exploration
    mode: document
  - level: specification
    mode: template
---
# abd-architecture-specification

## Purpose

Tell engineers exactly how domain concepts and stories become files, classes, and tests in a chosen stack — so agents know exactly how to generate working code for a domain and story that follows the architecture.

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
