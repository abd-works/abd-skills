---
title: Concepts Must Have Owns
impact: HIGH
tags: [step2, domain, concepts]
scanner: scan_concepts_have_owns
---

## Every Concept Must Have Decision Ownership

**DO** ensure every concept has an `owns` field — one sentence on what decision or rule this concept owns.

**DO NOT** leave a concept with only chunk_ids and no decision ownership. A concept earns its place by owning decisions or enforcing rules — not by appearing as a noun.

- Right: `owns: "Decides degree of success from d20 + modifier vs DC"` (chunk: id)
- Wrong: Concept with chunk_ids but empty or missing `owns`
