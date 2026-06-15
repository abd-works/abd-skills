### Rule: Reference is grounded in the architecture's source of truth

The **layer names** in the reference document must match the **agreed source of truth** for the same architecture — whatever form that takes (an ADR, a wiki page, a decision document, a sibling skill's output, or any other agreed record). The **mechanism names** must also match that source. The reference does not invent layers, rename them, or add mechanisms nobody else has heard of. When the reference needs a layer or mechanism that the source of truth does not yet contain, update the source of truth first, then regenerate the reference. Passing means a reviewer can hold the reference and the architecture's source of truth side-by-side and see the same vocabulary in both — same layer names, same mechanism names, same spelling. Failing means the reference uses a synonym (`Persistence layer` vs `Infrastructure`), drops a layer, or introduces a mechanism that the agreed source of truth never listed.

#### DO

- Copy or summarize the layer block from the architecture's agreed source of truth into the **Architecture Layers** section of the reference, keeping layer names byte-for-byte identical.

  **Example (pass):** The team's ADR lists four layers `Presentation`, `Application`, `Domain Core`, `Infrastructure`. The reference's `Architecture Layers` section lists the same four names in the same order, sourced from the ADR.

- Cite the source of truth for layers and mechanisms near the relevant sections so a reviewer can trace the names back.

  **Example (pass):** The Overview contains the line `> Sources: layers from ADR-0012; mechanisms from the team's architecture playbook.` — a reviewer knows exactly where the layer and mechanism vocabulary came from.

- When a mechanism is missing from the source of truth, **stop and add it there first** before adding it to the reference.

  **Example (pass):** The team realizes `Idempotency` is needed; the reference author updates the mechanism inventory doc (or the sibling skill's output) first, then adds the `Idempotency` section to the reference.

#### DO NOT

- Rename a layer to suit the mechanism (e.g. call it `Storage` in the caching section and `Infrastructure` in the persistence section).

  **Example (fail):** Mechanism `Caching` describes a `Storage layer` while `Persistence` describes an `Infrastructure layer` — same code lives in the same folder; the reference invented two names for the same layer.

- Add a mechanism that does not appear in the architecture's agreed source of truth.

  **Example (fail):** The reference includes `Mechanism: Multi-tenancy` but the mechanism inventory for this architecture has no Multi-tenancy entry — the reference has gone off-piste.

- Reorder or merge layers in a way that contradicts the agreed source of truth.

  **Example (fail):** The source lists `Domain Core` between `Application` and `Infrastructure`; the reference puts `Domain Core` at the top and merges `Application` into `Interface Adapters`.

**Source:** Practice-skill authoring convention (abd-architecture-template); preserves the vocabulary contract between the reference and the team's agreed architecture context, wherever that context lives.
