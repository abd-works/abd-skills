# Scenarios

## Purpose

Refine acceptance criteria into concrete specification-by-example scenarios — Given/When/Then with real domain values. Scenarios make behavior unambiguous, reviewable by business stakeholders, and directly translatable into executable tests.

## Team role

**Analyst**

## Practice skill

`abd-specification-by-example` — Concrete Given/When/Then steps with real domain values, bold concept names, italic values. Plain scenarios (inline values) and outline (multiple data rows).

## Entry conditions

- Exploration exit gate passed.
- `story-graph.json` contains stories with AC in WHEN/THEN format.
- Target stories for scenario writing are identified (typically those explored in the previous stage).

## Expected outputs

- Scenario files in the workspace (per the practice skill's template format).
- Updated `story-graph.json` with scenario references on stories where applicable.

## Exit gate

1. `story-graph.json` passes structural validation.
2. Practice skill scanners pass (if `abd-specification-by-example` ships scanners): `run_scanners.py --skill-root <abd-specification-by-example> --workspace <workspace>`.
3. Every explored story has at least one scenario with concrete values (not abstract placeholders).
4. Scenarios use Given/When/Then structure with real domain data.
5. Scenarios trace back to AC — every scenario exercises at least one AC.
6. Domain terms and actor names are consistent with upstream stages.
7. The user has confirmed the scenarios at a team-member checkpoint.

## Handoff to next stage

Pass forward:
- Scenario files and their paths.
- Updated `story-graph.json`.
- Mapping of scenarios to stories and AC for test traceability.
- Any ambiguities discovered during scenario writing that may need upstream revision.
