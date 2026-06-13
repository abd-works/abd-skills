# Rule: Principles are decidable one-sentence stances

Every guiding principle in the outline is **one sentence** and **decidable against a real code change or design proposal**. It names a constraint the system imposes on itself — not an aspiration. A reviewer should be able to look at a pull request and say "this violates principle 3" or "this is fine under principle 3". Failing means a principle is a paragraph, a slogan, a value statement, or so abstract that no piece of code could ever be measured against it.

## DO

- Every principle is one declarative sentence naming the constraint and the thing it constrains.

  **Example (pass):** "Domain never imports infrastructure — domain classes depend on interfaces; concrete database, HTTP, and message-bus types are referenced only from the Infrastructure layer."

- Every principle names a verifiable surface: a layer, a folder, a code path, or a build-time check.

  **Example (pass):** "Tests run without infrastructure — the full domain and application test suite runs in under 60 seconds with no databases, brokers, or third-party services started." Verifiable by running the test suite.

- The principles list contains 5–10 entries, each fitting on one bullet line with an optional short clarification clause.

  **Example (pass):** Eight principles, each a single sentence. The ninth candidate ("prefer immutability where cost is low") is deferred to the blueprint because it cannot be applied at outline level.

## DO NOT

- Express a principle as a value statement or slogan that cannot be applied to a code change.

  **Example (fail):** "We value craftsmanship and clean code." Undecidable — a reviewer cannot pass or fail a PR against this.

- Write a principle as a multi-paragraph entry.

  **Example (fail):** A principle entry is three paragraphs explaining context, options considered, and consequences. That is an ADR, not a principle.

- Embed implementation rules inside a principle.

  **Example (fail):** "Use `Result<T, E>` from the `neverthrow` library and avoid `try/catch` except at the HTTP boundary, configuring the library at `src/shared/result.ts`." This is implementation detail for a mechanism rule, not an outline-level principle.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the principles list is the outline's third load-bearing element.
