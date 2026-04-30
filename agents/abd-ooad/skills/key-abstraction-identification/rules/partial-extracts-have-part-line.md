---
scanner: partial-extracts-have-part-line
---

# Rule: Partial extracts have Part line

Every extract marked `Extract: partial` must have a corresponding `Part:` line that names the slice in source-grounded terms. Conversely, `Extract: whole` must not have a `Part:` line. This ensures reviewers can reassemble sliced upstream extracts. Passing means the pairing is correct on every extract. Failing means a partial without `Part:` or a whole with an unnecessary `Part:`.

## DO

- When `Extract: partial`, include `Part:` naming the specific slice (paragraph range, bullet list, sentence group).

  **Example (pass):**
  ```
  Extract: partial
  Part: Sentences that define the generic transfer mechanism — before the wire/KYC paragraph.
  ```

- Name the slice in source-grounded terms a reviewer can locate in the upstream extract.

  **Example (pass):** `Part: The three-bullet list under "Outbound Wire Limits".`

- Omit `Part:` when `Extract: whole` (the entire passage lives here).

  **Example (pass):**
  ```
  Extract: whole
  ```
  (No `Part:` line.)

## DON'T

- Set `Extract: partial` without a `Part:` line.

  **Example (fail):**
  ```
  Extract: partial
  ```
  (Missing `Part:` — reviewer cannot identify which slice this is.)

- Add a `Part:` line to a `Extract: whole` block (contradicts the "whole" claim).

  **Example (fail):**
  ```
  Extract: whole
  Part: First two paragraphs only.
  ```
  (If it is only part of the passage, it should be `Extract: partial`.)
