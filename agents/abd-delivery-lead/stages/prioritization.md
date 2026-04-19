# Prioritization

## Purpose

Break the story map into thin vertical slices — groups of stories that cross application layers, represent business-observable behavior, and carry recognizable user value. Order slices to maximize early learning and risk reduction.

## Team role

**Product Owner**

## Practice skill

`abd-thin-slicing` — Thin-sliced delivery increments: vertical MVIs, spine vs optional paths, quality trade-offs, marketable increment names, and early risk validation.

## Entry conditions

- Discovery exit gate passed.
- `story-graph.json` exists with epics, sub-epics, and stories.
- Rendered story map available for reference.

## Expected outputs

- Updated `story-graph.json` with slice assignments on stories (increment groupings, ordering metadata).
- Rendered thin-slicing artifacts in `templates/` (`thin-slicing.md` and `thin-slicing.txt`) with identical increment and story coverage.

## Exit gate

1. `story-graph.json` passes structural validation.
2. Practice skill scanners pass: `run_scanners.py --skill-root <abd-thin-slicing> --workspace <workspace>` exits 0.
3. Every story is assigned to a slice/increment.
4. Slices are ordered with rationale (value, risk, learning).
5. At least one "spine" slice is identified — the minimum viable increment.
6. Rendered templates exist and reflect the slicing.
7. The user has confirmed the slicing at a team-member checkpoint.

## Handoff to next stage

Pass forward:
- Updated `story-graph.json` with slice metadata.
- Recommended first slice for exploration.
- Priority rationale and any scope deferral decisions.
