### Rule: Mechanism, layer, and system names match the agreed source of truth

The names this spec uses for mechanisms, layers, and external systems MUST match the names used by the architecture's agreed source of truth — ADRs, blueprint, decision records, or the sibling skill that produced the vocabulary. The central spec and every context file MUST use the same spelling, the same casing, and the same scoping (`Identity Setup` is not `Identity` is not `Auth Setup`). If a name needs to change, update the source of truth first and then propagate. Passing means a reviewer can hold the central spec, a context file, and the source-of-truth document side by side and see one vocabulary across all three. Failing means a synonym appears in one place ("Persistence" vs "Infrastructure"), a mechanism is renamed locally to suit a section, or a layer the source-of-truth document does not contain appears in the spec.

#### DO

- Copy mechanism, layer, and external-system names verbatim from the source of truth.

  **Example (pass):** ADR-003 names the integration mechanism `Partner Integrations`. The Mechanisms section, Package Context, Source Layout tags, and every cross-reference all say `Partner Integrations` — same words, same casing.

- Cite the source of truth so a reviewer can trace vocabulary back.

  **Example (pass):**
  ```markdown
  ## Overview

  ...

  > **Sources:** Mechanism names from ADR-001 through ADR-007;
  > layer names from the blueprint § Layers;
  > external systems from the system context diagram.
  ```

- When a new mechanism or layer is needed, update the source of truth first, then regenerate.

  **Example (pass):** The team realises `Idempotency` is a missing mechanism. The architect writes ADR-008 first; once accepted, the central spec adds the Idempotency entry that points to the new ADR.

#### DO NOT

- Use a synonym for a named element.

  **Example (fail):** Caching section calls the storage layer `Storage`; Persistence section calls the same layer `Infrastructure`. Same folder, two names; the spec invents a synonym.

- Introduce a mechanism or layer the source of truth does not contain.

  **Example (fail):** The spec lists `Mechanism: Multi-tenancy` but no ADR, blueprint, or decision document mentions multi-tenancy. The spec has gone off-piste.

- Rename a mechanism to fit a section heading style.

  **Example (fail):** ADR-002 calls it `Configuration & Secrets`; the spec drops the ampersand and writes `Configuration and Secrets` for readability. The two names now diverge across documents.

- Drop a layer because it is small.

  **Example (fail):** The blueprint names five layers; the spec consolidates two into one because they "are basically the same". The vocabulary contract is broken.

**Source:** Ubiquitous Language (Evans, Domain-Driven Design) — the cost of two names for one concept is permanent confusion across the team.
