---
rule_id: assessment-complete
phases: [step6]
order: 30
impact: HIGH
---

## Assessment Must Be Produced and Applied

Step 6 includes an Assess phase. Produce an assessment covering consistency, coverage, completeness, and type-field-vs-subtype. Apply fixes before declaring final.

There is no scanner for this rule. The AI must perform the assessment and document it.

**DO** produce an assessment that covers:
- **Consistency** — naming, types, terminology aligned across modules
- **Coverage** — all concepts participate in at least one story
- **Completeness** — no `[defer]` or `open_questions` left unresolved (or explicitly documented as known gaps)
- **Type-field-vs-subtype** — enum vs subtype representation is correct

**DO NOT** skip assessment. Document gaps. Apply fixes. The final output is validated only after assessment is complete.
