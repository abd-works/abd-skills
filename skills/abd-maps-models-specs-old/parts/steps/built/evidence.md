# Evidence

## Purpose

Extract structured evidence from the codebase (or corpus) guided by the concept list in `map-model-spec.json`. Evidence feeds into **[Structure](../../process.md)** (Stage 3) for full model construction.

**Status:** The extractor script is not yet implemented. The process below describes the intended behavior. Until implemented, evidence files must be produced manually or by an external tool; scanners validate the output.

---

## Inputs

- `map-model-spec.json` — canonical scaffold with concept list
- Source corpus (code, docs, or context directory: `context_index.json` + `chunks/*.md`)

---

## Corpus Scope

**Scan the full corpus.** **Evidence** is code-based extraction across **all chunks** in the context directory (`chunks/*.md`). Do not limit to chunks indexed in mms-chunk-index.json. This step is where corpus coverage expands beyond the **~30%** sampled in **[Modules and Epics](../../process.md)** (scaffold breadth). For each concept in the scaffold, search the entire corpus for evidence.

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

These rules apply to the evidence extraction output. **Evidence** is code-based; scanners validate the evidence files before **Structure**.

Full rule files: `rules/`

---

### Evidence files exist
*Scanner: `scripts/scanners/evidence_files_exist.py` → Rule: `evidence-files-exist.md`*

**DO** produce all four evidence files: `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, `evidence/relationships.json`.

**DO NOT** skip a file — **Structure** expects all four. Empty `{}` or `{"concepts": {}}` is valid when no evidence found.

---

### Evidence references scaffold concepts only
*Scanner: `scripts/scanners/evidence_scaffold_refs.py` → Rule: `evidence-scaffold-refs.md`*

**DO** ensure every concept_id (or concept key) in evidence files exists in the scaffold (`map-model-spec.json`).

**DO NOT** invent concepts in evidence — extract only for concepts already in the canonical scaffold.

---

### Evidence schema valid
*Scanner: `scripts/scanners/evidence_schema.py` → Rule: `evidence-schema-valid.md`*

**DO** produce valid JSON. Each file should have a structure that maps concepts to evidence entries (e.g. `{"ConceptName": [...]}` or `{"concepts": {"ConceptName": [...]}}`).

**DO NOT** produce malformed JSON or files that cannot be parsed by **Structure**.

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


---

## Rules (baked in)

Apply these rules when producing output for this step.

---
rule_id: evidence-scaffold-refs
phases: [step4]
order: 10
scanner: scripts/scanners/evidence_scaffold_refs.py
impact: HIGH
---

## Evidence must reference only scaffold concepts

Extraction is guided by the canonical concept list in `map-model-spec.json`. Evidence files attach chunks and claims to those concept keys. Keys that are not in the scaffold break Step 5 and invalidate traceability.

The scanner (`scripts/scanners/evidence_scaffold_refs.py`) flags concept IDs in evidence files that do not exist in the scaffold.

**DO** ensure every concept key in `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, and `evidence/relationships.json` exists under some `module.concepts[].name` in `map-model-spec.json` (exact spelling).

Scaffold (`map-model-spec.json`):

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "WireTransfer",
            "owns": "Owns customer-initiated wire instruction validation and release",
            "owns_chunk": "chunk-pay-1",
            "chunk_ids": ["chunk-pay-1"]
          }
        ]
      },
      "epic": { "name": "Wire release", "stories": [] }
    }
  ]
}
```

Evidence (`evidence/actions.json`) — top-level keys match concept names:

```json
{
  "WireTransfer": [
    {
      "action": "Customer submits instruction",
      "chunk_ids": ["chunk-pay-1"]
    }
  ]
}
```

Same scaffold, nested `concepts` shape (also accepted by the scanner):

```json
{
  "concepts": {
    "WireTransfer": [
      { "action": "Customer submits instruction", "chunk_ids": ["chunk-pay-1"] }
    ]
  }
}
```

**DO** add the concept to the scaffold in Step 3 (or an explicit intermediate pass) before attaching evidence under that key.

**DO NOT** add evidence for concepts not in the scaffold “because the PDF mentions them” — extend the scaffold first, or file under the nearest existing parent with `[defer]` in the scaffold text.

Scaffold has only `WireTransfer`, but evidence introduces extra keys:

```json
{
  "WireTransfer": [],
  "ACHCredit": [],
  "LimtChecker": []
}
```

`ACHCredit` and `LimtChecker` are not in `module.concepts[].name` — scanner reports orphan keys. (`LimtChecker` is also a typo for `LimitChecker`.)

**DO NOT** use a different naming convention in evidence than in the scaffold.

Scaffold:

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "LimitChecker",
            "owns": "Owns limit evaluation for payment instructions",
            "owns_chunk": "chunk-lim-1",
            "chunk_ids": ["chunk-lim-1"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Evidence:

```json
{
  "limit_checker": []
}
```

Key `limit_checker` does not match `LimitChecker` — violation.

The scaffold is the namespace; evidence is annotations on that namespace — not the driver of new concept names without a scaffold update.


---

---
rule_id: evidence-files-exist
phases: [step4]
order: 5
scanner: scripts/scanners/evidence_files_exist.py
impact: HIGH
---

## All four evidence files must exist

Step 4 produces structured evidence for downstream structure and assessment. Step 5 expects a complete set of files. A missing file usually means extraction stopped early or a path was wrong.

The scanner (`scripts/scanners/evidence_files_exist.py`) checks that all four files exist.

**DO** produce these paths under `evidence/`:

- `evidence/actions.json`
- `evidence/decisions.json`
- `evidence/states.json`
- `evidence/relationships.json`

**DO** use empty but valid JSON when a category has nothing to say:

`evidence/relationships.json`:

```json
{}
```

`evidence/decisions.json`:

```json
{}
```

`evidence/states.json`:

```json
{
  "concepts": {}
}
```

`evidence/actions.json`:

```json
{}
```

(Adjust empty shape to match your pipeline’s convention; each file must still parse as JSON.)

**DO NOT** skip a file because “we had no relationships”. Create the file with empty content.

**DO NOT** rename files or invent parallel names — automation depends on fixed paths.

Invalid handoff — only one file on disk:

```
evidence/
  actions.json
```

Missing: `decisions.json`, `states.json`, `relationships.json`.

Wrong contract:

```
evidence/
  actions.json
  actions_v2.json
```

Use the four canonical filenames only.


---

---
rule_id: evidence-schema-valid
phases: [step4]
order: 15
scanner: scripts/scanners/evidence_schema.py
impact: MEDIUM
---

## Evidence files must be valid JSON

Step 5 reads evidence files programmatically. Malformed JSON blocks the structure phase.

The scanner (`scripts/scanners/evidence_schema.py`) validates that each evidence file parses as valid JSON.

**DO** produce valid JSON. Use `python -m json.tool evidence/actions.json` or `python -c "import json; json.load(open('evidence/actions.json'))"` before handoff.

**DO** match the expected shape: an object with concept keys or a `concepts` object mapping concept names to evidence arrays — follow the schema your pipeline documents.

`evidence/actions.json` (valid):

```json
{
  "WireTransfer": [
    {
      "action": "Customer submits instruction",
      "chunk_ids": ["chunk-pay-1"]
    }
  ]
}
```

UTF-8 encoding; no paste artifacts inside strings.

**DO NOT** produce truncated files (copy-paste cut mid-string).

**DO NOT** use JSON5, trailing commas, or comments inside `.json` unless your toolchain explicitly supports them.

Not valid JSON (do not save this inside a `.json` file):

```
{'WireTransfer': []}
```

Not valid JSON:

```
{
  "WireTransfer": [
    {
      "action": "Incomplete
    }
  ]
}
```

Not valid JSON:

```
{
  "WireTransfer": [],
  // TODO: add ACH
}
```

Markdown fenced code pasted into the `.json` file itself — the file on disk must be raw JSON only.


---
