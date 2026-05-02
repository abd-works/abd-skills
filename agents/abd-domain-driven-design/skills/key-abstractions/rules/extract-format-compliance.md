---
scanner: extract-format-compliance
---

# Rule: Ref entry format compliance

Every `**Ref — …**` block must carry the required header fields: `Source:`, `Locator:`, and `Extract: whole|partial`. These fields are inherited from the UDL stage and must not be removed or malformed during key-abstractions enrichment. Passing means every ref block has a complete, well-formed header. Failing means a header field is missing or malformed.

## DO

- Preserve the `Source:` line pointing to the chunk file path.

  **Example (pass):**
  ```
  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole
  ```

- Preserve the `Locator:` line with a precise locator (lines, section heading, etc.).

  **Example (pass):** `Locator: lines 1238–1344`

- Set `Extract:` to exactly `whole` or `partial` (no other values).

  **Example (pass):** `Extract: whole`

## DO NOT

- Remove the `Source:` line from a ref header during enrichment.

  **Example (fail):** A ref block with title, Locator, and Extract but no Source line.

- Change `Extract:` to a value other than `whole` or `partial`.

  **Example (fail):** `Extract: summary` or `Extract: verbatim`.

- Malform the `**Ref —**` header (e.g. `##Ref —` or `*Ref —*`).

  **Example (fail):** `##Ref — Game Play##` instead of `**Ref — Game Play**`.
