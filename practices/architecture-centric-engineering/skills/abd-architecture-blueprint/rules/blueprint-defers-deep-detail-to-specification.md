# Rule: Blueprint defers deep detail to the specification

The blueprint stops at description; the architecture specification owns walkthroughs. The blueprint **must not** contain code-level walkthroughs of a mechanism, multi-participant sequence diagrams, full data schemas/DDL, test code, or per-component file structures — that material belongs in `abd-architecture-specification` output: the central `docs/architecture/specification/architecture-specification.md` plus per-folder `architecture-context.md` files (three tiers — mechanism, package, miscellaneous). Code-level patterns live inside the mechanism-tier context file's **Canonical Patterns** and **Class Specification** sections; multi-participant diagrams live in mechanism-tier `architecture-participants.drawio`; test-suite layout lives in the test-helpers package-tier context file. When a reader needs that level of detail, the blueprint must forward-link to the central spec rather than inline it. Failing means a single mechanism section runs to multiple pages of code, a class diagram with twenty types ships in the blueprint, or the blueprint duplicates content that already exists in any `architecture-context.md`.

## DO

- Forward-link to the central spec whenever a question naturally leads to deeper detail.

  **Example (pass):** "Caching — write-through, keys named `cat:{sku}:v{n}`. *See `docs/architecture/specification/architecture-specification.md` → Mechanisms → Caching for the full key convention, eviction strategy, and consistency guarantees.*"

- Keep diagrams in the blueprint to a single concern (one entity relationship, one ownership boundary, one mechanism overview). Multi-participant sequence diagrams belong in the mechanism-tier context file's Class Specification.

  **Example (pass):** Blueprint section 4 has a single classDiagram showing five entities. The spec's `src/orders/architecture-context.md` carries the five-participant sequenceDiagram for the order-placement flow.

- When code is genuinely useful to the blueprint reader, prefer a *one-line* contract signature over an implementation.

  **Example (pass):** "Components publish events through `IEventPublisher.publish(event: DomainEvent): Promise<void>`." (Signature only; defer the in-process bus implementation to the mechanism-tier context file's Canonical Patterns.)

## DO NOT

- Inline a full method body inside a mechanism subsection.

  **Example (fail):** Section 3.2 (Error Handling) has 40 lines of TypeScript showing the `ErrorTranslator.translate(error)` switch. That is specification content; the blueprint should describe the *role* and link to the Error Handling mechanism's `architecture-context.md`.

- Ship a sequence diagram with more than three participants in the blueprint.

  **Example (fail):** Section 3.1 (Security) has a six-lane sequence diagram covering the full Auth0 PKCE flow. Move it to the Authentication mechanism's `architecture-context.md` Class Specification; the blueprint just names the mechanism.

- Include the database schema or DDL.

  **Example (fail):** Section 4 (Data Architecture) prints the `CREATE TABLE orders (...)` statement with every column and index. The blueprint shows entity relationships and ownership; schemas belong with the Persistence mechanism's `architecture-context.md`.

- Embed a test-suite example.

  **Example (fail):** Section 5 (Testing Architecture) lists ten test methods of `OrderServiceDomainTests`. The blueprint names the tier; per-tier file layout, fixtures, and spec-alignment lives in the test-helpers package-tier `architecture-context.md` (e.g. `tests/domain-helpers/architecture-context.md`).

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); blueprint is description, `abd-architecture-specification` output (central spec + per-folder context files) is the walkthrough.
