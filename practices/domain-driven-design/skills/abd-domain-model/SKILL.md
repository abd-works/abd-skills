---
name: abd-domain-model
catalog_garden_tier: practice
catalog_garden_order: 3
catalogue_one_liner: >-
  Make ownership and responsibilities explicit for each concept — so code knows who does what.
description: >-
  Make ownership and responsibilities explicit for each concept — who creates it, who mutates it, what it guards. Use when a Domain Language exists and the team needs to assign responsibilities before writing code.
context-perspective: domain
context-fidelity:
  - level: exploration
    mode: conceptual-model
---
# abd-domain-model

## Purpose

Make ownership and responsibilities explicit for every concept — who creates it, who mutates it, what it guards — so code knows where behavior lives before anyone writes a class.

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File names:**

| File | Role |
| --- | --- |
| `domain-model.md` | Human-readable projection (flat heading shape) |
| `domain-model.json` | Machine-readable spine — `abd-domain-model/v1` schema; parallel to `story-graph.json` |
| `domain.json` | Flat scanner vocabulary index — derived from `domain-model.json` |

Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-domain-model.md` (and matching `.json`).

The files are **not** an in-place enrichment of the domain-language file. They are fresh artifacts in the same flat heading shape every other DDD phase skill uses.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Responsibility ambiguity** — when two concepts could reasonably own the same behavior, which one actually does — and what's the real-world evidence for that choice?
- **Hidden invariants** — which business rules feel so obvious that nobody has stated them — and what breaks downstream if the model doesn't make them explicit?
- **Collaboration direction** — when two concepts interact, which one initiates — and are we sure the direction reflects how the business actually works, not just how we'd code it?
- **Subtype vs. configuration** — when behavior varies by kind, is the variation genuinely structural or is it just a flag — and what happens when a new kind appears?
- **Missing concepts** — are there behaviors assigned to existing concepts that really belong to a concept nobody has named yet — a missing collaborator hiding inside another class?

---

## Diagram workflow

Produces `<deliverables-folder>/domain-model.drawio` (one tab per KA) from `domain-model.md`. Must exist before the cell is marked done.

```bash
python scripts/drawio_domain_cli.py \
  <deliverables-folder>/domain-model.md \
  --output <deliverables-folder>/domain-model.drawio
```

Run once after `domain-model.md` is written. To regenerate, re-run the same command — the markdown is the source of truth.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — domain model format: class blocks, constructor, properties, methods, collaborators, invariants, subtypes, and the consistent file shape.
- **`reference/domain-model-json.md`** — `domain-model.json` schema, containment hierarchy, and upstream mapping from glossary terms and domain-language bullets.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-model-template.md` | The domain model markdown with typed class blocks under each KA. |
| `templates/domain-model-template.json` | The domain model graph (`abd-domain-model/v1`) — Module → KA → Class → Property/Operation. |
| `templates/domain.json` | Flat scanner vocabulary — class names, property names (camelCase), inheritance — derived from `domain-model.json`. |

**Quality bar:** Every behavior bullet from the Domain Language maps to at least one property or method. Properties are typed — never raw `String`; use domain types, constrained enums, or typed primitives. Methods use type-only params (no param names). Hidden collaborators (not in params or return) listed underneath methods, indented, before invariants. No `+` prefix. No stereotypes. No `List<T>` or `Dictionary<K,V>`. No `Interaction:` blocks. Subtype blocks carry only deltas. State marker set to `domain-model`.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Per-phase output file** — named `[<name>-]domain-model.md`. No prior or later phase content lives in it.
- **Every KA has a class that names it** — the KA's own class is listed first under the `## **KA**` heading.
- **Coverage** — every concept from the domain-language file has a corresponding `### **Class**` block.
- **No sub-headings under classes** — class member blocks live directly under each `### **Class**` heading.
- **References per KA** — one `### references` per KA with fenced `source` blocks.
- **Decisions per KA** — one `### decisions made` per KA listing modeling judgment calls.
- **No slash terms** — no `A / B` names in any heading or block.
- **No raw String types** — every type is a domain type, constrained enum, or typed primitive (Timestamp, FilePath, Identifier, etc.).
- **No visibility prefix** — no `+` on properties or methods; `-` for private methods only.
- **No stereotypes** — no `<< Entity >>`, `<< ValueObject >>`, or similar markers.
- **No list or dictionary types** — no `List<T>` or `Dictionary<K,V>`; use inner domain type only.
- **No interaction blocks** — no `Interaction:` pseudocode.
- **No param names** — method signatures use `method(Type, Type): ReturnType`, not `method(param: Type)`.
- **Collaborators before invariants** — indented collaborator lines appear before indented invariant lines.
- **Constructor present** — every class with state has a constructor line before `------`.
- **Separator markers** — `------` between constructor and properties; `----` between properties and methods.
- **Subtype deltas only** — subtype blocks contain only added or overridden members.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
