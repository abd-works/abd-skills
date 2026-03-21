# Structure

## Purpose

AI builds the full model from the canonical scaffold plus evidence. Properties, operations, inheritance, stories, and steps are populated from `map-model-spec.json` and `evidence/`.

---

## Inputs

- `map-model-spec.json` — canonical scaffold from **[Integrate and Harmonize](../../process.md)** (Stage 2)
- `evidence/` — actions.json, decisions.json, states.json, relationships.json

---

## Process

AI step. Read the scaffold and evidence. For each module/epic pair:

1. **Domain model** — Populate properties, operations, invariants from evidence. Assign types. Add inheritance where subtypes are finalized.
2. **Story map** — Populate stories with Trigger, Response, Pre-Condition, Failure-Modes. Add scenarios and steps. Ground in `**Concept**`.
3. **Sync** — Ensure every concept participates in at least one story. Ensure every story references concepts.

---

## Rules

These rules apply after structuring. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Use evidence where available (AI-only)
*(AI-only — no scanner)*

**DO** populate properties, operations, and invariants from `evidence/` when evidence exists for a concept.

**DO NOT** ignore evidence — **Structure** merges scaffold with evidence. Empty evidence for a concept is acceptable; populated evidence must be reflected.

---

### No duplicates (reuse)
*Scanner: `scripts/scanners/no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept and module names remain unique.

---

### Domain–story map sync (reuse)
*Scanner: `scripts/scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story.

---

### Hierarchy sizing (reuse)
*Scanner: `scripts/scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range.

---

### Concepts must have owns (reuse)
*Scanner: `scripts/scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scripts/scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story has trigger and response.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
```

Review each violation. Fix or document. Re-run until all scanners report PASS.

### Pass 2 — Adversarial validation (AI)

- Any evidence ignored when it should have been used?
- Any property or operation invented without evidence?
- Any concept with evidence that has no properties/operations populated?

---

## Output

- `map-model-spec.json` — structured (full domain model + story map)


---

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: no-anemia
phases: [step2, step3, step5]
order: 35
scanner: null
impact: MEDIUM
---

## No anemic concepts (manual / assessment)

An anemic concept is a named bucket with no properties, no operations, and a vague `owns` — it does not carry enough structure to validate or implement.

There is **no automated scanner** for this rule in this package. Apply it during adversarial validation and assessment.

**DO** give each concept at least one property or operation when the source supports it, and make `owns` state a specific decision.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Promotion",
            "owns": "Owns which discount rules apply to a cart line and in what order",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"],
            "properties": [
              { "definition": "String code", "chunk": "chunk-r2" },
              {
                "definition": "EnumType stackPolicy { exclusive, additive }",
                "chunk": "chunk-r2"
              }
            ],
            "operations": [
              {
                "definition": "apply(cart: Cart, line: LineItem) -> MoneyAmount",
                "chunk": "chunk-r2"
              }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** leave a concept as only a name and generic owns.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Promotion",
            "owns": "Handles promotions",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

No properties, no operations, vague owns — anemic.

**DO NOT** split one cohesive rule across three empty shells.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "PromotionRules",
            "owns": "Rules",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          },
          {
            "name": "PromotionEngine",
            "owns": "Engine",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          },
          {
            "name": "PromotionResult",
            "owns": "Result",
            "owns_chunk": "chunk-r2",
            "chunk_ids": ["chunk-r2"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Three names, no structure — fold into one concept or add real properties/operations.


---

---
rule_id: no-over-centralization
phases: [step2, step3, step5]
order: 36
scanner: null
impact: MEDIUM
---

## No god object (manual / assessment)

A god object owns every decision in the domain — dozens of unrelated properties and operations on one concept, with other concepts reduced to dumb data holders.

There is **no automated scanner** for this rule in this package. Apply it during adversarial validation and assessment.

**DO** distribute ownership so each concept owns a coherent slice of decisions.

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
            "chunk_ids": ["chunk-r1"],
            "properties": [
              { "definition": "List<LineItem> lines", "chunk": "chunk-r1" }
            ],
            "operations": [
              {
                "definition": "addLine(sku: String, qty: Number) -> void",
                "chunk": "chunk-r1"
              }
            ]
          },
          {
            "name": "TaxCalculator",
            "owns": "Owns jurisdiction rules and tax lines for a cart",
            "owns_chunk": "chunk-r3",
            "chunk_ids": ["chunk-r3"],
            "operations": [
              {
                "definition": "compute(cart: Cart) -> List<TaxLine>",
                "chunk": "chunk-r3"
              }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** pile unrelated domains onto one concept.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "OrderSystem",
            "owns": "Owns cart, tax, payment, shipping, inventory, promotions, and user profiles",
            "owns_chunk": "chunk-r1",
            "chunk_ids": ["chunk-r1"],
            "properties": [
              { "definition": "List<LineItem> lines", "chunk": "chunk-r1" },
              { "definition": "MoneyAmount tax", "chunk": "chunk-r1" },
              { "definition": "String cardToken", "chunk": "chunk-r1" },
              { "definition": "String trackingNumber", "chunk": "chunk-r1" },
              { "definition": "Number stockOnHand", "chunk": "chunk-r1" }
            ],
            "operations": [
              { "definition": "checkout() -> void", "chunk": "chunk-r1" },
              { "definition": "ship() -> void", "chunk": "chunk-r1" },
              { "definition": "chargeCard() -> void", "chunk": "chunk-r1" }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Single concept absorbing cart, tax, payment, shipping, inventory — god object.

**DO NOT** make every other concept an empty DTO while one concept holds all behavior — split by bounded context from the corpus.


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
