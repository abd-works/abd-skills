---
rule_id: mechanism-concept-coverage
---

## Mechanism entities must resolve to concepts or ledger entries

**Applies** when `mechanisms.json` and `candidate_queue.json` are present under the workspace `output_dir`. When `promotion_ledger.json` exists, the scanner also checks ledger coverage.

**Automation:** `scripts/scanners/mechanism_concept_coverage.py` (this skill's `build_pipeline`). Validates that entities named in mechanism descriptions and `realized_by` paths are accounted for in `terms_layer.json`, `candidate_queue.json`, or `map-model-spec.json` concepts. When `promotion_ledger.json` exists, also checks that every candidate has a ledger entry.

**DO**

- Ensure every entity named in a mechanism `description` or `realized_by` path appears in at least one of: `terms_layer.json`, `candidate_queue.json`, or `map-model-spec.json` `concepts[]`.
- Ensure every entry in `candidate_queue.json` has a corresponding decision in `promotion_ledger.json` (when ledger exists).

**DO NOT**

- Leave entities referenced in mechanisms unaccounted for — they must appear as terms, candidates, or promoted concepts.
- Leave candidates in the queue without a ledger decision after the domain-types phase completes.
