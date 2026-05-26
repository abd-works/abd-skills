# Slot MM — Reviewer Finished

**Timestamp:** <ISO 8601>
**Stage reviewed:** shaping | discovery | exploration | specification | engineering
**Role:** reviewer (`slot_type: reviewer`; same `team-role` as executor under review)
**Prior executor slot:** slot-NN-finished.md

## Artifacts reviewed

| Artifact | Path | Present |
|----------|------|---------|
| <name> | <workspace-relative path> | yes / no |

## Scanner results (reviewer scanned)

| Practice skill | Scanner command | Result | Violations |
|----------------|-----------------|--------|------------|
| <skill> | run_scanners.py --skill-root … | PASS / FAIL | <summary or none> |

**All scanners:** PASS / FAIL

**Scanner infrastructure:** PASS / FAIL — If FAIL (import crash, traceback, false ALL CLEAN, no scanners found), set **Overall gate: FAIL** and list under Blockers. Do not continue the chain.

## Scanner exception (only if obviously not relevant)

| Field | Content |
| --- | --- |
| **Applies?** | no (default) / yes |
| **Scanner / rule** | <name> |
| **Why not relevant here** | <1–3 sentences — must be obvious; not brownfield convenience> |
| **Exit gate without this rule** | <which items still pass> |

If **Applies?** = yes → **Overall gate** may be **PASS with documented scanner exception**. Infra failures never use this section.

## Exit-gate review (reviewer reviewed)

Reference: `../../../content/stages/<stage>.md`

| Gate item | Pass / Fail | Finding |
|-----------|-------------|---------|
| <item> | PASS / FAIL | <detail or —> |

**Overall gate:** PASS / FAIL

## Findings for delivery lead

- **Blockers:** <list or "None"> — include **scanner infrastructure** when scanners crashed or did not execute
- **Suggested fixes:** <numbered list for rework slot or scanner-infra fix slot, or "None — clean pass">
- **Corrections to log:** <rule ids / entry titles, or "None">

## For delivery lead

- Tick checklist: **Reviewer — scanners run** and **Reviewer — exit-gate review complete**
- If **scanner infrastructure FAIL:** stop chain; author scanner-infra fix slot; re-run scanners before slot NN+1 (see delivery-lead **Scanner infrastructure gate**)
- If artifact suggested fixes: log corrections, author rework executor slot, tick **Rework** lines when incorporated
