---
rule_id: chunks-must-be-referenced
phases: [step1]
order: 10
scanner: scripts/scanners/chunks_must_be_referenced.py
impact: HIGH
---

## All evidence claims must cite a chunk

Every field that makes an evidence claim must include a chunk reference. An uncited claim is speculation — it cannot be verified, cannot be navigated in later steps, and cannot be included in the reverse index.

The scanner (`scripts/scanners/chunks_must_be_referenced.py`) highlights missing citations. It does not determine whether a missing citation is a genuine gap or a false positive — that judgment belongs to the AI in the adversarial validation pass.

**DO** cite a chunk on every evidence-bearing field:

- `module.description_chunk` — the chunk that evidenced the module description
- `concept.owns_chunk` — the chunk that evidenced what this concept owns
- `concept.chunk_ids` (or `chunk_evidence` with `chunk_id`) — non-empty where the concept is evidenced
- `property.chunk` — the chunk that evidenced this property (paired with `definition`)
- `operation.chunk` — the chunk that evidenced this operation (paired with `definition`)
- `epic.statement_chunk` — the chunk that evidenced the epic statement
- `epic.pre_condition_chunk` — the chunk that evidenced the pre-condition (when `pre_condition` is populated)

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "description": "Originate and release customer payment instructions.",
        "description_chunk": "chunk-mod-pay-1",
        "concepts": [
          {
            "name": "LimitChecker",
            "owns": "Owns whether a payment instruction is allowed against daily and per-transaction limits",
            "owns_chunk": "chunk-4410b",
            "chunk_ids": ["chunk-4410b", "chunk-4410c"],
            "properties": [
              {
                "definition": "Number dailyLimit",
                "chunk": "chunk-4410b"
              }
            ],
            "operations": [
              {
                "definition": "evaluate(instruction: PaymentInstruction) -> Decision",
                "chunk": "chunk-4410c"
              }
            ]
          }
        ]
      },
      "epic": {
        "name": "Wire transfers",
        "statement": "**Customer** initiates **WireTransfer**; **System** validates limits before release.",
        "statement_chunk": "chunk-09bc",
        "pre_condition": "**Customer** session is authenticated.",
        "pre_condition_chunk": "chunk-09bc"
      }
    }
  ]
}
```

**DO NOT** populate any of these fields without a chunk citation. If you cannot cite a chunk, either leave the field blank or add a `[defer]` flag with the chunk that shows the thing exists but was not fully read.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "LimitChecker",
            "owns": "Owns whether a payment instruction is allowed against daily and per-transaction limits",
            "chunk_ids": ["chunk-4410b"]
          }
        ]
      },
      "epic": { "name": "Placeholder" }
    }
  ]
}
```

`owns` is set but `owns_chunk` is missing — violation.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Provisioning",
        "description": "Install and activate customer circuits from service orders."
      },
      "epic": { "name": "Placeholder" }
    }
  ]
}
```

`description` is set but `description_chunk` is missing — violation.

Do not cite a nearby chunk “by proximity” when the corpus does not support the claim — use `[defer]` in the owning text and a real chunk id that proves the gap is documented.
