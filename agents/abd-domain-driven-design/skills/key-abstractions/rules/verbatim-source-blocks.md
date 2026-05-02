---
scanner: verbatim-source-blocks
---

# Rule: Verbatim source blocks trace to disk

Every fenced `source` block must contain text copied byte-for-byte from a file on disk. The `Source:` line in the parent `**Ref —**` entry must reference a resolvable path — not agent memory, training data, or generated content. Passing means every source block can be traced to a real file. Failing means a source block uses generated content or points to a non-existent file.

## DO

- Reference real files on disk in the `Source:` line (context chunk files).

  **Example (pass):** `Source: context/rules/HeroesHandbook-rules__chunk_009.md`

- Copy text character-for-character from the source — preserve whitespace, bullets, markdown formatting, OCR artifacts.

  **Example (pass):** The source block body matches the file byte-for-byte.

- Stop and report to the user when a referenced source file does not exist on disk.

  **Example (pass):** Agent says "chunk_009.md not found — cannot add source extract."

## DO NOT

- Use markers that indicate generated content: `domain-knowledge`, `from memory`, `reconstructed`, `agent knowledge`.

  **Example (fail):** `Source: domain-knowledge — "Resolution Rules"` — no file to verify.

- Paraphrase, clean up, or reformat the source text inside source blocks.

  **Example (fail):** Agent rewrites bullet points into clean prose before placing them in the source block.

- Proceed with source block creation when the referenced file does not exist on disk.

  **Example (fail):** `Source: context/rules/HeroesHandbook-rules__chunk_099.md` but that file is not in the workspace.
