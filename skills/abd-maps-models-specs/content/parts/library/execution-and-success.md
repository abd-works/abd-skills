# Execution order and success definition

Enduring reference for **what to run next** and **what “good” looks like**. Keep this file aligned with [`principles-and-rules.md`](principles-and-rules.md) and [`content/parts/process.md`](../content/parts/process.md). When execution gates or paths change, update **[`context-spec.md`](context-spec.md)** (Phase 1) and the relevant phase docs.

---

## Execution order (what to do next)

1. **Greenfield:** **[Phase 0](../phases/context-chunking-approach.md) — §1:** convert sources to **canonical Markdown** where needed (PDF, DOCX, PPTX, …); own the scripts or ingest pipeline there. **Phase 0 — §2–§4:** wire **`solution.conf`**, structural inventory, draft + review **`context_chunking_spec`** per [`context-spec.md`](context-spec.md). **Phase 1:** emit chunks + index + manifest **pin** when the **contract** validator passes.

2. **Existing `context/`:** If sources or layout **changed**, refresh **Phase 0** rules then **rebuild** or **re-chunk** in Phase 1.

3. **Finalize** the Phase 1 context package (see [`context-spec.md`](context-spec.md) — runnable pipeline, manifest, validators) before Phase 2.

4. Only then: **Phase 2** onward in order — `python scripts/build_phase2_artifacts.py` → `test/mm3/abd-maps-models-specs/phase2/`. See [`terms-mechanisms-contract.md`](terms-mechanisms-contract.md). Re-run `generate_context_bundle_manifest.py` for phase2 hashes.

5. **Phase 3:** maintain `test/mm3/abd-maps-models-specs/phase3/mm3_story_map.json` (stories with **anchor** + `term_refs` / **`evidence_chunk_ids`**). Validate: `python scripts/scanners/phase3_story_map_evidence.py` (wrapper: `validate_phase3_story_map.py`; extend per [`shaped-story-map.md`](shaped-story-map.md)). See [`story-map.md`](story-map.md). Re-run bundle manifest for phase3 hash.

6. **Phase 4–8:** types → variants → deepen → integrate → validate/render (per [`content/parts/process.md`](../content/parts/process.md) and [`pipeline_invariants.md`](pipeline_invariants.md)).

---

## Success definition (reusable)

Another domain (another handbook) should be able to:

1. Supply **source material**, run **Phase 0** conversion + chunking spec (see Phase 0 §1–§4), then land on the **same Phase 1 package** after Phase 1 (`context_index.json` + context chunks + rules).

2. Run **subsequent phases** so **relationships** and **types** follow **explicit** gates and the [**principles table**](principles-and-rules.md), with **evidence-backed** promotion and schema checks.
