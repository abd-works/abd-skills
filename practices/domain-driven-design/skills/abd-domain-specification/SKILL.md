---
name: abd-domain-specification
catalog_garden_tier: practice
catalog_garden_order: 4
catalogue_one_liner: >-
  Lock down types, relationships, and invariants — so code generation starts from a verified design.
description: >-
  Lock down types, relationships, and invariants at any scope — so code generation starts from a verified design. Use when a verified typed surface is needed before writing code.
context-perspective: domain
context-fidelity:
  - level: specification
    mode: typed-model
---
# abd-domain-specification

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Type precision** — which properties are typed as generic primitives when the domain actually constrains them — where does "string" hide a real domain type with its own rules?
- **Relationship ownership** — when two concepts reference each other, which one owns the relationship — and what happens to the dependent when the owner changes or disappears?
- **Cross-concept invariants** — which business rules span multiple classes — and where does the enforcement logic actually live when no single class owns the whole rule?
- **Interaction completeness** — for operations with multiple steps, are we confident we know every participant — or are there hidden collaborators the sequence depends on?
- **Identity assumptions** — which concepts have identity and which don't — and what breaks if something we treat as a value actually needs to be tracked individually?

---

## Purpose

Build a typed Class Model for a module — fully typed properties, operations with parameters, relationships, object initialisation, and interaction blocks — from a domain model or directly from domain knowledge.

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File name:** `class-model.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-class-model.md`.

The file is **not** an in-place enrichment of the domain model file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — typed notation: properties, operations, object initialisation, relationships (aggregation/composition/association), collections, inheritance, invariants, interactions, entities and value objects, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-model-scaffold.md` | The Class Model file with typed class blocks under each KA. |
| `templates/domain.json` | Domain JSON with class names, property names (camelCase), and inheritance. |

**Quality bar:** Every property is typed and justified by a domain responsibility. Every operation is a fully typed signature. Every class has object initialisation decided. Composition/aggregation properties carry stereotypes. Subtype blocks carry only deltas. Operations with inherent complexity have `Interaction:` blocks. No operation carries multiple invariants without an `Interaction:`. Variable names in interactions use domain language. State marker set to `domain-model`.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Per-phase output file** — named `[<name>-]class-model.md`. No prior or later phase content lives in it.
- **Every KA has a class that names it** — `### **Class** << Stereotype >>` matching the KA, listed first.
- **No sub-headings under classes** — class member blocks live directly under each `### **Class**` heading.
- **References per KA** — one `### references` per KA with fenced `source` blocks.
- **Decisions per KA** — one `### decisions made` per KA listing class-model judgment calls.
- **Every property typed** — justified by a domain responsibility that requires stored state.
- **Every operation fully typed** — `+ methodName(param: Type): ReturnType`.
- **Object initialisation decided** — constructor, internal, factory method, or factory object.
- **Relationship stereotypes present** — `<< composition >>` or `<< aggregation >>` on owning properties.
- **Subtype deltas only** — no inherited members repeated.
- **Interactions present where needed** — no operation with multiple invariants lacks an `Interaction:` block.
- **Domain-language variable names** — no generic placeholders in `Interaction:` blocks.
- **All domain model collaborators accounted for** — in parameters, return types, properties, or `Interaction:` steps.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
