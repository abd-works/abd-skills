# Domain Model JSON — Schema and upstream mapping

Machine-readable spine for the domain model perspective. Parallel to `story-graph.json` for stories and `domain-model.md` for human-readable projection.

**Canonical file:** `docs/domain/model/domain-model.json`  
**Schema:** `abd-domain-model/v1`

---

## Containment hierarchy

```text
domain-model.json
└── modules[]
    ├── relationships[]             ← cross-KA / module-wide (sibling to key_abstractions)
    ├── key_abstractions[]          ← KA (Key Abstraction)
    │   ├── relationships[]         ← within-KA class relationships (sibling to classes)
    │   ├── classes[]
    │   │   ├── properties[]        ← return_type, invariants, optional interaction
    │   │   └── operations[]        ← params, return_type, collaborators, invariants, optional interaction
    │   ├── references[]
    │   └── decisions[]
    └── boundary_domain
        ├── relationships[]
        ├── classes[]
        ├── references[]
        └── decisions[]
```

**Relationships sit outside classes** — they are first-class siblings at module, KA, or boundary scope. A class does not own its relationship list; the relationship names both ends explicitly.

Same depth as `story-graph.json`:

| Story graph | Domain model |
| --- | --- |
| `product` | `product` |
| `epics[]` | `modules[]` |
| `sub_epics[]` | `key_abstractions[]` |
| `stories[]` | `classes[]` |
| `acceptance_criteria[]` / `scenarios[]` | `properties[]` / `operations[]` |
| *(cross-story links)* | `relationships[]` at module or KA scope |

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
| `intro` | no | Module-level intro paragraph carried from markdown (longer prose; `scope` stays for the short label) |
| `core_terms` | no | Flat term list (from glossary **Core terms** / **Terms**) |
| `relationships` | yes | Cross-KA relationships between classes in this module (may be empty) |
| `key_abstractions` | yes | KA groups under **Core Domain** |
| `boundary_domain` | yes | Scoped boundary classes and their relationships. May carry an `intro` string for the Boundary Domain section prose |

---

## Key abstraction (KA)

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | KA name (matches `## KAName` in markdown) |
| `definition` | yes | KA intro paragraph — the term definition for the KA |
| `relationships` | yes | Relationships between classes in this KA (may be empty) |
| `classes` | yes | All classes owned by this KA |
| `references` | yes | Source refs for this KA (may be empty) |
| `decisions` | yes | Modeling decisions for this KA (may be empty) |

---

## Relationship

Declared at **module**, **KA**, or **boundary_domain** scope — never nested inside a class.

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Relationship name (domain language, e.g. `"resolved using"`, `"carries"`) |
| `kind` | yes | `"association"`, `"aggregation"`, or `"composition"` |
| `ends` | yes | Exactly two ends — both classes, roles, and cardinalities |

### Relationship end

| Field | Required | Meaning |
| --- | --- | --- |
| `class` | yes | PascalCase class name at this end |
| `role` | yes | Role name at this end (camelCase noun from domain vocabulary) |
| `cardinality` | yes | One of `1..1`, `0..1`, `1..*`, `0..*` |

**Placement rules:**

| Scope | Use when |
| --- | --- |
| `modules[].relationships[]` | Both classes may span different KAs within the module |
| `key_abstractions[].relationships[]` | Both classes live under the same KA |
| `boundary_domain.relationships[]` | Boundary class relates to a core-domain class |

**Direction:** the class that lists a collaborator in the domain model is the navigating end. Cardinality on each end is independent.

Example:

```json
{
  "name": "carries",
  "kind": "composition",
  "ends": [
    { "class": "Trait", "role": "trait", "cardinality": "1..1" },
    { "class": "Rank", "role": "rank", "cardinality": "1..1" }
  ]
}
```

Markdown equivalent (domain specification): `Trait *composes* Rank [1..1 ↔ 1..1]`.

---

## Class

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | PascalCase class name |
| `ka_anchor` | yes | `true` for the class that names the KA (listed first) |
| `term` | yes | Glossary / domain-language term this class came from |
| `extends` | yes | Parent class name for subtypes, or `null` |
| `constructor` | yes | `{ "parameter_types": ["Type", ...], "parameters": [{"name", "type"}]? }` |
| `properties` | yes | Typed state (may be empty) |
| `operations` | yes | Behavior (may be empty) |
| `stereotype` | no | One of `Entity`, `ValueObject`, `Service`, `Factory`, `Repository`, `DomainEvent`, `Boundary`. Lifted from `<< Stereotype >>` markers in markdown |
| `stereotype_note` | no | Free-text qualifier following the stereotype (e.g. `"Identity Provider — AWS IAM"` from `<< Service >> [Identity Provider — AWS IAM]`) |
| `initialisation` | no | Free-text initialisation paragraph (e.g. `"AWS Amplify singleton — configured at app bootstrap"`) |
| `note` | no | Free-text note carried from `Note:` lines in markdown |
| `owned_by` | boundary only | Owning module for boundary classes |

**Subtypes:** set `extends` to the parent class name. The child block carries **delta members only** — same rule as `### ChildClass : ParentClass` in markdown.

Omit `constructor` or use `"parameter_types": []` when the class has no constructor. When named parameters are known (specification fidelity), populate `constructor.parameters` as well — `parameter_types` stays populated for back-compat.

### Stereotype canonical list

`Entity`, `ValueObject`, `Service`, `Factory`, `Repository`, `DomainEvent`, `Boundary`.

Project-invented stereotypes (e.g. `ProxyController`) must be normalised to one of the canonical names with the original name preserved in `stereotype_note` or in `domain-context.md` at the module root.

---

## Property

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | camelCase property name |
| `return_type` | yes | Domain type, constrained enum, or typed primitive — never raw `String` |
| `invariants` | yes | Declarative constraints (may be empty) |
| `interaction` | no | Array of strings and/or structured steps — **may be strings only** |
| `note` | no | Free-text note carried from `Note:` lines in markdown |
| `language_bullets` | no | Traceability back to domain-language bullets |

Properties use `return_type` (not `type`) for parity with operations.

When a property's `return_type` references another class, the corresponding `relationships[]` entry at KA or module scope declares kind and cardinality. The property and the relationship are complementary — not duplicates.

---

## Operation

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | camelCase method name |
| `parameter_types` | yes | Types only — no parameter names |
| `parameters` | no | `[{name, type}]` — named params at specification fidelity. Parallel to `parameter_types` |
| `return_type` | yes | Return type; use `void` for commands with no return |
| `visibility` | yes | `"public"` or `"private"` (`-` prefix in markdown) |
| `collaborators` | yes | Hidden domain types not in params or return (may be empty) |
| `invariants` | yes | Declarative constraints (may be empty) |
| `interaction` | no | Array of strings and/or structured steps — **may be strings only** |
| `phase` | no | Free-text grouping label lifted from `**<Phase> operations**:` headers in markdown (e.g. `"onboarding"`, `"self-care"`) |
| `note` | no | Free-text note carried from `Note:` lines in markdown |
| `language_bullets` | no | Traceability back to domain-language behavior bullets |

---

## Interaction

Optional **array** on **properties** and **operations**. Each element is **either**:

1. A **plain string** — simplest form; use whenever it reads clearly
2. A structured **operation call** — `{ return_type, object, operation, params? }`
3. A structured **property access** — `{ return_type, property }`

The entire `interaction` array may be strings only — structured objects are optional, not required.

```json
"interaction": [
  "roll: Integer = d20.roll()",
  "rollTotal = roll + trait.rank.toModifier().value + circumstanceModifier.value",
  "return result"
]
```

Omit `interaction` when behavior is a simple delegation, a direct property read, or fully captured by signature + a single invariant.

### String step (preferred when sufficient)

A single domain-spec line — assignment, comparison, or return:

```json
"rollTotal = roll + modifier.value + circumstanceModifier.value"
"return result"
```

### Structured step — operation call (optional)

`object.operation(params)` — call an operation on a domain object.

| Field | Required | Meaning |
| --- | --- | --- |
| `return_type` | yes | Type produced by this step |
| `object` | yes | Domain-language object (variable, `self`, or class name for construction) |
| `operation` | yes | Operation name on that object |
| `params` | no | Argument expressions (may be empty) |

```json
{ "return_type": "Integer", "object": "d20", "operation": "roll", "params": [] }
```

Maps to domain-spec pseudocode: `roll: Integer = d20.roll()`.

### Structured step — property access (optional)

| Field | Required | Meaning |
| --- | --- | --- |
| `return_type` | yes | Type of the property value |
| `property` | yes | Property path (e.g. `trait.rank.toModifier`) |

```json
{ "return_type": "Modifier", "property": "trait.rank.toModifier" }
```

Use **either** `object` + `operation` + `params` **or** `property` on a structured step — not both. Prefer a **string** when the line is easier to read as text.

### Mixed example (`Check.resolve`)

```json
"interaction": [
  { "return_type": "Integer", "object": "d20", "operation": "roll", "params": [] },
  { "return_type": "Modifier", "property": "trait.rank.toModifier" },
  "rollTotal = roll + modifier.value + circumstanceModifier.value",
  "success = rollTotal >= difficultyClass.value",
  { "return_type": "CheckResult", "object": "CheckResult", "operation": "new", "params": ["success", "margin"] },
  "return result"
]
```

**Collaborator accounting:** every type in `collaborators[]` must appear in `parameter_types`, `return_type`, a property `return_type`, or an interaction step (`object`, `property`, or string). Unaccounted collaborators are modeling gaps.

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

| Upstream | JSON |
| --- | --- |
| `### term` under a KA | `classes[].term` = term name |
| KA's own term | `ka_anchor: true` on the matching class |
| `### Subtype *is a type of* Base` | `extends: "Base"` on the child class |
| `### term *(boundary)*` | `boundary_domain.classes[]` with `owned_by` |

### Domain-language bullet → property or operation

| Language bullet pattern | JSON target |
| --- | --- |
| `is a … of *parent*` / `has …` / `carries …` | `properties[]` with `return_type` |
| `is resolved by …` / `produces …` / behavior verb | `operations[]` |
| `**Invariant:**` line | `invariants[]` on the nearest property or operation |
| Cross-class dependency in bullets | `relationships[]` at KA or module scope |

**Collaborators** on operations are inferred from *italicized* class names in bullets. **Relationships** are declared separately at KA/module scope with both ends, kind, roles, and cardinalities.

### Domain specification projection

When promoting to class-model / domain-specification fidelity:

| domain-model.json | domain-specification |
| --- | --- |
| `properties[].return_type` | `+ property: ReturnType` |
| `operations[].interaction` | tab-indented `Interaction:` block |
| `relationships[]` | relationship lines with cardinality |
| `extends` | `### Child : Parent` heading |

---

## Semantic pointer (for context-graph)

```text
modules/Check Resolution/relationships/resolved using
modules/Check Resolution/key_abstractions/Trait/relationships/carries
modules/Check Resolution/key_abstractions/Trait/classes/Rank
modules/Check Resolution/key_abstractions/Check/classes/OpposedCheck
```

---

## Templates

Practice-wide artifacts live under `practices/domain-driven-design/references/`:

| File | Purpose |
| --- | --- |
| `references/domain-model-template.json` | Placeholder scaffold with `{{tokens}}` |
| `references/domain-model-outline.json` | Minimal valid graph with KA-level relationship |
| `references/domain-model-example.json` | Filled Check Resolution example |
| `references/domain-model-json.md` | This document |
| `skills/supporting/domain-ops/` | `domain-ops` — CLI, validation, persistence (`domain_graph_cli.py`) |

## domain-ops

After creating or editing `domain-model.json`, validate with **domain-ops**:

```bash
export PYTHONPATH="practices/domain-driven-design/skills/supporting/domain-ops/scripts"
python3 practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py read --file docs/domain/model/domain-model.json
```

See `skills/supporting/domain-ops/SKILL.md`.

---

## Relationship to delivery-graph solution

This file is the **domain view spine** described in `docs/delivery-graph-solution.md`. Canonical name is **`domain-model.json`** to mirror `domain-model.md` and `story-graph.json` naming.
