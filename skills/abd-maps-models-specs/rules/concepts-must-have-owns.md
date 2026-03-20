---
title: Concepts Must Have Owns
impact: HIGH
tags: [step2, step3, step5, step6, domain, concepts]
scanner: scanners/concepts_have_owns.py
---

## Every Concept Must Have Decision Ownership

**DO** ensure every concept has an `owns` field — one sentence on what decision or rule this concept owns.

**DO NOT** leave a concept with only chunk_ids and no decision ownership. A concept earns its place by owning decisions or enforcing rules — not by appearing as a noun.

- Right: `owns: "Decides degree of success from d20 + modifier vs DC"` (chunk: id)
- Wrong: Concept with chunk_ids but empty or missing `owns`
