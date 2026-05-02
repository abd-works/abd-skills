# Rule: Source accounting complete — no uncited passages

**Scanner:** Manual review

Every in-scope source passage must be mentioned as a `**Ref —**` entry at concept level, module level, or in `[Unallocated]` / `[Rejected]`. No source passage may be silently dropped. Passing means a reviewer can trace every source passage to a citation somewhere in the file. Failing means a source passage exists in the referenced context but has no citation.

## DO

- Cite every in-scope source passage at the most specific level possible — a `**Ref —**` entry under the concept is preferred.

  **Example (pass):** A concept carries `**Ref — Gate before ship**` with `Source:`, `Locator:`, `Extract: partial`, `Part:`.

- When a passage supports the whole module rather than one concept, cite it in the module-level `### Extract` inventory.

  **Example (pass):** `### Extract` bullet: `- Source: Fulfillment requirements | Locator: Policy ch.4 (warehouse gate)`

- When a passage cannot be allocated to any concept, place it in `[Unallocated]` with its own ref.

  **Example (pass):** `## Module: [Unallocated]` with a `**Ref —**` entry for the orphaned passage.

## DO NOT

- Leave a referenced source passage without any citation in the file.

  **Example (fail):** The module's Key Abstractions reference `chunk_009.md` but no `**Ref —**` entry mentions it.

- Remove `**Ref —**` entries that existed in the Key Abstractions stage.

  **Example (fail):** A `**Ref —**` entry from key-abstractions has no corresponding entry in the object sketch sections.

**Source:** Engagement convention (domain-sketch skill).
