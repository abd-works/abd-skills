# Rule: Source accounting complete — no uncited passages

**Scanner:** Manual review

Every in-scope source passage must appear as a `**Ref —**` entry in the `### References` section of the concept that uses it. No source passage may be silently dropped. Passing means a reviewer can trace every source passage to a citation on a specific concept. Failing means a source passage exists in the referenced context but has no citation.

## DO

- Cite every in-scope source passage in the `### References` section of the concept it supports.

  **Example (pass):**
  ```
  ### check
  - is resolved by *rolling* a *d20*...

  ### Decisions made
  - ...

  ### References
  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole
  ```

- When a passage supports multiple concepts, cite it on each concept that uses it.

  **Example (pass):** `**Ref — Ranks & Measures**` appears under both `### Trait` and `### Rank` because both concepts draw from the same source passage.

- When a passage cannot be allocated to any concept, place it in `[Unallocated]` with its own ref.

## DO NOT

- Leave a referenced source passage without any citation in the file.

  **Example (fail):** The key-abstractions file references `chunk_009.md` but no `**Ref —**` entry in any concept mentions it.

- Remove `**Ref —**` entries that existed in the key-abstractions stage.

  **Example (fail):** A `**Ref —**` entry from key-abstractions has no corresponding entry anywhere in the domain-sketch.

- Bundle all references for an entire KA in one `### references` section at the end.

  **Example (fail):**
  ```
  ### concept_a
  - ...
  ### concept_b
  - ...
  ### references              ← all refs for entire KA here
  ```

**Source:** Engagement convention (domain-sketch skill), updated for per-concept structure.
