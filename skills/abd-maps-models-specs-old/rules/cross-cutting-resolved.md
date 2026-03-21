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
