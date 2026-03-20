---
rule_id: chunks-must-be-referenced
phases: [step1]
order: 10
scanner: scanners/chunks_must_be_referenced.py
impact: HIGH
---

## All evidence claims must cite a chunk

Every field that makes an evidence claim must include a chunk reference. An uncited claim is speculation — it cannot be verified, cannot be navigated in Step 2, and cannot be included in the reverse index.

The scanner (`scanners/chunks_must_be_referenced.py`) highlights missing citations. It does not determine whether a missing citation is a genuine gap or a false positive — that judgment belongs to the AI in the adversarial validation pass.

**DO** cite a chunk on every evidence-bearing field:

- `module.description_chunk` — the chunk that evidenced the module description
- `concept.owns_chunk` — the chunk that evidenced what this concept owns
- `concept.chunk_ids` — non-empty list of chunks where this concept is the primary subject
- `property.chunk` — the chunk that evidenced this property
- `operation.chunk` — the chunk that evidenced this operation
- `epic.statement_chunk` — the chunk that evidenced the epic statement
- `epic.pre_condition_chunk` — the chunk that evidenced the pre-condition (when pre-condition is populated)

**DO NOT** populate any of these fields without a chunk citation. If you cannot cite a chunk, either leave the field blank or add a `[defer]` flag with the chunk that shows the thing exists but was not fully read.
