---
scanner: every-ref-has-source-block
---

# Rule: Every ref has a source block

After key-abstractions enrichment, every `**Ref —**` entry in the module file must be followed by a fenced `source` block containing verbatim text from the referenced chunk. Passing means every ref has a non-empty source block. Failing means a ref exists without a corresponding source block.

## DO

- Place a fenced `source` block immediately after the `Extract:` line of each `**Ref —**` entry.

  **Example (pass):**
  ```
  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole

  ```source
  GAME PLAY
  …verbatim text from chunk…
  ```
  ```

- Ensure the source block is non-empty — at least one line of content.

  **Example (pass):** Source block has 20 lines of verbatim text.

## DO NOT

- Leave a `**Ref —**` entry without a source block.

  **Example (fail):**
  ```
  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole

  #### next term
  ```
  (No source block between the ref and the next heading.)

- Place an empty source block.

  **Example (fail):**
  ```
  ```source
  ```
  ```
  (Empty body — must contain verbatim text.)
