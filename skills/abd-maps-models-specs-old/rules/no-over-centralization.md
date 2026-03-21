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
