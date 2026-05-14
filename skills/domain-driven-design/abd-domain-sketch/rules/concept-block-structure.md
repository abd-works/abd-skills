# Rule: Concept block follows the per-concept structure

**Scanner:** Manual review

Each concept block must follow the prescribed structure: concept heading (no bold), verb-led behavior bullets with *italicized domain terms*, then `### Decisions made` and `### References` for that concept, followed by a `---` separator before the next concept. Property/instance stubs get a minimal heading with a classification note. KA headings use `## KAName` (no bold). Passing means every concept follows this structure. Failing means a concept uses bold headings, bundles decisions/references at the KA level, or omits separators.

## DO

- Use plain headings — no bold on KA headings or concept headings.

  **Example (pass):**
  ```
  ## Trait

  ### Trait
  - is a *quantifiable characteristic* of a *character*

  ### Decisions made
  - ...

  ### References
  **Ref — ...**
  ```

- Place `### Decisions made` and `### References` per concept, immediately after its behavior bullets.

  **Example (pass):**
  ```
  ### check
  - is resolved by *rolling* a *d20*, adding the *trait rank*...
  - **Invariant:** ...

  ### Decisions made
  - *Check* alone owns *success/failure*...

  ### References
  **Ref — Game Play**
  Source: ...

  ---

  ### Check Result
  - is produced by a *check*...

  ### References
  **Ref — Degrees Of Success And Failure**
  Source: ...

  ---
  ```

- Separate concept blocks with `---` horizontal rules.

  **Example (pass):** Every concept block ends with `---` before the next concept heading.

- Give property/instance terms a stub heading with a classification note.

  **Example (pass):**
  ```
  ### d20
  - is the instrument a *check* rolls — a property of *check*, not a separate concept

  ### References
  **Ref — The Die**
  Source: ...

  ---
  ```

## DO NOT

- Use bold on concept or KA headings.

  **Example (fail):**
  ```
  ## **Product Catalog**

  ### **product catalog**
  ```

- Bundle all decisions and references at the end of the KA.

  **Example (fail):**
  ```
  ### concept_a
  - ...
  ### concept_b
  - ...
  ### references              ← bundled for entire KA
  ### decisions made          ← bundled for entire KA
  ```

- Omit `---` separators between concept blocks.

  **Example (fail):** Two concept headings with no `---` between them.

- Silently drop terms classified as properties or instances without a stub heading.

  **Example (fail):** A term from the KA grouping has no heading in the sketch and is only mentioned in a decisions-made bullet with no reference.

**Source:** Correction — check-resolution engagement established per-concept structure as standard (replaces per-KA bundling).
