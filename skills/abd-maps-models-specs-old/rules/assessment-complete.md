---
rule_id: assessment-complete
phases: [step6]
order: 30
impact: HIGH
---

## Assessment must be produced and applied

**[Finalize](../parts/process.md)** (Stage 3) includes an **Assess** activity. There is **no scanner** for this rule — the AI (or human reviewer) must perform it and record the outcome. Skipping assessment ships contradictions: enum/subtype mistakes, orphan concepts, and story/domain drift.

**DO** produce an assessment artifact (for example `assessment.json` next to `map-model-spec.json`, or a section your repo documents) that explicitly records decisions and follow-ups.

```json
{
  "assessment_version": "1",
  "map_model_spec_path": "map-model-spec.json",
  "resolved": [
    {
      "topic": "type_field_vs_subtype",
      "decision": "Merge WireTransfer, ACHCredit, RTPPayment into PaymentInstruction with EnumType rail { wire, ach, rtp }",
      "chunk_ids": ["chunk-pay-001"]
    },
    {
      "topic": "domain_interaction_sync",
      "decision": "Story used **SKU**; scaffold had Product only — stories updated to **Product**",
      "chunk_ids": ["chunk-retail-12"]
    }
  ],
  "known_gaps": []
}
```

**DO** apply fixes before declaring `map-model-spec.json` final, or record open gaps in `known_gaps`:

```json
{
  "assessment_version": "1",
  "map_model_spec_path": "map-model-spec.json",
  "resolved": [],
  "known_gaps": [
    {
      "id": "gap-01",
      "description": "Two concepts both named like spell slot — merge deferred to next harmonize",
      "chunk_ids": ["chunk-srd-magic-2"]
    }
  ]
}
```

**DO NOT** skip assessment because “the JSON validates”.

**DO NOT** treat linter green as model correct — scanners catch syntax and heuristics, not semantic truth.

Chat-only resolution with no saved artifact — no audit trail:

```
(Conversation only: "merged RTP into PaymentInstruction" — assessment.json not updated)
```

Cosmetic JSON edits with empty assessment:

```json
{
  "assessment_version": "1",
  "resolved": [],
  "known_gaps": []
}
```

No entries in `resolved` despite substantive model changes — insufficient assessment record.
