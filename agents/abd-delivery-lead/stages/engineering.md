# Engineering

## Purpose

Implement production code that makes the acceptance tests pass. Follow clean code principles: domain language, single responsibility, explicit dependencies, guard clauses, and continuous refactoring. The GREEN and REFACTOR phases of TDD.

## Team role

**Engineer**

## Practice skill

`abd-clean-code` — Production code implementing story behavior using domain language, clean functions, explicit dependencies, and observable design. SRP, intention-revealing names, constructor injection, DRY, domain exceptions.

## Entry conditions

- Acceptance Tests exit gate passed.
- Executable test files exist and are RED (failing).
- API surface and design patterns are established from test helpers.
- `story-graph.json` is current with stories, AC, scenarios, and test mapping.

## Expected outputs

- Production code modules that make the acceptance tests GREEN.
- Refactored code meeting clean code quality bar.
- Updated test helpers if the implementation surface changed during GREEN phase.

## Exit gate

1. All acceptance tests pass (GREEN).
2. Practice skill scanners pass: `run_scanners.py --skill-root <abd-clean-code> --workspace <workspace>` exits 0.
3. Code uses domain language consistent with upstream stages.
4. Functions and classes follow single responsibility — no god objects or multi-purpose utilities.
5. Dependencies are explicit (constructor injection, no hidden globals).
6. No duplication that could be extracted.
7. The user has confirmed the implementation at a team-member checkpoint.

## Handoff (flow complete)

This is the final stage. Pass to the delivery lead:
- Summary of implemented stories, passing tests, and code quality.
- Any technical debt logged for future iteration.
- Suggestions for the next delivery increment (next slice from prioritization).
