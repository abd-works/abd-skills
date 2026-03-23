---
rule_id: evidence-citations-required
phase_files:
  - terms-mechanisms.md
  - shaped-story-map.md
  - domain-types.md
  - variant-classification.md
  - deepen.md
  - integrate.md
  - validate-render.md
---

## Evidence claims must cite the corpus

**Applies from Phase 2 onward** (after Phase 1 has validated **`context_index.json`** and context chunks). Phases **2–8** in the process table.

**Where** something is anchored (Phase 1 `chunk_id` / block IDs) and **what** it becomes in later layers (term, mechanism, story, promoted concept, …) are **different moves**. This rule covers the **“where”**: any field that asserts substance about the source must remain traceable.

Use the shapes in [`terms-mechanisms-contract.md`](../content/parts/library/terms-mechanisms-contract.md), [`shaped-story-map.md`](../content/parts/library/shaped-story-map.md), and [`domain-model.md`](../content/parts/library/domain-model.md)—not legacy JSON field names from other repos unless this skill’s output **actually** uses them.

**Automation:** `scripts/validate_phase3_story_map.py` (Phase 3); `scripts/scanners/chunks_must_be_referenced.py` when `maps-models-specs/map-model-spec.json` exists (skips if absent). Scanners catch misses; this rule states what “good” looks like for authoring.

**DO**

- Tie Phase 2 terms and mechanisms that are not guesswork to **`chunk_id`** (or equivalent evidence fields your automation defines).
- List **`evidence_chunk_ids[]`** on substantive Phase 3 stories; resolve against `context_index.json`.
- Carry **chunk** (or approved evidence) references on promoted concepts and deepen fields where you claim corpus grounding.

```json
{
  "term": "PaymentInstruction",
  "definition": "Customer-originated payment request",
  "chunk_id": "chunk-pay-01"
}
```

**DO NOT**

- Paraphrase the source with **no** `chunk_id`, or treat a module name as evidence for a promoted concept.

```json
{
  "term": "PaymentInstruction",
  "definition": "Customer-originated payment request"
}
```

Missing `chunk_id` on a substantive term—violation once Phase 1 validates.
