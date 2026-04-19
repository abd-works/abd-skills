# Acceptance Tests

## Purpose

Turn scenarios and acceptance criteria into executable test code. Tests are written first (RED phase of TDD) — they define the behavioral contract that production code must satisfy. The orchestrator pattern: Given-When-Then test methods calling helper functions; one class per behavior, one test per scenario.

## Team role

**Engineer**

## Practice skill

`abd-acceptance-test-driven-development` — Write tests first from behavioral context. Orchestrator pattern, TDD cycle (RED-GREEN-REFACTOR), domain language, API design through failing tests.

## Entry conditions

- Scenarios exit gate passed.
- Scenario files exist with concrete Given/When/Then examples.
- `story-graph.json` contains stories with AC and scenario references.
- Target language and test framework are known or can be inferred from the workspace.

## Expected outputs

- Executable test files in the workspace (one class per behavior, one test per scenario).
- Tests are RED — they compile/parse but fail because production code does not yet exist.
- Test-to-story mapping documented (which test covers which story/AC/scenario).

## Exit gate

1. `story-graph.json` passes structural validation (test node mapping if applicable).
2. Practice skill scanners pass: `run_scanners.py --skill-root <abd-acceptance-test-driven-development> --workspace <workspace>` exits 0.
3. Every scenario from the previous stage has a corresponding test.
4. Tests follow the orchestrator pattern: Given-When-Then methods call helper functions.
5. Tests use domain language from upstream stages (story names, AC terms, scenario values).
6. Tests are parseable/compilable in the target language.
7. The user has confirmed the test structure at a team-member checkpoint.

## Handoff to next stage

Pass forward:
- Test file paths and test-to-story mapping.
- API surface implied by tests (function signatures, class interfaces the tests call).
- Any design decisions or architectural patterns established in test helpers.
