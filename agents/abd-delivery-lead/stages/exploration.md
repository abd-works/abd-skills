# Exploration

## Purpose

Deepen each story's definition by writing behavioral acceptance criteria — concrete WHEN/THEN statements that describe how the system responds to user actions. Bridge the gap between story-level intent and testable expectations.

## Team role

**Analyst**

## Practice skill

`abd-acceptance-criteria` — Exploration-phase AC: WHEN/THEN/AND/BUT, behavioral language, per-story domain terms, atomic AC, actor alternation.

## Entry conditions

- Prioritization exit gate passed.
- `story-graph.json` contains stories with slice assignments.
- A target slice or set of stories is identified for exploration (typically the first/spine slice from prioritization).

## Expected outputs

- Updated `story-graph.json` with AC arrays on explored stories.
- Rendered acceptance-criteria artifacts per the practice skill templates (`acceptance-criteria.md` and `acceptance-criteria.txt`).

## Exit gate

1. `story-graph.json` passes structural validation.
2. Practice skill scanners pass: `run_scanners.py --skill-root <abd-acceptance-criteria> --workspace <workspace>` exits 0.
3. Every explored story has at least one AC in WHEN/THEN format.
4. AC use behavioral language — describe system response to user action, not implementation.
5. AC reference only stories that exist in the graph (traceability).
6. Domain vocabulary is consistent with discovery-stage naming.
7. The user has confirmed the AC at a team-member checkpoint.

## Handoff to next stage

Pass forward:
- Updated `story-graph.json` with AC.
- Which stories/slices have been explored (scope for scenarios stage).
- Any open questions, edge cases flagged but not yet resolved, and gaps in business logic.
