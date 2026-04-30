---
scanner: extract-format-compliance
---

# Rule: Extract format compliance

Every `**Extract — …**` block must carry the required header fields: `Source:`, `Locator:`, `Extract: whole|partial`, and `Part:` when the extract is partial. Passing means every extract block has a complete, well-formed header. Failing means a header field is missing or `Extract: partial` appears without a `Part:` line.

## DO

- Include `Source:` on every extract pointing back one hop (partition file or corpus locator).

  **Example (pass):**
  ```
  **Extract — Funds Transfer (overview)**
  Source: module-partitioning.md — Module: [Funds Transfer] — "Funds Transfer (overview)"
  Locator: Ch.3 §Funds Transfer
  Extract: whole
  ```

- Include `Locator:` with a precise locator (chapter, page, lines, section heading).

  **Example (pass):** `Locator: Ch.5 §Wire Transfer — bullet list of limits`

- Set `Extract:` to exactly `whole` or `partial` (no other values).

  **Example (pass):** `Extract: partial`

- When `Extract: partial`, always include a `Part:` line naming the slice in source-grounded terms.

  **Example (pass):** `Part: Sentences that define the generic transfer mechanism — before the wire/KYC paragraph.`

## DON'T

- Omit the `Source:` line from an extract header.

  **Example (fail):** An extract block with title, Locator, and Extract type but no Source line.

- Use vague `Part:` descriptions like "the relevant bit" or "see above".

  **Example (fail):** `Part: the relevant section` — not source-grounded.

- Set `Extract:` to a value other than `whole` or `partial`.

  **Example (fail):** `Extract: summary` or `Extract: paraphrased`.

- Omit `Part:` when `Extract: partial` is set.

  **Example (fail):** `Extract: partial` with no `Part:` line following it.
