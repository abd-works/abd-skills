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
