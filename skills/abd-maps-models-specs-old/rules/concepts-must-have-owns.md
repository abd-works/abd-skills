---
rule_id: concepts-must-have-owns
phases: [step2, step3, step5]
order: 20
scanner: scripts/scanners/concepts_have_owns.py
impact: HIGH
---

## Every concept must have decision ownership

The scanner (`scripts/scanners/concepts_have_owns.py`) flags concepts that violate this rule. Borderline wording is resolved in assessment.

**DO** ensure every concept has an `owns` field — one sentence stating what **decision or rule** this concept owns (not a restatement of the name, not vague marketing text).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "PriceBook",
            "owns": "Owns which list price applies for a SKU in a channel and effective date range",
            "owns_chunk": "chunk-retail-12",
            "chunk_ids": ["chunk-retail-12"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "ArmorClass",
            "owns": "Owns the target number an attack roll must meet or beat to hit",
            "owns_chunk": "chunk-srd-combat-3",
            "chunk_ids": ["chunk-srd-combat-3"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Telco",
        "concepts": [
          {
            "name": "ServiceOrder",
            "owns": "Owns lifecycle state transitions for install or repair orders until closed",
            "owns_chunk": "chunk-telco-ord-1",
            "chunk_ids": ["chunk-telco-ord-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** leave a concept with only `chunk_ids` and no decision ownership. A concept earns its place by owning decisions or enforcing rules — not by appearing as a noun in the source.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "PriceBook",
            "chunk_ids": ["chunk-retail-12"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** set `owns` to the concept name or other non-decision text.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "ArmorClass",
            "owns": "ArmorClass",
            "owns_chunk": "chunk-srd-combat-3",
            "chunk_ids": ["chunk-srd-combat-3"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```
