# Execution order and success definition

Enduring reference for **what to run next** and **what “good” looks like**. Keep this file aligned with [`principles-and-rules.md`](principles-and-rules.md) and [`content/parts/process.md`](../content/parts/process.md). When execution gates or paths change, update **[`context-package.md`](context-package.md)** (Phase 1) and the relevant phase docs.

---

## Execution order (what to do next)

1. **Context path A — Greenfield or known bad:** Ensure **canonical Markdown** (e.g. **PDF →** `HeroesHandbook.md`). **Write the chunking spec** (`context_chunking_spec.yaml` per [`context-package.md`](context-package.md)), then implement **Phase 1** (chunks + index + version pin). Use **Phase 0** questions as **acceptance** for that package before freezing v1.

2. **Context path B — Existing `context/`:** Run **readiness** (Phase 0: metrics + spot-check)—or **skip** straight to rebuild if you already know it fails (e.g. MM3: spot-check **no**).

3. If **adopt with extensions:** migrate or sidecar into canonical schema; fill `modeling_kind`; **freeze** v1.

4. If **rebuild or first build:** complete Phase 1; **freeze** the Phase 1 package (see [`context-package.md`](context-package.md) — runnable pipeline, manifest, validators).

5. Only then: **Phase 2** onward in order — `python scripts/build_phase2_artifacts.py` → `test/mm3/abd-maps-models-specs/phase2/`. See [`terms-mechanisms-contract.md`](terms-mechanisms-contract.md). Re-run `generate_context_bundle_manifest.py` for phase2 hashes.

6. **Phase 3:** maintain `test/mm3/abd-maps-models-specs/phase3/mm3_story_map.json` (behavioral stories with **anchor** + `term_refs` / **`evidence_chunk_ids`**). Validate: `python scripts/validate_phase3_story_map.py` (extend per [`behavioral-story-map.md`](behavioral-story-map.md)). See [`story-map-narrative.md`](story-map-narrative.md). Re-run bundle manifest for phase3 hash.

7. **Phase 4–8:** types → variants → deepen → integrate → validate/render (per [`content/parts/process.md`](../content/parts/process.md) and [`pipeline_invariants.md`](pipeline_invariants.md)).

---

## Success definition (reusable)

Another domain (another handbook) should be able to:

1. Supply **source material** (typically **PDF → Markdown**, then chunking) and land on the **same Phase 1 package** after Phase 1 (frozen index + rules).

2. Run **subsequent phases** so **relationships** and **types** follow **explicit** gates and the [**principles table**](principles-and-rules.md), with **evidence-backed** promotion and schema checks.
