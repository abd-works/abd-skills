---
rule_id: variant-decisions-before-deepen
phase_files:
  - variant-classification.md
  - deepen.md
---

## Variant representation before deep property work

**Process:** Phase **5** (variant classification) **before** Phase **6** (deepen). See [`pipeline_invariants.md`](../content/parts/library/pipeline_invariants.md).

For each **family of variation**, decide **how** it is represented (enum vs subtypes vs other) **before** you spread properties and operations across types. Deepening (Phase 6) **assumes** those decisions are stable enough to argue responsibilities and `depends_on` without constant rework.

At **variant-classification**, write **explicit** per-family decisions (format is yours to standardize, but the decision must exist in the artifact set you use).

At **deepen**, if variant shape was wrong, **fix the variant decision first**, then deepen—not the reverse. Deepen is not a backdoor to “implicit enum vs inheritance.”

This replaces hand-wavy “classify variants before modeling” rules tied to old step indices. The **phase files** `variant-classification.md` and `deepen.md` define the boundary.

**DO**

- Record per-family representation **before** Phase 6 property work.

```json
{
  "variant_family": "Discount",
  "representation": "enum",
  "values": ["NONE", "PERCENT", "FIXED"]
}
```

**DON'T**

- Add many properties to subtypes in Phase 6 while Phase 5 still says **“TBD”** for how the family is represented.

```json
{
  "variant_family": "Discount",
  "representation": "TBD",
  "subtypes": [{ "name": "PercentDiscount", "properties": [...] }]
}
```

Properties **before** representation is locked—**violation**.
