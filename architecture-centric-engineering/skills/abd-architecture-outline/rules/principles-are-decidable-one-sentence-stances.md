# Rule: Principles are decidable one-sentence stances

A guiding principle in the outline is **one sentence** and **decidable against a real code change or design proposal**. It names what the system constrains itself to do, not what every engineer should aspire to. A reviewer should be able to look at a pull request and say "this violates principle 3" or "this is fine under principle 3". Failing means a principle is a paragraph, a slogan, a value statement, or so abstract that no piece of code could ever be measured against it.

## DO

- State each principle as one declarative sentence naming the constraint and the thing constrained.

  **Example (pass):** "Domain never imports infrastructure — domain classes depend on interfaces; concrete database, HTTP, and message-bus types are referenced only from the Infrastructure layer."

- Give every principle a verifiable surface: a layer, a folder, a code path, or a build-time check.

  **Example (pass):** "Tests run without infrastructure — the full domain and application test suite runs in under 60 seconds with no databases, brokers, or third-party services started." (verifiable by running the suite.)

- Keep the principles list to 5–10 entries. If a candidate cannot fit alongside the others as a peer, it is probably not outline-level.

  **Example (pass):** Eight principles, each fitting on one bullet line plus an optional short clarification clause.

## DO NOT

- Write a principle as a value statement or slogan that cannot be applied to a code change.

  **Example (fail):** "We value craftsmanship and clean code." — true but undecidable; a reviewer cannot pass/fail a PR with this.

- Use multi-paragraph principles that read like a mini essay.

  **Example (fail):** A principle that is three paragraphs explaining context, options, and consequences — that is an ADR, not a principle.

- Mix principles with implementation rules.

  **Example (fail):** "Use `Result<T, E>` from the `neverthrow` library and avoid `try/catch` except at the HTTP boundary, configuring the library at `src/shared/result.ts`." — this is implementation detail for a rule, not a principle.

**Source:** Practice-skill authoring convention (abd-architecture-outline); principles list is the outline's third load-bearing element.
