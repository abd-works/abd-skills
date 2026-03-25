# Output Structure

## Per-topic layout (`index_memory --path` / `--output …/memory`)

- **Convert:** For each original at `topic/…/file.ext`, markdown is `topic/markdown/…/file.md` (a **`markdown/`** folder at the topic root, parallel to **`memory/`**, same relative path under it as the original).
- **Chunk:** `topic/memory/…` mirrors the source tree **without** any `markdown` directory in the path (e.g. source `markdown/notes/x.md` → chunks under `memory/notes/`).

## Chunk source reference

Each chunk includes: `<!-- Source: path | file://url -->` for navigation.

## Legacy notes

Older docs may mention `converted/` / `chunked/` under `memory/name/`; current scripts use **`markdown/`** at the source and chunk files under **`memory/`** with `__slide_NN` / `__section_NN` suffixes.
