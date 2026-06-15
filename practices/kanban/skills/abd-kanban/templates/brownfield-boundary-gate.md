# Brownfield boundary gate — reviewer checklist

Use **after** story-mapping (and optional domain/arch draft) **before** acceptance-criteria or ATDD slots for the same boundary.

**Boundary name:** <e.g. world-entry, Enter Game, AccountServer API>
**Strategy:** `brownfield-current-state`
**Executor slot reviewed:** slot-NN-finished.md

## Evidence completeness

| Check | Pass / Fail | Notes |
| ----- | ----------- | ----- |
| Every in-scope **story** has at least one evidence reference (code, test, log, config, or verified chunk) | | |
| Entry points traced (not class-name-only mapping) | | |
| Failure / alternate paths from source are mapped or explicitly deferred to AC with story refs | | |
| No **fix-while-map** changes in production code during mapping slot | | |
| Quirks/bugs listed as **observed**, not silently corrected in map text | | |

## Artifact alignment

| Artifact | Path | Aligned with map? |
| -------- | ---- | ----------------- |
| story-map.md / story-graph.json | | yes / no / n/a |
| module partition (if used) | | |
| domain-terms / UL (if run) | | |
| architecture outline/blueprint (if run) | | |

## Scanners

| Skill | Result |
| ----- | ------ |
| abd-story-mapping (`run_scanners.py`) | PASS / FAIL |
| Other assigned discovery skills | |

## Decision

**Gate:** PASS / FAIL

**Blockers:** <list or None>

**Approved to proceed to:** acceptance-criteria / thin-slicing / ATDD — <which>

**For kanban lead:** Tick checklist; if FAIL, rework story-mapping skill for this boundary only.
