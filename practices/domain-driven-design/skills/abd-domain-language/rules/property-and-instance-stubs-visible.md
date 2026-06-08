# Rule: Properties belong on the parent concept — no stub heading for pure properties

**Scanner:** AI review

A property with **no independent behavior, invariants, or interactions** is mentioned only in the parent concept's bullets. It does **not** get its own `### heading`. A property earns its own `### heading` only when it has at least one of: its own invariant, its own behavior, or its own cross-concept interaction.

## DO

- Mention pure properties (values, timestamps, flags, identifiers) as bullets on the parent concept.

  **Example (pass):**
  ```
  ### ticket
  - carries *lineage*, *priority*, *entered_stage*, and *completed_stage* for timing and ordering
  ```

- Give a property its own `###` only when it has independent behavior or invariants.

  **Example (pass):**
  ```
  ### rank
  - supplies the base *modifier* for a *check*
  - **Invariant:** *ranks* must never be added directly; convert to *measures* first
  ```

## DO NOT

- Create a `### property_name` stub that only says "is a property of X".

  **Example (fail):**
  ```
  ### lineage
  - is a property of *ticket* — an ordered array of ancestor names
  ```
  ← No behavior, no invariant. Mention it in the *ticket* bullet instead.

- Silently omit a term from the Terms list if you decided it is a property — record the typing call in `#### Decisions made`.

**Source:** Inherited from abd-domain-language — property stubs.
