# Step 4 — Evidence Extraction

## Purpose

Extract structured evidence from the codebase (or corpus) guided by the concept list in `map-model-spec.json`. Evidence feeds into Step 5 for full model construction.

---

## Inputs

- `map-model-spec.json` — canonical scaffold with concept list
- Source corpus (code, docs, or `context/context_chunks.json`)

---

## Corpus Scope

**Scan the full corpus.** Step 4 is code-based extraction across **all chunks** in `context_chunks.json`. Do not limit to chunks indexed in mms-chunk-index.json. This step is where corpus coverage expands beyond the 30% sampled in Step 1. For each concept in the scaffold, search the entire corpus for evidence.

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

These rules apply to the evidence extraction output. Step 4 is code-based; scanners validate the evidence files before Step 5.

Full rule files: `rules/`

---

### Evidence files exist
*Scanner: `mms_scan_evidence_files_exist.py` → Rule: `evidence-files-exist.md`*

**DO** produce all four evidence files: `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, `evidence/relationships.json`.

**DO NOT** skip a file — Step 5 expects all four. Empty `{}` or `{"concepts": {}}` is valid when no evidence found.

---

### Evidence references scaffold concepts only
*Scanner: `mms_scan_evidence_scaffold_refs.py` → Rule: `evidence-scaffold-refs.md`*

**DO** ensure every concept_id (or concept key) in evidence files exists in the scaffold (`map-model-spec.json`).

**DO NOT** invent concepts in evidence — extract only for concepts already in the canonical scaffold.

---

### Evidence schema valid
*Scanner: `mms_scan_evidence_schema.py` → Rule: `evidence-schema-valid.md`*

**DO** produce valid JSON. Each file should have a structure that maps concepts to evidence entries (e.g. `{"ConceptName": [...]}` or `{"concepts": {"ConceptName": [...]}}`).

**DO NOT** produce malformed JSON or files that cannot be parsed by Step 5.

---

## After Extraction — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/mms_scan_evidence_files_exist.py
python scripts/mms_scan_evidence_scaffold_refs.py
python scripts/mms_scan_evidence_schema.py
```

Review each violation. Fix extraction logic. Re-run until all scanners report PASS.

---

## Output

- `evidence/actions.json` — actions per concept
- `evidence/decisions.json` — decisions per concept
- `evidence/states.json` — states and transitions per concept
- `evidence/relationships.json` — cross-concept relationships
