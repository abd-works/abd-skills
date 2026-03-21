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
