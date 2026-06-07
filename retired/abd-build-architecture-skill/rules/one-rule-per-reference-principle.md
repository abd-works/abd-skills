### Rule: One generated rule per reference principle

For every **Principles & Patterns** subsection in the reference document, the generated skill must ship one corresponding `rules/<principle-slug>.md` file whose `Example (pass)` block matches the principle's named pattern and whose `Example (fail)` block matches the anti-pattern named in (or strongly implied by) the reference walkthrough. This is the **one-to-one trace** that lets a reviewer hold the reference and the generated skill side-by-side and confirm coverage. Passing means each principle has a rule, each rule has a pass and fail example, and a reviewer can match them in either direction. Failing means a principle has no rule, a rule does not name the principle it implements, or the same rule tries to cover three unrelated principles.

#### DO

- Walk every `Mechanism: <Name>` section's `Principles & Patterns` subsection. For each principle line, create one rule file named after the **valid state** the principle guards (e.g. `maintain-layer-purity.md`, `handle-errors-at-boundary.md`, `cache-via-side-car.md`).

  **Example (pass):** Reference's Caching mechanism states "Principle: the application layer is unaware of the cache." → generated skill contains `rules/keep-application-unaware-of-cache.md` whose opening paragraph begins "The application layer must never call cache APIs directly. From the Caching section of `inputs/architecture-reference.md`..."

- Use the pattern named in the reference as the rule's `Example (pass)`; use the "WRONG" code from the reference's walkthrough (or a paraphrase) as the `Example (fail)`.

  **Example (pass):** `rules/keep-application-unaware-of-cache.md` `Example (pass)` shows the `CachingRecipientsRepository` side-car (the named pattern); `Example (fail)` shows a service calling `redis.get(...)` directly (the anti-pattern).

- Tag each generated rule with a `Source:` line that points back at the reference section.

  **Example (pass):** Rule ends with `Source: inputs/architecture-reference.md — section "Mechanism: Caching", under "Principles & Patterns".`

#### DO NOT

- Skip principles the reference lists because "they're obvious" or "they're already in the project's coding standard".

  **Example (fail):** Reference lists four principles for Error Handling; generated skill has only two rule files, the other two are silently dropped.

- Lump multiple principles into one rule file.

  **Example (fail):** `rules/architecture-correctness.md` has six `DO` bullets pulled from six different reference principles. A reviewer cannot tell which violation maps to which `DO`.

- Invent a rule that is **not** in the reference (even if it sounds sensible).

  **Example (fail):** Generated skill includes `rules/use-graphql-instead-of-rest.md`. The reference does not mention GraphQL — the generated skill has drifted from its source.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); the reference→rule trace is what makes the generated skill auditable against its source document.
