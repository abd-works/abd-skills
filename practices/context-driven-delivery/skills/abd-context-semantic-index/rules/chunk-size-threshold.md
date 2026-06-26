# Rule: Chunk size threshold

Chunks should only be created from source files large enough to benefit from splitting. A file that is already 1–2 pages or shorter produces fragments too small for useful retrieval when subdivided. Passing means every chunk comes from a file that exceeded the size threshold, and no chunk is smaller than the minimum useful size. Failing means a short file was needlessly split, or a chunk is so small it carries no retrievable context.

## DO

- Only create chunks from source files that exceed roughly 1,500 characters (about 2 printed pages).

  **Example (pass):** `requirements.md` is 4,200 characters — split into two chunks of ~2,100 characters each. Both chunks carry enough context for retrieval.

- Pass through files at or below the threshold intact — assign view tags but do not subdivide.

  **Example (pass):** `glossary.md` is 900 characters — listed in the report as a pass-through with `primary_views: [domain]` and hierarchical tags, but no `chunk_NN` files are created from it.

- Keep individual chunks between roughly 800 and 3,000 characters so each piece is large enough to carry context but small enough for focused retrieval.

  **Example (pass):** A 6,000-character file is split into three chunks of approximately 2,000 characters each, each one covering a coherent section under its own heading.

## DO NOT

- Split a source file that is already at or below the size threshold (~1,500 characters).

  **Example (fail):** `api-notes.md` is 1,100 characters — the chunker produces `api-notes__chunk_01` (600 chars) and `api-notes__chunk_02` (500 chars). Both fragments are too small and the file should have passed through intact.

- Produce a chunk smaller than roughly 400 characters unless it is the final tail of a file and merging it with the prior chunk would exceed 3,000 characters.

  **Example (fail):** `requirements__chunk_07` is 180 characters containing only a heading and one sentence. It should have been merged with the preceding chunk.

- Ignore the threshold and chunk every file regardless of size.

  **Example (fail):** A batch of 20 source files includes 8 files under 1,000 characters. All 20 are split into chunks. The 8 small files should have been pass-throughs.
