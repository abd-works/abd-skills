---
rule_id: no-junk-concepts
phases: [step2, step3, step5]
order: 30
scanner: scripts/scanners/no_junk_concepts.py
impact: HIGH
---

## No junk concepts

A concept is junk if it is a synonym of another concept, a UI label with no decision ownership, a database table name mistaken for domain meaning, or a passive noun with no rules.

The scanner (`scripts/scanners/no_junk_concepts.py`) flags likely junk. Borderline cases are resolved in assessment.

**DO** merge synonyms into one concept with `aliases` (or one canonical name and evidence that ties alternate terms to the same chunk).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "ShoppingCart",
            "aliases": ["Basket", "Cart"],
            "owns": "Owns line items and running totals before checkout",
            "owns_chunk": "chunk-retail-cart-1",
            "chunk_ids": ["chunk-retail-cart-1"]
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
        "name": "Retail",
        "concepts": [
          {
            "name": "InventoryReservation",
            "owns": "Owns whether stock is held for an order line and for how long",
            "owns_chunk": "chunk-retail-inv-2",
            "chunk_ids": ["chunk-retail-inv-2"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** introduce parallel concepts for the same decision with only naming drift.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "ShoppingCart",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-retail-cart-1",
            "chunk_ids": ["chunk-retail-cart-1"]
          },
          {
            "name": "Basket",
            "owns": "Owns line items before checkout",
            "owns_chunk": "chunk-retail-cart-1",
            "chunk_ids": ["chunk-retail-cart-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Two concepts, same `owns` and same chunks — junk duplicate.

**DO NOT** model passive containers as concepts when they carry no rules.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Ops",
        "concepts": [
          {
            "name": "OrderHeaderRow",
            "owns": "Row in the orders table",
            "owns_chunk": "chunk-db-99",
            "chunk_ids": ["chunk-db-99"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Table shape is not domain ownership — fold into `Order` or drop.

**DO NOT** invent concepts for every UI string.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "UI",
        "concepts": [
          {
            "name": "SubmitButton",
            "owns": "The button the user clicks",
            "owns_chunk": "chunk-mockup-1",
            "chunk_ids": ["chunk-mockup-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

UI chrome is not a domain concept unless the source assigns it explicit behavioral rules.
