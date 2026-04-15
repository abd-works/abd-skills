---
rule_id: domain-types-and-deepen-quality
---

## Promotion and deepen: quality bar for concepts

**Phases 4–6** — sparse types, variant decisions, responsibilities and dependencies.

**Promotion (Phase 4):** **`concepts[]`** only where **distinct behavioral contracts** are justified—see [`domain-model.md`](../content/parts/library/domain-model.md). Each promoted concept has **owns** (or equivalent) grounded in evidence where you claim it—not a slogan. **Reject** explicit duplicates and **near-duplicates** with a written rationale (candidate queue).

**Variants (Phase 5):** Variant families have an explicit representation choice **before** you assign broad structure (see `variant-decisions-before-deepen`).

**Deepen (Phase 6):** **No anemic concepts:** responsibilities and collaborations reflect **real** state and operations. **No over-centralization:** avoid a single “god” concept unless the domain truly works that way. Deepen claims that matter still cite **chunks** (or approved evidence fields).

For **`map-model-spec.json`**, citation presence is enforced by **`scripts/scanners/chunks_must_be_referenced.py`** when that file exists. This rule remains **normative prose**; other mechanical checks live beside that scanner under `scripts/`.

**DO**

- Give each promoted concept an **`owns`** sentence that states a **decision or rule** the concept owns, with evidence where you claim it—not a restatement of the name.

```json
{
  "name": "OrderTotal",
  "owns": "Owns how tax and discounts combine to a payable total for the cart",
  "evidence_chunk_ids": ["chunk-orders-09"]
}
```

**DO NOT**

- Promote a concept with `owns` that is a vague label, or **five near-duplicates** with no reject/merge note in the candidate queue.

```json
{
  "name": "OrderTotal",
  "owns": "Stuff about orders"
}
```

Vague `owns`—violation.
