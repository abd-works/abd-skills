---
name: abd-ddd-design-building-blocks
catalog_garden_order: 7
catalogue_one_liner: >-
  Answer the business questions behind identity, consistency, and ownership — so patterns match real rules.
description: >-
  Classify domain concepts with DDD stereotypes by surfacing the business questions behind identity, consistency, and ownership. Use when refining a domain model or applying DDD building blocks.
context-perspective: domain
context-role: support
context-fidelity:
  - level: specification
    mode: building-blocks
---
# abd-ddd-design-building-blocks

## Purpose

Answer the business questions behind identity, consistency, and ownership for each concept — so DDD patterns match real business rules, not developer assumptions.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these:

- **Identity assumption** — Does this concept truly need a persistent identity, or are you giving it one out of habit?
- **Aggregate boundary** — What invariant does this aggregate protect — and can you state it as a business rule, not a database constraint?
- **Value Object hiding** — Are any "entities" actually interchangeable by value — same data means same thing, no lifecycle?
- **Service or misplaced logic** — Is this domain service genuinely homeless, or does the operation belong on an entity you haven't modelled yet?
- **Consistency boundary** — Does the business really need immediate consistency here, or would eventual consistency be acceptable — and who decided?

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File name:** `ddd-building-blocks.md`. Add a `<name>-` prefix only when disambiguation is needed. Placed beside the source model artifact.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — all building block stereotypes (Entity, Value Object, Aggregate, Repository, Factory, Service, Domain Event, Specification), cross-aggregate consistency, the business questions each stereotype surfaces, and source-fidelity guidance.
- **`reference/examples.md`** — a worked domain model before-and-after example showing building blocks applied to an Order domain.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/ddd-building-blocks-template.md` | The building-blocks portrait for every concept — stereotypes, identity rules, aggregate boundaries, events, services, with business questions and rationale. |

**Quality bar:** Every concept from the input model appears with at least one stereotype facet or an explicit Unresolved note. Every stereotype records the business question asked and the answer given. Concepts may express multiple stereotypes (Entity + Aggregate Root + emits Events). Write at the same fidelity as the input source (domain model notation, typed notation, or plain-English concept blocks). Include the source model and show DDD annotations layered on top.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect the building-blocks portrait as a domain expert and architect would.

- **Business questions surfaced** — every stereotype facet records the question asked and answer given.
- **Multi-faceted portraits** — concepts that are Entities AND Aggregate Roots AND emit Events show all facets.
- **Domain expert check** — every concept named in domain language from the source model; no technical jargon introduced.
- **Complete coverage** — every concept from the input model appears with at least one stereotype or an explicit Unresolved note.
- **Identity test applied** — Entity vs Value Object decisions cite the identity question with a domain-grounded answer.
- **Aggregate boundaries defensible** — each aggregate names its root, lists boundary members, and states protected invariants.
- **Services genuinely homeless** — no service could be more naturally placed on an existing Entity or Value Object.
- **Events belong to their Aggregate** — every Domain Event names the raising Aggregate, uses past-tense, and names consumers.
- **No premature infrastructure** — no database tables, message queues, or framework classes prescribed.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
