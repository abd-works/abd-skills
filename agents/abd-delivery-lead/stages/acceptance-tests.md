# Acceptance Tests

## Purpose

Turn scenarios and acceptance criteria into executable test code. Tests are written first (RED phase of TDD) — they define the behavioral contract that production code must satisfy. The orchestrator pattern: Given-When-Then test methods calling helper functions; one class per behavior, one test per scenario.

Acceptance Test Driven Development (ATDD) is a practice in which the team collaboratively discusses acceptance criteria, uses real-world examples to formulate concrete acceptance tests, and writes those tests **before development begins**. By doing ATDD, the team gains a shared understanding of what is being developed and when it would be considered done.

## Why this stage matters

- **Tests define the contract:** The tests written here are the executable definition of "done" for each story. Production code exists only to make these tests pass — nothing more, nothing less.
- **API design through failing tests:** Writing tests first forces design decisions to surface early. The function signatures, class interfaces, and domain objects that tests call become the API surface of the production code.
- **Shared understanding as code:** ATDD involves at least three perspectives — business, development, and testing. Tests that emerge from this collaboration encode the team's shared understanding in a form that can be run, not just read.
- **Confidence for change:** A comprehensive suite of acceptance tests gives the team confidence to refactor, extend, and evolve the codebase. Without them, every change is a gamble.
- **Not going well when:** developers write tests after the feature is demonstrated (just to fulfil a DoD), the acceptance criteria are not meaningful to users, or developers write tests without involving business or testing perspectives.

## Team role

**Engineer**

## Practice skill

`abd-acceptance-test-driven-development` — Write tests first from behavioral context. Orchestrator pattern, TDD cycle (RED-GREEN-REFACTOR), domain language, API design through failing tests.

## Entry conditions

- Story Definition exit gate passed.
- Scenario files exist with concrete Given/When/Then examples.
- `story-graph.json` contains stories with AC and scenario references.
- Target language and test framework are known or can be inferred from the workspace.

## Expected outputs

- Executable test files in the workspace (one class per behavior, one test per scenario).
- Tests are RED — they compile/parse but fail because production code does not yet exist.
- Test-to-story mapping documented (which test covers which story/AC/scenario).

## Key questions (is this stage done?)

1. Does every scenario from the previous stage have a corresponding executable test?
2. Are the tests RED — do they compile/parse but fail because production code does not yet exist?
3. Do tests follow the orchestrator pattern: high-level Given-When-Then methods that delegate to helper functions?
4. Does the test code read in domain language — can a non-engineer understand what behavior is being verified by reading the test name and structure?
5. Is there a clear mapping from each test back to its story, AC, and scenario?
6. Does the API surface implied by the tests (function signatures, class names, parameters) make sense as a domain-driven design?
7. Could a new developer read the test suite and understand the intended behavior of the system without reading any other documentation?

## Conditions of success

- **One class per behavior, one test per scenario:** Tests are organized around behaviors (stories), not around technical layers or modules.
- **Orchestrator pattern:** Test methods are high-level Given-When-Then sequences calling helper functions — not deep procedural scripts with setup, action, and assertion tangled together.
- **Domain language throughout:** Test class names, method names, helper names, and variable names use the vocabulary from upstream stages. The same words that appear in the story map and AC appear in the test code.
- **RED state confirmed:** All tests compile and run, but fail. This proves the test is meaningful — it will detect when the behavior is implemented.
- **Tests drive the design:** The function signatures and class interfaces that tests call are intentional design decisions, not accidents. The test suite is the first client of the production API.

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
