---
rule_id: cross-cutting-resolved
phases: [step3]
order: 5
scanner: mms_scan_cross_cutting_resolved.py
impact: HIGH
---

## All Cross-Cutting Items Must Be Resolved

Step 3 produces a canonical scaffold. Every item that was flagged `[cross-cutting]` in Step 1 or 2 must be resolved before evidence extraction. Unresolved cross-cutting items indicate concepts or mechanics that span modules but have not been assigned a home — the scaffold is incomplete.

The scanner (`mms_scan_cross_cutting_resolved.py`) flags non-empty `cross_cutting_notes` that still contain unresolved items.

**DO** resolve every cross-cutting item by:
- Assigning it to a primary module (with rationale)
- Creating a shared module when the concept is truly cross-cutting
- Documenting in `open_questions` if human input is needed (with explicit question)

**DO NOT** leave `cross_cutting_notes` with unresolved entries. Move resolved items out; document decisions.
