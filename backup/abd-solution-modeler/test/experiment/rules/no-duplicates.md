---
rule_id: no-duplicates
phases: [step1]
order: 20
scanner: scan_no_duplicates.py
impact: HIGH
---

## Names must be unique within their scope

Duplicate names indicate a collision — two things being called the same thing in the same context. This is always a modeling error at Step 1: either the same concept was named twice (remove one), or two distinct concepts share a name (rename one to distinguish them).

The scanner (`scan_no_duplicates.py`) highlights duplicate names. It does not determine which entry to keep or how to rename — that judgment belongs to the AI.

**DO** ensure concept names are unique within their module.

**DO** ensure module names are unique across the entire output.

**DO NOT** have two concepts with the same name in the same module. If two chunks describe the same concept, merge them into one entry with both chunk_ids.

**DO NOT** have two modules with the same name. If two areas of the domain share a name, one of them is misnamed.
