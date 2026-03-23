---
rule_id: validate-and-manifest-gates
phase_files:
  - validate-render.md
---

## Validate & render: reproducible gates

**Phase 8** — scanners, schema checks, reports, bundle manifest, optional CI.

**What “done” means here:** (1) **Context contract** — `scripts/scanners/context_index_contract.py` when `context_index.json` exists (legacy wrapper: `validate_context_contract.py`). (2) **Story map** — `scripts/scanners/phase3_story_map_evidence.py` when `mm3_story_map.json` exists (legacy wrapper: `validate_phase3_story_map.py`). (3) **Map-model-spec citations** — `scripts/scanners/chunks_must_be_referenced.py` when `map-model-spec.json` exists. (4) **Pipeline outputs** — `scanner_pipeline_outputs.py` per your wiring. (5) **Manifest** — `generate_context_bundle_manifest.py` for reproducibility.

**Render:** Reports and diagrams must **trace** to the same artifacts validators use—not a one-off narrative that drifts from JSON.

“Assessment complete” in older pipelines referred to a different **phase index**. Here, **Phase 8** is the **validation and delivery** gate for this skill’s **published** slice.

**DO**

- Run **`python scripts/build.py`** (or the same validators in CI) before you call the slice “done”; keep manifest hashes aligned with published outputs.

```text
build.py: context_index_contract → phase3_story_map_evidence → chunks_must_be_referenced → manifest
```

**DON'T**

- Publish a report or diagram that claims success while validators would **fail** on the same tree.

```text
Rendered report: "All stories green"
phase3_story_map_evidence.py: FAIL (missing evidence_chunk_ids)
```

Narrative and machine state **must** match.
