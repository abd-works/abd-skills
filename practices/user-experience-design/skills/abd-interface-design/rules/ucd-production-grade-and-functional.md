# Rule: The implementation is production-grade and every AC is a working behaviour

**Scanner:** AI review

Every acceptance criterion for the screen is implemented as a working behaviour in the host framework, covered by at least one test named for the story title and clause number. No clause is silently deferred, stubbed, or marked TODO. The screen passes the host project's lint, format, type-check, and test gates.

## DO

- Map every AC clause to a working behaviour the user can trigger and observe.

  **Example (pass):** AC clause "WHEN the GM submits a path THEN the system re-validates it against game bridge requirements AND saves the path and continues startup if validation passes" — the `Continue` button calls a real validator, persists the path on success, and triggers the screen transition.

- Name tests so every AC clause is traceable.

  **Example (pass):** Test name `"Prompt for Game Directory if Invalid — AC 2: re-validates and continues on valid path"` — a reviewer can match this directly to the source clause.

- Follow the host project's existing conventions (folder layout, state management, styling approach, test framework).

  **Example (pass):** The host uses Vitest + React Testing Library; this screen's tests use the same.

## DO NOT

- Stub an AC clause as TODO and ship.

  **Example (fail):** `// TODO: validate path here` with the `Continue` button always navigating regardless of validity.

- Silence lint or type errors instead of fixing them.

  **Example (fail):** `// eslint-disable-next-line` or `// @ts-expect-error` over a line that hides a real defect.

- Invent a parallel architecture that ignores the host project's patterns.

  **Example (fail):** Introducing a new state-management library, a new test framework, or a new folder layout just for this screen.
