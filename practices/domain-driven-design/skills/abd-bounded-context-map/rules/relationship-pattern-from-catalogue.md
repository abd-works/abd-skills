# Rule: Relationship pattern from the DDD/ABD catalogue

The team engagement model on every dependency arc must name a recognized pattern from the DDD strategic patterns catalogue or the ABD team collaboration models. Ad hoc labels ("we'll figure it out", "hybrid approach", "loose coupling") do not encode the specific trade-offs each named pattern carries. Failure is a dependency whose team engagement model uses an invented label instead of a named pattern.

## DO

- Name one of the recognized **DDD relationship patterns** for each dependency: Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service/Published Language, or Separate Ways.

  **Example (pass):**

  ```
  - Team engagement model: Anticorruption Layer — Front Page isolates itself from the legacy Supply Operation model
  ```

- When the arc also has a **team collaboration model**, name it from the ABD catalogue: Travelling Team Members, Service Provider, or Enabler.

  **Example (pass):**

  ```
  - Team engagement model: Customer/Supplier — Travelling Team Members (significant change requires cross-team pairing)
  ```

- When two patterns apply (a DDD relationship pattern plus an ABD team collaboration model), name both explicitly.

  **Example (pass):**

  ```
  - Team engagement model: Open Host Service / Published Language — Enabler (Gateway team provides transport; DCF team consumes self-service)
  ```

## DO NOT

- Use ad hoc labels that do not appear in the DDD or ABD catalogues.

  **Example (fail):**

  ```
  - Team engagement model: loose coupling with occasional syncs
  ```

  "Loose coupling with occasional syncs" is not a named pattern — it hides the actual power dynamic and collaboration commitment.

- Name only a team collaboration model without the DDD relationship pattern (or vice versa) when both are relevant.

  **Example (fail):**

  ```
  - Team engagement model: Service Provider
  ```

  Service Provider describes team collaboration but does not say whether the relationship is Customer/Supplier, Conformist, or something else. Both dimensions are needed.

**Source:** Kept chunk #2 in `inputs/abd-answers-retrieval.md` — seven relationship patterns (Evans); Kept chunk #9 — ABD Model Sharing Patterns catalogue; Kept chunk #7 — ABD team engagement models.
