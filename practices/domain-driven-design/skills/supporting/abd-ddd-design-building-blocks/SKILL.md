---
name: ddd-design-building-blocks
catalog_garden_tier: practice
catalog_garden_order: 7
catalogue_one_liner: >-
  DDD stereotypes (Entity, VO, Aggregate, Service, Event) from domain model artifacts.
description: >-
  Surface the business questions that DDD building block stereotypes encode —
  identity, consistency boundaries, ownership, and integration — and classify
  each domain concept (Entity, Value Object, Aggregate, Service, Domain Event)
  from a domain model, Class Model, or Domain Language.
  Use when refining a domain model with DDD stereotypes, answering identity or
  consistency questions, or when the user asks to "apply DDD building blocks"
  or "classify domain concepts."
---
# abd-ddd-design-building-blocks

## Purpose

This skill works through a domain model concept by concept, identifying the right technical constraints through a set of questions that — while technical in framing — can only be answered by business requirements. For example: if two patients have the same name and date of birth, should we consider them the same patient? If a product changes, when do we update the inventory system?

Every DDD building block — Entity, Value Object, Aggregate, Service, Domain Event — looks technical but **exposes a question only the business can answer**. This skill models these elements by understanding business requirements for identity semantics, consistency boundaries, immutability guarantees, and integration contracts across business concepts and systems.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `ddd-building-blocks.md`. Add a `<name>-` prefix only when disambiguation is needed. Placed beside the source model artifact.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — all building block stereotypes (Entity, Value Object, Aggregate, Repository, Factory, Service, Domain Event, Specification), cross-aggregate consistency, the business questions each stereotype surfaces, and source-fidelity guidance.
- **`reference/examples.md`** — a worked domain model before-and-after example showing building blocks applied to an Order domain.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/ddd-building-blocks-template.md` | The building-blocks portrait for every concept — stereotypes, identity rules, aggregate boundaries, events, services, with business questions and rationale. |

**Quality bar:** Every concept from the input model appears with at least one stereotype facet or an explicit Unresolved note. Every stereotype records the business question asked and the answer given. Concepts may express multiple stereotypes (Entity + Aggregate Root + emits Events). Write at the same fidelity as the input source (domain model notation, typed notation, or plain-English concept blocks). Include the source model and show DDD annotations layered on top.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-ddd-design-building-blocks \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

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
