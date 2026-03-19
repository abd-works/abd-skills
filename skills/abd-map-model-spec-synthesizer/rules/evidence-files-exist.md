---
rule_id: evidence-files-exist
phases: [step4]
order: 5
scanner: mms_scan_evidence_files_exist.py
impact: HIGH
---

## All Evidence Files Must Exist

Step 4 produces four evidence files. Step 5 expects all four. Missing files indicate incomplete extraction.

The scanner (`mms_scan_evidence_files_exist.py`) checks that all four files exist.

**DO** produce:
- `evidence/actions.json`
- `evidence/decisions.json`
- `evidence/states.json`
- `evidence/relationships.json`

**DO NOT** skip a file. Empty content (`{}` or `{"concepts": {}}`) is valid when no evidence was found for any concept.
