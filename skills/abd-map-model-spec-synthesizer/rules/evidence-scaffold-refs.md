---
rule_id: evidence-scaffold-refs
phases: [step4]
order: 10
scanner: mms_scan_evidence_scaffold_refs.py
impact: HIGH
---

## Evidence Must Reference Only Scaffold Concepts

Extraction is guided by the concept list. Do not invent concepts — extract evidence only for concepts already in the canonical scaffold (`map-model-spec.json`).

The scanner (`mms_scan_evidence_scaffold_refs.py`) flags concept IDs in evidence files that do not exist in the scaffold.

**DO** ensure every concept key in evidence files exists in `map-model-spec.json` (across all modules).

**DO NOT** add evidence for concepts not in the scaffold. If you discover a new concept during extraction, add it to the scaffold first (Step 3) or defer to a later pass.
