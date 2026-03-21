# Integrate and Harmonize

## Purpose

Unify naming, wire cross-module relationships, resolve `[cross-cutting]` items, and finalize subtypes/enums. Produces a clean, consistent scaffold ready for evidence extraction.

### Domain + story map — relevant excerpts only (full specs: **`parts/domain.md`**, **`parts/story-map.md`**)

*Domain (integrate pass):*

- **Synonym merge:** one **`concepts[].name`**; **union** **`chunk_ids`** / **`chunk_evidence`**; if a merged concept had **`extends`**, ensure the parent **`name`** still exists or repoint **`extends`** after renames (**`parts/domain.md`** — naming + scaffold extensions).
- **Cross-module wiring:** **`depends_on`**, **`provides_concepts`**, and any **`relationships`** stay consistent with **`parts/domain.md`** module boundaries; new shared concepts get **`owns`** + evidence (**`concepts-must-have-owns`**).
- **Subtypes / enums:** align **`extends`** trees and **`EnumType {…}`** property types with finalized decisions (**`parts/domain.md`** — property types).

*Story map (integrate pass):*

- After **moving or renaming** a concept, scan epics/sub-epics/stories: every **`**Concept**`** reference must match a surviving **`concepts[].name`** in the right module (**`parts/story-map.md`** — *Domain Grounding*; scanner **`domain-interaction-sync`**).
- **Hierarchy 4–9** still holds after regrouping (**`parts/story-map.md`** — *Hierarchy* + **`hierarchy-approximately-4-to-9-children`**).

---

## Inputs

- `map-model-spec.json` — deepened output from **[Concept Classes and Stories](../../process.md)** (Stage 2)
- `mms-chunk-index.json` — reverse chunk index

---

## Tasks

1. **Unify naming** — Resolve synonyms, standardize terminology across modules. Ensure concept names are consistent where they refer to the same thing.

2. **Wire cross-module relationships** — For each `[cross-cutting]` item in `cross_cutting_notes`: assign to a primary module or create a shared module; add explicit `relationships` between concepts across modules.

3. **Resolve [cross-cutting]** — Move resolved items out of `cross_cutting_notes`. Document decisions in `open_questions` if human input was needed.

4. **Finalize subtypes and enums** — For deferred subtype candidates: create subtype concepts or confirm enum. For enum decisions: ensure `EnumType {val1, val2}` is applied consistently.

---

## Rules

These rules apply after canonicalization. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Cross-cutting resolved
*Scanner: `scripts/scanners/cross_cutting_resolved.py` → Rule: `cross-cutting-resolved.md`*

**DO** resolve every item in `cross_cutting_notes` — assign to a primary module, create a shared module, or document in `open_questions` if human input is needed.

**DO NOT** leave unresolved `[cross-cutting]` items. The scaffold must be clean before evidence extraction.

---

### No duplicates (reuse)
*Scanner: `scripts/scanners/no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept names remain unique within their module after unification. **DO** ensure module names remain unique across the output.

**DO NOT** introduce duplicates when unifying synonyms — merge into one concept with combined chunk_ids.

---

### Domain–story map sync (reuse)
*Scanner: `scripts/scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story after cross-module wiring.

**DO NOT** break sync when assigning cross-cutting concepts — update stories to reference the concept in its new home.

---

### Hierarchy sizing (reuse)
*Scanner: `scripts/scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range. Subtype additions must not violate hierarchy sizing.

---

### Concepts must have owns (reuse)
*Scanner: `scripts/scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept (including new subtypes) has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scripts/scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story retains trigger and response after canonicalization.

---

### Subtypes and enums finalized (AI-only)
*(AI-only — no scanner)*

**DO** resolve all deferred subtype/enum decisions. Create subtype concepts or apply `EnumType {val1, val2}` consistently.

**DO NOT** leave `[defer]` for subtype/enum in the output. **Integrate and Harmonize** must resolve them — no deferred structural decisions in the integrated scaffold.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/cross_cutting_resolved.py --input map-model-spec.json
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
```

Review each violation. Fix or document. Re-run until all scanners report PASS.

### Pass 2 — Build chunk index (code)

If structure changed:

```
python scripts/build_chunk_index.py --input map-model-spec.json --output mms-chunk-index.json
```

### Pass 3 — Adversarial validation (AI)

- Any cross-cutting item left unresolved?
- Any synonym unification that merged distinct concepts?
- Any subtype that should have been an enum (or vice versa)?
- Any cross-module relationship missing or incorrect?

---

## Output

- `map-model-spec.json` — updated with unified names, cross-module relationships, resolved cross-cutting items, finalized subtypes/enums
- `mms-chunk-index.json` — updated if structure changed (re-run `build_chunk_index.py`)


---

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: cross-cutting-resolved
phases: [step5]
order: 50
scanner: scripts/scanners/cross_cutting_resolved.py
impact: HIGH
---

## Cross-cutting concerns must be resolved or explicitly deferred

When the same concept name appears in multiple modules, or when evidence shows shared infrastructure (logging, auth, notifications), document how it is handled — either assign a **home module** with `cross_cutting_notes`, or leave `cross_cutting_notes` empty only when the scanner finds **no** cross-cutting pattern to flag.

The scanner (`scripts/scanners/cross_cutting_resolved.py`) treats **non-empty** `cross_cutting_notes` as a violation until assessment marks the concern handled. Empty notes pass.

**DO** keep `cross_cutting_notes` empty when concepts are cleanly scoped and names do not collide across modules.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "Cart",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          }
        ]
      },
      "epic": { "name": "Checkout", "stories": [] }
    },
    {
      "module": {
        "name": "Payments",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "SettlementBatch",
            "owns": "Owns batching and cut-off times for release",
            "owns_chunk": "chunk-p1",
            "chunk_ids": ["chunk-p1"]
          }
        ]
      },
      "epic": { "name": "Settlement", "stories": [] }
    }
  ]
}
```

**DO** document the resolution in `cross_cutting_notes` when you intentionally share a concept — then clear or update notes in assessment once home module and boundaries are agreed.

```json
{
  "name": "Retail",
  "cross_cutting_notes": "Customer identity: home module is IAM; Retail stores only customerId foreign key — see IAM.CustomerAccount.",
  "concepts": []
}
```

**DO NOT** leave stale placeholder text in `cross_cutting_notes` through final delivery — the scanner flags non-empty notes.

```json
{
  "name": "Retail",
  "cross_cutting_notes": "TODO: figure out auth",
  "concepts": []
}
```

Non-empty — violation until resolved in assessment.

**DO NOT** duplicate the same concept name in two modules without notes.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "CustomerAccount",
            "owns": "Owns cart preferences",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          }
        ]
      },
      "epic": { "name": "Checkout", "stories": [] }
    },
    {
      "module": {
        "name": "IAM",
        "cross_cutting_notes": "",
        "concepts": [
          {
            "name": "CustomerAccount",
            "owns": "Owns credentials and sessions",
            "owns_chunk": "chunk-i1",
            "chunk_ids": ["chunk-i1"]
          }
        ]
      },
      "epic": { "name": "Login", "stories": [] }
    }
  ]
}
```

Same concept name, two modules, empty `cross_cutting_notes` — scanner may flag; assessment must rename, merge, or document.


---

---
rule_id: no-duplicates
phases: [step1, step2, step3, step5]
order: 15
scanner: scripts/scanners/no_duplicates.py
impact: HIGH
---

## No duplicate names at the same scope

The same name must not appear twice among siblings at the same level: duplicate module names, duplicate concept names within a module, duplicate epic names at the same parent, duplicate story names under the same epic or sub-epic.

The scanner (`scripts/scanners/no_duplicates.py`) flags collisions.

**DO** use distinct names or merge duplicates into one entry with combined evidence.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": { "name": "Checkout", "stories": [] }
    },
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": { "name": "Settlement", "stories": [] }
    }
  ]
}
```

```json
{
  "name": "Retail",
  "concepts": [
    {
      "name": "Cart",
      "owns": "Owns line items before checkout",
      "owns_chunk": "chunk-a",
      "chunk_ids": ["chunk-a"]
    },
    {
      "name": "Promotion",
      "owns": "Owns discount rules",
      "owns_chunk": "chunk-b",
      "chunk_ids": ["chunk-b"]
    }
  ]
}
```

**DO NOT** repeat the same module name in `modules_and_epics[]`.

```json
{
  "modules_and_epics": [
    { "module": { "name": "Retail", "concepts": [] }, "epic": { "name": "A", "stories": [] } },
    { "module": { "name": "Retail", "concepts": [] }, "epic": { "name": "B", "stories": [] } }
  ]
}
```

**DO NOT** repeat concept names within one module.

```json
{
  "name": "Retail",
  "concepts": [
    {
      "name": "Cart",
      "owns": "Owns line items",
      "owns_chunk": "chunk-a",
      "chunk_ids": ["chunk-a"]
    },
    {
      "name": "Cart",
      "owns": "Owns totals display",
      "owns_chunk": "chunk-c",
      "chunk_ids": ["chunk-c"]
    }
  ]
}
```

**DO NOT** repeat story names under the same parent.

```json
{
  "name": "Checkout",
  "stories": [
    { "name": "Apply tax", "trigger": "…", "response": "…" },
    { "name": "Apply tax", "trigger": "…", "response": "…" }
  ]
}
```


---

---
rule_id: domain-interaction-sync
phases: [step1, step2, step3, step5]
order: 40
scanner: scripts/scanners/domain_interaction_sync.py
impact: HIGH
---

## Domain names in stories must match concepts

Stories use `**Concept**` bolding to name domain participants. Those names must resolve to concepts in the module — or the story cannot be traced to the model.

The scanner (`scripts/scanners/domain_interaction_sync.py`) checks that bolded names in `epic.statement`, `epic.pre_condition`, and each story's `trigger` / `response` exist as concept names (or aliases) under the paired module.

**DO** use the same spelling and casing as `module.concepts[].name` (or list the term under `aliases`).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Cart",
            "owns": "Owns line items and running totals before checkout",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          },
          {
            "name": "Promotion",
            "owns": "Owns which discount rules apply to a cart line",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          }
        ]
      },
      "epic": {
        "name": "Apply promotions",
        "statement": "**Cashier** adds rows to **Cart**; **System** evaluates **Promotion** rules.",
        "statement_chunk": "chunk-r1",
        "stories": [
          {
            "name": "Stacking rules",
            "trigger": "**Cashier** adds a second **Promotion** to **Cart**",
            "response": "**System** applies stacking policy and refreshes **Cart** totals"
          }
        ]
      }
    }
  ]
}
```

**DO NOT** bold names that do not exist on concepts (unless they are actors like **Customer** — actors are not required to be concepts).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Cart",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"]
          }
        ]
      },
      "epic": {
        "name": "Apply promotions",
        "statement": "**System** evaluates **PromoEngine** against **Cart**.",
        "statement_chunk": "chunk-r1",
        "stories": []
      }
    }
  ]
}
```

`PromoEngine` is bolded but no concept (or alias) — violation.

**DO NOT** rename concepts in stories without updating `concepts[]` (or aliases).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "ArmorClass",
            "aliases": [],
            "owns": "Owns the target number to hit",
            "owns_chunk": "chunk-srd-1",
            "chunk_ids": ["chunk-srd-1"]
          }
        ]
      },
      "epic": {
        "name": "Resolve hits",
        "statement": "**System** compares roll to **AC**.",
        "statement_chunk": "chunk-srd-1",
        "stories": []
      }
    }
  ]
}
```

`AC` is not `ArmorClass` and is not listed under `aliases` — violation.

Fix in scaffold (alias) or story text:

```json
{
  "name": "ArmorClass",
  "aliases": ["AC"],
  "owns": "Owns the target number to hit",
  "owns_chunk": "chunk-srd-1",
  "chunk_ids": ["chunk-srd-1"]
}
```


---
