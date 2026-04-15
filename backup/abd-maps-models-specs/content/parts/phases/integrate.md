# Integrate

**Goal:** Synonyms, repointing, **drain candidate queue** into final `map-model-spec` (or split artifacts if story map stays separate).

**Normative for Phase 9:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.

## Steps

1. Reconcile synonyms and duplicate references.

2. **Verify candidate queue is fully drained.** Every entry in `candidate_queue.json` must have a corresponding entry in `promotion_ledger.json` with one of: `promote`, `absorb`, `merge`, `extend`, `defer`, `reject`. If any candidate lacks a ledger entry, resolve it now using the decision taxonomy from [domain-types.md](domain-types.md).

3. For `defer` entries: verify the trigger condition is documented and actionable. If new evidence arrived during later phases, re-evaluate deferred candidates.

4. Keep **domain narrative** and **story map** aligned when both artifacts exist.

5. **Final pass on class-shaped prose:** Reconcile any remaining gaps between `map-model-spec.json` and the module **domain concept** blocks per [domain-model.md](../library/domain-model.md). Remove stale **`**newly added**`** markers if you are cutting a **release** snapshot (optional); otherwise leave them for one review cycle. Re-run **`render_map_model_class_diagram.py`** if the spec changed in this phase.

## Exit

- Single coherent map-model-spec (or documented split) ready for validation.
- `promotion_ledger.json` has an entry for every candidate in the queue — no orphans.
- All `defer` entries have documented trigger conditions.
