---
phases: [concept_synthesis]
order: 10
---

## Merge alias concepts into canonical

**DO** merge alias concepts into their canonical using `concept_guidance.concept_aliases`. If concept_aliases has "Account": ["ACCT"], then concepts must NOT contain both "ACCT" and "Account" as separate entries.

**DO NOT** leave abbreviation concepts (ACCT, REV, CUST, SKU, etc.) as separate concepts when concept_aliases maps them to a canonical.
