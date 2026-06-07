---
name: class-model
catalog_garden_tier: practice
catalog_garden_order: 6
catalogue_one_liner: >-
  Typed Class Model from the domain model; properties, operations, relationships, invariants.
description: >-
  Build a typed Class Model for a module. A domain model makes it faster but is
  not required. Use when a module needs a typed domain surface before writing
  production code, or when a module has reached state: class-model.
---
# abd-domain-implementation

## Purpose

Build a typed Class Model for a module. When a domain model exists it is the primary input — the skill converts that behavioral model into a typed domain surface with far less effort. Without a domain model the skill can still produce an Class Model directly from domain knowledge.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `class-model.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-class-model.md`.

The file is **not** an in-place enrichment of the domain model file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — typed notation: properties, operations, object initialisation, relationships (aggregation/composition/association), collections, inheritance, invariants, interactions, entities and value objects, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-model-scaffold.md` | The Class Model file with typed class blocks under each KA. |
| `templates/domain.json` | Domain JSON with class names, property names (camelCase), and inheritance. |

**Quality bar:** Every property is typed and justified by a domain responsibility. Every operation is a fully typed signature. Every class has object initialisation decided. Composition/aggregation properties carry stereotypes. Subtype blocks carry only deltas. Operations with inherent complexity have `Interaction:` blocks. No operation carries multiple invariants without an `Interaction:`. Variable names in interactions use domain language. State marker set to `domain-model`.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-domain-implementation \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

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
- **State marker** — front matter reads `state: class-model`.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
