---
rule_id: evidence-schema-valid
phases: [step4]
order: 15
scanner: mms_scan_evidence_schema.py
impact: MEDIUM
---

## Evidence Files Must Be Valid JSON

Step 5 reads evidence files. Malformed JSON blocks the structure phase.

The scanner (`mms_scan_evidence_schema.py`) validates that each evidence file parses as valid JSON.

**DO** produce valid JSON. Expected structure: object with concept keys or a `concepts` object mapping concept names to evidence arrays.

**DO NOT** produce truncated, malformed, or non-JSON output.
