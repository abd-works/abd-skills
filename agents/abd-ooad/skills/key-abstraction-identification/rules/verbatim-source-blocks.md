---
scanner: verbatim-source-blocks
---

# Rule: Verbatim source blocks trace to disk

Every ```` ```source ```` block must contain text copied byte-for-byte from a file on disk. The `Source:` line must reference a resolvable path or a known partition entry — not agent memory, training data, or generated content. Passing means every extract can be traced to a real file. Failing means a Source line uses generated-content markers or points to a non-existent file.

## DO

- Reference real files on disk in the `Source:` line (partition file, corpus chunk, or context directory file).

  **Example (pass):** `Source: module-partitioning.md — Module: [Funds Transfer] — "Funds Transfer (overview)"`

- Copy text character-for-character from the source — preserve OCR artifacts, page numbers, whitespace, and bullet formatting.

  **Example (pass):** The ```` ```source ```` body matches the file byte-for-byte when opened.

- Stop and report to the user when no source files exist on disk rather than generating content from memory.

  **Example (pass):** Agent says "No source files found under context/ — please load source material before running this skill."

## DON'T

- Use markers that indicate generated content: `domain-knowledge`, `application-requirements`, `training data`, `from memory`, `reconstructed`, `agent knowledge`.

  **Example (fail):** `Source: domain-knowledge — "Settlement Rules"` — no file to verify.

- Paraphrase, clean up, or reformat the source text inside ```` ```source ```` blocks.

  **Example (fail):** Agent rewrites OCR-scanned bullet points into clean markdown before placing them in the source block.

- Proceed with extract creation when the referenced file does not exist on disk.

  **Example (fail):** `Source: context/rules/ch04-transfers.md` but that file is not present in the workspace.
