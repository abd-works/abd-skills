---
rule_id: validate-and-manifest-gates
---

## Validate & render: reproducible gates

**Phase 8** — scanners, schema checks, reports, bundle manifest, optional CI.

**What “done” means here:** Run **`python scripts/build.py`** so **`operator.build_pipeline`** executes. That pipeline includes the **rule-bound** steps registered in **`rules/scanners.json`** (context index contract, shaped story map evidence, chunk citations when artifacts exist), **`scanner_pipeline_outputs.py`**, **`generate_context_bundle_manifest.py`**, and **`test_rule_examples.py`**. Extend or reorder steps in **`skill-config.json`** if your host needs a different operator sequence.

**Render:** Reports and diagrams must **trace** to the same artifacts validators use—not a one-off narrative that drifts from JSON.

“Assessment complete” in older pipelines referred to a different **phase index**. Here, **Phase 8** is the **validation and delivery** gate for this skill’s **published** slice.

**DO**

- Run **`python scripts/build.py`** (or the same validators in CI) before you call the slice “done”; keep manifest hashes aligned with published outputs.

```text
build.py: operator.build_pipeline (see skill-config.json) — includes rule-bound scanners from rules/scanners.json
```

**DON'T**

- Publish a report or diagram that claims success while validators would **fail** on the same tree.

```text
Rendered report: "All stories green"
phase3_story_map_evidence.py: FAIL (missing evidence_chunk_ids)
```

Narrative and machine state **must** match.
