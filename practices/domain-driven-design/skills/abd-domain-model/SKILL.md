---
name: domain-model
catalog_garden_tier: practice
catalog_garden_order: 5
catalogue_one_liner: >-
  Typed domain model from Domain Language; constructors, properties, methods, collaborators, invariants.
description: >-
  Build a typed domain model for a module — constructors, typed properties,
  method signatures, hidden collaborators, and invariants in one pass.
  Combines domain model responsibility assignment with typed notation but without
  class-model embellishments (no stereotypes, no interaction blocks, no
  list types, no param names). Use when a completed Domain Language
  exists and the user asks to "build the domain model", "run domain model",
  "assign responsibilities", or when ownership, boundaries, and typed
  surface need to be made explicit before writing code.
---
# abd-domain-model

## Purpose

This skill takes domain concepts from a completed Domain Language and produces a typed domain model: for each concept, a constructor, typed properties, method signatures with collaborators and invariants. The result is a standalone file with `### **Class**` blocks under each Key Abstraction.

The format sits between domain model and a full Class Model — it uses typed notation (constructors, property types, method signatures) but avoids class-model embellishments (no `<< stereotypes >>`, no `List<T>` or `Dictionary<K,V>`, no `Interaction:` blocks, no `+` visibility prefixes, no param names in method signatures).

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `domain-model.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-domain-model.md`.

The file is **not** an in-place enrichment of the domain-language file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — domain model format: class blocks, constructor, properties, methods, collaborators, invariants, subtypes, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-model-template.md` | The domain model file with typed class blocks under each KA. |
| `templates/domain.json` | Domain JSON with class names, property names (camelCase), and inheritance. |

**Quality bar:** Every behavior bullet from the Domain Language maps to at least one property or method. Properties are typed — never raw `String`; use domain types, constrained enums, or typed primitives. Methods use type-only params (no param names). Hidden collaborators (not in params or return) listed underneath methods, indented, before invariants. No `+` prefix. No stereotypes. No `List<T>` or `Dictionary<K,V>`. No `Interaction:` blocks. Subtype blocks carry only deltas. State marker set to `domain-model`.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-domain-model \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

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
- **State marker** — front matter reads `state: domain-model`.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
