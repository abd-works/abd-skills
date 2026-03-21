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
