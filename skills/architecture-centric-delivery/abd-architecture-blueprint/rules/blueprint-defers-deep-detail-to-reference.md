# Rule: Blueprint defers deep detail to the reference

The blueprint stops at description; the reference owns walkthroughs. The blueprint **must not** contain code-level walkthroughs of a mechanism, multi-participant sequence diagrams, full data schemas/DDL, test code, or per-component file structures — that material belongs in `architecture-reference.md` (one section per mechanism, six parts each). When a reader needs that level of detail, the blueprint must forward-link to the reference rather than inline it. Failing means a single mechanism section runs to multiple pages of code, a class diagram with twenty types ships in the blueprint, or the blueprint duplicates content that already exists in the reference.

## DO

- Forward-link to the reference whenever a question naturally leads to deeper detail.

  **Example (pass):** "Caching — write-through, keys named `cat:{sku}:v{n}`. *See `architecture-reference.md` section 3.6 for the full key convention, eviction strategy, and consistency guarantees.*"

- Keep diagrams in the blueprint to a single concern (one entity relationship, one ownership boundary, one mechanism overview). Multi-participant sequence diagrams belong in the reference.

  **Example (pass):** Blueprint section 4 has a single classDiagram showing five entities. The reference has a five-participant sequenceDiagram for the order-placement flow.

- When code is genuinely useful to the blueprint reader, prefer a *one-line* contract signature over an implementation.

  **Example (pass):** "Components publish events through `IEventPublisher.publish(event: DomainEvent): Promise<void>`." (signature only, defer the in-process bus implementation to the reference.)

## DO NOT

- Inline a full method body inside a mechanism subsection.

  **Example (fail):** Section 3.2 (Error Handling) has 40 lines of TypeScript showing the `ErrorTranslator.translate(error)` switch. That is reference content; the blueprint should describe the *role* and link.

- Ship a sequence diagram with more than three participants in the blueprint.

  **Example (fail):** Section 3.1 (Security) has a six-lane sequence diagram covering the full Auth0 PKCE flow. Move it to the reference; the blueprint just names the mechanism.

- Include the database schema or DDL.

  **Example (fail):** Section 4 (Data Architecture) prints the `CREATE TABLE orders (...)` statement with every column and index. The blueprint shows entity relationships and ownership; schemas belong with the persistence mechanism reference.

- Embed a test-suite example.

  **Example (fail):** Section 5 (Testing Architecture) lists ten test methods of `OrderServiceDomainTests`. The blueprint names the tier; per-mechanism tests live in the reference.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); blueprint is description, reference is walkthrough.
