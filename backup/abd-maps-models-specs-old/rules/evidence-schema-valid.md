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
