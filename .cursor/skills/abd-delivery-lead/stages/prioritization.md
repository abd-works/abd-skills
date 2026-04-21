# Prioritization

## Purpose

Break the story map into thin vertical slices — groups of stories that cross application layers, represent business-observable behavior, and carry recognizable user value. Order slices to maximize early learning and risk reduction.

Thin slices are groups of stories from a large initiative that span multiple features, technologies, and potentially teams into something that can be developed and tested end-to-end. They are elements of a deployable item with recognizable user value, though they do not comprise all the functionality needed for a full release.

## Why this stage matters

- **End-to-end delivery:** Thin slicing forces work through all layers of the system, exposing integration issues early instead of deferring them to late integration phases.
- **Feedback frequency:** Smaller increments increase the frequency of internal customer feedback, so the team learns whether it is building the right thing before investing heavily.
- **Risk reduction:** Ordering slices by risk and learning means the hardest unknowns are tackled first, when there is still time to adjust.
- **Quality metrics:** Each slice is testable as a business scenario, allowing quality to be measured on real behavior, not component checkboxes.
- **WIP control:** Thin slices control how much significant work is started at once, reducing hand-offs and increasing flow.

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

## Key questions (is this stage done?)

1. Can the team describe each slice in one sentence of business value — not a list of technical components?
2. Does the first (spine) slice represent the minimum end-to-end path a user could exercise?
3. Is the ordering rationale explicit — why this slice before that one (value, risk, or learning)?
4. Are there stories that span multiple slices or are unassigned? If so, is there a reason?
5. Could the team start building the first slice tomorrow and deliver something testable at the end?
6. Has the team identified which slices are optional or deferrable versus which are on the spine?

## Conditions of success

- Every story is assigned to a named slice/increment.
- At least one **spine** slice is identified — the minimum viable increment that delivers recognizable user value end-to-end.
- Slices are vertical: each one crosses from user interaction through business logic to persistence or integration, not horizontal layers.
- Slice ordering reflects a deliberate strategy (value first, risk first, learning first) with explicit rationale.
- The slicing is a tool for conversation — the team and stakeholders agree on what comes first and why.

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
