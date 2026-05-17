### Rule: Reference is grounded in abd-architecture-description and abd-architecture-mechanisms

The **layer names** in the reference document must match the output of **abd-architecture-description** for the same architecture, and the **mechanism names** must match the output of **abd-architecture-mechanisms**. The reference document is the join of those two skills; it does not invent layers, rename them, or add mechanisms the mechanisms skill never listed. When the reference needs a layer or mechanism that the upstream skills do not contain, the upstream skill is updated first and the reference is regenerated. Passing means a reviewer can hold the abd-architecture-description output, the abd-architecture-mechanisms output, and the reference side-by-side and see the same vocabulary in all three. Failing means the reference uses a synonym (`Persistence layer` vs `Infrastructure`), drops a layer, or introduces a mechanism that nobody else has heard of.

#### DO

- Copy or summarize the layer block from **abd-architecture-description** into the **Architecture Layers** section of the reference, keeping layer names byte-for-byte identical.

  **Example (pass):** `abd-architecture-description` names four layers `Presentation`, `Interface Adapters`, `Application`, `Domain Core`, `Infrastructure`. The reference's `Architecture Layers` section lists the same five names in the same order.

- For each mechanism, cite the **abd-architecture-mechanisms** entry that it implements, near the mechanism heading.

  **Example (pass):** `## Mechanism: Caching` is followed by the line `> Source intent: abd-architecture-mechanisms entry for Caching.`

- When a mechanism is missing from **abd-architecture-mechanisms**, **stop and add it there first** before adding it to the reference.

  **Example (pass):** The team realizes `Idempotency` is needed; the reference author updates `abd-architecture-mechanisms` first, regenerates its output, then adds the `Idempotency` section to the reference.

#### DO NOT

- Rename a layer to suit the mechanism (e.g. call it `Storage` in the caching section and `Infrastructure` in the persistence section).

  **Example (fail):** Mechanism `Caching` describes a `Storage layer` while `Persistence` describes an `Infrastructure layer` — same code lives in the same folder; the reference invented two names.

- Add a mechanism that does not appear in **abd-architecture-mechanisms**.

  **Example (fail):** The reference includes `Mechanism: Multi-tenancy` but the `abd-architecture-mechanisms` output for this architecture has no Multi-tenancy entry — the reference has gone off-piste.

- Reorder or merge layers in a way that contradicts **abd-architecture-description**.

  **Example (fail):** `abd-architecture-description` lists `Domain Core` between `Application` and `Infrastructure`; the reference puts `Domain Core` at the top and merges `Application` into `Interface Adapters`.

**Source:** Practice-skill authoring convention (abd-architecture-reference); preserves the contract with **abd-architecture-description** and **abd-architecture-mechanisms** that downstream tooling depends on.
