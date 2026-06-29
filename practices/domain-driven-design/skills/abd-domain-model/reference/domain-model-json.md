# Domain Model JSON — Schema and upstream mapping

Machine-readable spine for the domain model perspective. Parallel to `story-graph.json` for stories and `domain-model.md` for human-readable projection.

**Canonical file:** `docs/domain/model/domain-model.json`  
**Schema:** `abd-domain-model/v1`

---

## Containment hierarchy

```text
domain-model.json
└── modules[]
    ├── key_abstractions[]          ← KA (Key Abstraction)
    │   ├── classes[]
    │   │   ├── properties[]
    │   │   └── operations[]
    │   ├── references[]
    │   └── decisions[]
    └── boundary_domain
        ├── classes[]
        ├── references[]
        └── decisions[]
```

Same depth as `story-graph.json`:

| Story graph | Domain model |
| --- | --- |
| `product` | `product` |
| `epics[]` | `modules[]` |
| `sub_epics[]` | `key_abstractions[]` |
| `stories[]` | `classes[]` |
| `acceptance_criteria[]` / `scenarios[]` | `properties[]` / `operations[]` |
| `increments[]` | *(no direct equivalent — boundary_domain is a sibling section)* |

---

## Root fields

| Field | Required | Meaning |
| --- | --- | --- |
| `schema` | yes | Always `"abd-domain-model/v1"` |
| `product` | yes | System or product name |
| `scope` | yes | Engagement or bounded-slice scope |
| `modules` | yes | One or more module trees |

---

## Module

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Module name (matches `# Module: [Name]` in markdown) |
| `scope` | no | Module-specific scope when different from root |
| `core_terms` | no | Flat term list (from glossary **Core terms** / **Terms**) |
| `key_abstractions` | yes | KA groups under **Core Domain** |
| `boundary_domain` | yes | Scoped boundary classes (may be empty) |

---

## Key abstraction (KA)

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | KA name (matches `## KAName` in markdown) |
| `definition` | yes | KA intro paragraph — the term definition for the KA |
| `classes` | yes | All classes owned by this KA |
| `references` | yes | Source refs for this KA (may be empty) |
| `decisions` | yes | Modeling decisions for this KA (may be empty) |

---

## Class

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | PascalCase class name |
| `ka_anchor` | yes | `true` for the class that names the KA (listed first) |
| `term` | yes | Glossary / domain-language term this class came from |
| `extends` | yes | Parent class name, or `null` |
| `constructor` | yes | `{ "parameter_types": ["Type", ...] }` — types only, no param names |
| `properties` | yes | Typed state (may be empty) |
| `operations` | yes | Behavior (may be empty) |
| `owned_by` | boundary only | Owning module for boundary classes |

Omit `constructor` or use `"parameter_types": []` when the class has no constructor.

---

## Property

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | camelCase property name |
| `type` | yes | Domain type, constrained enum, or typed primitive — never raw `String` |
| `invariants` | yes | Declarative constraints (may be empty) |
| `language_bullets` | no | Traceability back to domain-language bullets |

---

## Operation

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | camelCase method name |
| `parameter_types` | yes | Types only — no parameter names |
| `return_type` | yes | Return type; use `void` for commands with no return |
| `visibility` | yes | `"public"` or `"private"` (`-` prefix in markdown) |
| `collaborators` | yes | Hidden domain types not in params or return (may be empty) |
| `invariants` | yes | Declarative constraints (may be empty) |
| `language_bullets` | no | Traceability back to domain-language behavior bullets |

---

## Reference

| Field | Required | Meaning |
| --- | --- | --- |
| `title` | yes | Ref title |
| `source` | yes | Source file path |
| `locator` | yes | Line range or section pointer |
| `extract` | yes | `"whole"` or `"partial"` |

---

## Upstream mapping

### Glossary term → class

When a glossary or domain-language **term** is modeled as a **class** (not a pure property or subtype heading only):

| Upstream | JSON |
| --- | --- |
| `### term` under a KA | `classes[].term` = term name |
| KA's own term | `ka_anchor: true` on the matching class |
| `### Subtype *is a type of* Base` | `extends: "Base"` on the child class |
| `### term *(boundary)*` | `boundary_domain.classes[]` with `owned_by` |

Terms that stay **properties only** (e.g. *d20* on *check*) do not get a separate class — they appear as `properties[]` on the owning class.

### Domain-language bullet → property or operation

Domain-language structure maps **one-for-one** except **relations and who-does-what**:

| Language bullet pattern | JSON target |
| --- | --- |
| `is a … of *parent*` / `has …` / `carries …` | `properties[]` on the concept's class |
| `is resolved by …` / `produces …` / behavior verb | `operations[]` on the concept's class |
| `**Invariant:**` line | `invariants[]` on the nearest property or operation |
| Pure property with no independent behavior | property on parent class only — no separate class |

**Collaborators** (`collaborators[]` on operations) and **who initiates** are **not** copied from language prose. Infer them from *italicized* class names mentioned in the bullet text — every domain type referenced in a behavior bullet that is not already in `parameter_types` or `return_type` becomes a collaborator.

Example:

```text
- is resolved by *rolling* a *d20*, adding the *trait rank* … comparing … to the *difficulty class*
```

→ `operations[].collaborators`: `["Trait", "DifficultyClass", "D20"]` (types already in signature are not repeated).

### domain.json (scanner vocabulary)

`domain.json` remains a **flat index** derived from this graph:

```json
{
  "concepts": {
    "Check": {
      "attributes": ["d20", "difficultyClass", "trait"],
      "inherits": null
    },
    "OpposedCheck": {
      "attributes": [],
      "inherits": "Check"
    }
  }
}
```

Generate `domain.json` from `domain-model.json` — do not hand-maintain both independently.

---

## Semantic pointer (for context-graph)

Name-based locator within the file (same convention as `story-graph.json`):

```text
modules/Check Resolution/key_abstractions/Trait/classes/Rank
modules/Catalog/boundary_domain/classes/PowerEffect
```

---

## Templates

| File | Purpose |
| --- | --- |
| `templates/domain-model-template.json` | Placeholder scaffold with `{{tokens}}` |
| `templates/domain-model-outline.json` | Minimal valid empty-ish graph |
| `templates/domain-model-example.json` | Filled Check Resolution example |

---

## Relationship to delivery-graph solution

This file is the **domain view spine** described in `docs/delivery-graph-solution.md` (there named `domain-graph.json`). Canonical name in the scaffold is **`domain-model.json`** to mirror `domain-model.md` and `story-graph.json` naming.
