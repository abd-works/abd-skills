# Rule: No orphan contexts — every bounded context participates or is declared standalone

Every bounded context listed in the inventory must either appear in at least one dependency arc (as source or target) or be explicitly declared as **standalone** with a rationale in the Standalone Contexts section. A floating context with no arcs and no standalone declaration is a gap — the reviewer cannot tell whether it was forgotten or intentionally isolated. Failure is a bounded context that appears in the inventory but nowhere in the Dependencies or Standalone Contexts sections.

## DO

- Ensure every bounded context name from the inventory appears as either a source or target in at least one dependency arc.

  **Example (pass):**

  Inventory lists: Supply Operation, Trading, Invoice, Communication Gateway, DCF Folder, DCF Front Page. Each appears in at least one arc under Dependencies.

- When a bounded context genuinely has no integration with others, declare it in the Standalone Contexts section with a rationale.

  **Example (pass):**

  ```
  ## Standalone Contexts

  ### Reporting Data Warehouse
  Standalone. Consumes nightly batch extracts but has no runtime integration with other contexts.
  Rationale: read-only analytics; no domain model coupling. Separate Ways pattern applies.
  ```

## DO NOT

- List a bounded context in the inventory without it appearing in any dependency arc or the Standalone Contexts section.

  **Example (fail):**

  Inventory lists five contexts. Dependencies section has arcs for only four of them. The fifth context does not appear anywhere else in the document — the reader cannot tell if it was forgotten or intentionally left out.

- Assume that "no arc means standalone" without explicitly stating it in the Standalone Contexts section.

  **Example (fail):**

  ```
  ## Standalone Contexts

  No standalone contexts.
  ```

  But the Notification Service context from the inventory has no dependency arcs — the statement contradicts the evidence.
