# Generate — abd-story-specification

## From acceptance criteria

When AC exist, use the main-flow AC as spine: WHEN → When, THEN → Then, add Given preconditions. Then add failure, edge, and alternate flows.

## Stubbed services

When a scenario stubs an external service, apply `rules/stub-service-interaction-structure.md`. Note new stub input/output pairs for fixture update (`abd-story-acceptance-test` rule `stub-data-sync-with-scenarios`).

Default notation (Scenario Outline) and coverage expectations are in `rules/` — especially `use-scenario-outline-when-needed.md`.
