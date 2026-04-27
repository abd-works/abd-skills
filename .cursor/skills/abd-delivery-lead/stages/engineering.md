# Engineering

## Purpose

Implement production code that makes the acceptance tests pass. Follow clean code principles: domain language, single responsibility, explicit dependencies, guard clauses, and continuous refactoring. The GREEN and REFACTOR phases of TDD.

TDD uses small, fine-grained steps to gradually increase developer confidence, which results in larger steps downstream. It is the tests that drive the development, not the other way around — the test either dictates the implementation or gives good pointers toward it.

## Why this stage matters

- **GREEN means done:** Production code exists to make tests pass — nothing more. If there is no failing test for a behavior, that behavior should not be implemented. This prevents scope creep at the code level.
- **Refactoring is continuous, not deferred:** The REFACTOR phase happens after every GREEN, not as a separate cleanup sprint. Coding standards, clean separations of concern, and DRY structure are maintained in real time.
- **Domain language in code:** The same vocabulary from discovery, AC, scenarios, and tests appears in production class names, method names, and variable names. Code reads as an expression of the domain, not as generic programming abstractions.
- **Collective ownership:** New code should look like existing code. The team has a single style guide and coding standard. Original authorship is immaterial — anyone can modify any code at any time, backed by the confidence that plentiful automated tests provide safety.
- **Separate construction from usage:** Clean code separates business logic from infrastructure concerns using factories or dependency injection, keeps crosscutting concerns isolated, and expresses the business layer as domain objects rather than framework-coupled code.

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

## Key questions (is this stage done?)

1. Do all acceptance tests pass (GREEN)?
2. Has every GREEN been followed by a REFACTOR pass — or is there deferred cleanup?
3. Do class and function names use domain language from the story map and AC, or have generic programming names crept in?
4. Can each class or module explain its single responsibility in one sentence?
5. Are dependencies explicit (constructor injection) or are there hidden globals, singletons, or service locators?
6. Is there duplication that could be extracted into a shared abstraction?
7. Could a developer new to the codebase read a production module and understand which story behavior it implements?
8. Are third-party API boundaries wrapped and tested with learning tests?

## Conditions of success

- **All acceptance tests GREEN:** The behavioral contract defined by upstream stages is fully satisfied.
- **Classes are compact and cohesive:** Lean toward many fine-grained classes rather than a few bloated ones. Dead code is eliminated. Private method behavior that applies to only a small subset is broken out.
- **Functions are small and intention-revealing:** Each function does one thing, named for what it does, with parameters that make sense to the caller.
- **Dependencies are explicit:** Construction is separated from usage. Business logic does not know about infrastructure. Crosscutting concerns are isolated.
- **Domain language is pervasive:** The code uses the same terms as the story map, AC, scenarios, and tests. A domain expert could read class and method names and recognize the product's vocabulary.
- **No duplication:** Every piece of knowledge has a single, unambiguous representation in the codebase.
- **Tested boundaries:** Third-party APIs are wrapped, and learning tests define expected behavior of external dependencies.

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
