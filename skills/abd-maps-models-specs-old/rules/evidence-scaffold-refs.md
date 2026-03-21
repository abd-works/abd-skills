---
rule_id: evidence-scaffold-refs
phases: [step4]
order: 10
scanner: scripts/scanners/evidence_scaffold_refs.py
impact: HIGH
---

## Evidence must reference only scaffold concepts

Extraction is guided by the canonical concept list in `map-model-spec.json`. Evidence files attach chunks and claims to those concept keys. Keys that are not in the scaffold break Step 5 and invalidate traceability.

The scanner (`scripts/scanners/evidence_scaffold_refs.py`) flags concept IDs in evidence files that do not exist in the scaffold.

**DO** ensure every concept key in `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, and `evidence/relationships.json` exists under some `module.concepts[].name` in `map-model-spec.json` (exact spelling).

Scaffold (`map-model-spec.json`):

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "WireTransfer",
            "owns": "Owns customer-initiated wire instruction validation and release",
            "owns_chunk": "chunk-pay-1",
            "chunk_ids": ["chunk-pay-1"]
          }
        ]
      },
      "epic": { "name": "Wire release", "stories": [] }
    }
  ]
}
```

Evidence (`evidence/actions.json`) — top-level keys match concept names:

```json
{
  "WireTransfer": [
    {
      "action": "Customer submits instruction",
      "chunk_ids": ["chunk-pay-1"]
    }
  ]
}
```

Same scaffold, nested `concepts` shape (also accepted by the scanner):

```json
{
  "concepts": {
    "WireTransfer": [
      { "action": "Customer submits instruction", "chunk_ids": ["chunk-pay-1"] }
    ]
  }
}
```

**DO** add the concept to the scaffold in Step 3 (or an explicit intermediate pass) before attaching evidence under that key.

**DO NOT** add evidence for concepts not in the scaffold “because the PDF mentions them” — extend the scaffold first, or file under the nearest existing parent with `[defer]` in the scaffold text.

Scaffold has only `WireTransfer`, but evidence introduces extra keys:

```json
{
  "WireTransfer": [],
  "ACHCredit": [],
  "LimtChecker": []
}
```

`ACHCredit` and `LimtChecker` are not in `module.concepts[].name` — scanner reports orphan keys. (`LimtChecker` is also a typo for `LimitChecker`.)

**DO NOT** use a different naming convention in evidence than in the scaffold.

Scaffold:

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "LimitChecker",
            "owns": "Owns limit evaluation for payment instructions",
            "owns_chunk": "chunk-lim-1",
            "chunk_ids": ["chunk-lim-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Evidence:

```json
{
  "limit_checker": []
}
```

Key `limit_checker` does not match `LimitChecker` — violation.

The scaffold is the namespace; evidence is annotations on that namespace — not the driver of new concept names without a scaffold update.
