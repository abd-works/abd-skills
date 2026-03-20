# Step 8 — Evidence

## Purpose

Extract structured evidence from the codebase (or corpus) guided by the concept list in `map-model-spec.json`. Evidence feeds into Step 9 for full model construction.

**Status:** The extractor script is not yet implemented. The process below describes the intended behavior. Until implemented, evidence files must be produced manually or by an external tool; scanners validate the output.

---

## Inputs

- `map-model-spec.json` — canonical scaffold with concept list
- Source corpus (code, docs, or context directory: `context_index.json` + `chunks/*.md`)

---

## Corpus Scope

**Scan the full corpus.** Step 8 is code-based extraction across **all chunks** in the context directory (`chunks/*.md`). Do not limit to chunks indexed in mms-chunk-index.json. This step is where corpus coverage expands beyond the 30% sampled in Step 4. For each concept in the scaffold, search the entire corpus for evidence.

---

## Process

Code-based extraction. For each concept in the scaffold:

1. **Actions** — Identify operations, methods, or behaviors that the concept participates in.
2. **Decisions** — Identify decision points, branching logic, or rule enforcement.
3. **States** — Identify state transitions, properties, or lifecycle phases.
4. **Relationships** — Identify collaborators, callers, receivers, containment.

Extraction is guided by the concept list — do not invent concepts; extract evidence for concepts already in the scaffold.

---

## Rules

These rules apply to the evidence extraction output. Step 6 is code-based; scanners validate the evidence files before Step 7.

Full rule files: `rules/`

---

### Evidence files exist
*Scanner: `scan_evidence_files_exist.py` → Rule: `evidence-files-exist.md`*

**DO** produce all four evidence files: `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, `evidence/relationships.json`.

**DO NOT** skip a file — Step 7 expects all four. Empty `{}` or `{"concepts": {}}` is valid when no evidence found.

---

### Evidence references scaffold concepts only
*Scanner: `scan_evidence_scaffold_refs.py` → Rule: `evidence-scaffold-refs.md`*

**DO** ensure every concept_id (or concept key) in evidence files exists in the scaffold (`map-model-spec.json`).

**DO NOT** invent concepts in evidence — extract only for concepts already in the canonical scaffold.

---

### Evidence schema valid
*Scanner: `scan_evidence_schema.py` → Rule: `evidence-schema-valid.md`*

**DO** produce valid JSON. Each file should have a structure that maps concepts to evidence entries (e.g. `{"ConceptName": [...]}` or `{"concepts": {"ConceptName": [...]}}`).

**DO NOT** produce malformed JSON or files that cannot be parsed by Step 7.

---

## After Extraction — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/evidence_files_exist.py
python scripts/scanners/evidence_scaffold_refs.py
python scripts/scanners/evidence_schema.py
```

Review each violation. Fix extraction logic. Re-run until all scanners report PASS.

---

## Output

- `evidence/actions.json` — actions per concept
- `evidence/decisions.json` — decisions per concept
- `evidence/states.json` — states and transitions per concept
- `evidence/relationships.json` — cross-concept relationships
