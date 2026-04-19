# Source convert (abd-answers fork)

**Path contract:** convert and chunk stages use `<repo>/data/assets/abd-answers-memory-pipeline/{markdown,chunked}/` only. **`rag/`** holds Pinecone sync metadata (manifest under `rag/`), not a local vector index. See **`PIPELINE_CONTRACT.md`** — new code must not use ad-hoc pipeline roots.

Copied from `abd_content/skills/abd-context-to-memory/scripts` and adjusted so outputs match **abd-answers** hub layout (see `packages/answers/server/src/abd-answers-paths.ts`):

| Stage | Destination |
|--------|-------------|
| Convert | `data/assets/abd-answers-memory-pipeline/markdown/` (under abd-answers repo) |
| Chunk (default) | `data/assets/abd-answers-memory-pipeline/chunked/` |

**Topics (Source tile)** use `resolveSourceFilesRootAbs()` (hub / `ANSWERS_DEFAULT_HUB_PATH` / repo `data/assets`). **Pipeline** (markdown, chunked, rag) is always repo `data/assets/abd-answers-memory-pipeline/` (or `files/data/assets/...`), same as TypeScript `resolvePipelineRootAbs()` — not overridden by the hub path.

## Env

- `ANSWERS_DEFAULT_HUB_PATH` — hub directory for topics: either the `assets` folder or its parent (see `abd-answers-paths.ts`), optional if `data/assets` exists in the repo
- `OPENAI_API_KEY` — from `conf/.secrets` or env (loaded by `_config.py`)

## Commands

From repo root:

```bash
cd scripts/source-convert
python convert_to_markdown.py --memory .
python chunk_markdown.py --path .
```

**Pinecone** (embed + sync from **`chunked/`** only): `npx tsx scripts/migrate-memory-to-pinecone.ts`. Full wipe + re-embed: `npx tsx scripts/migrate-memory-to-pinecone.ts --wipe`.

Convert/chunk skip **`…/abd-answers-memory-pipeline/rag/`** (and legacy **`…/assets/rag/`**) — those trees are manifest-only, not corpus (`path_is_pinecone_rag_metadata_only` in `_config.py`).

## Upstream

When behavior in the skill changes, merge updates from:

`abd_content/skills/abd-context-to-memory/scripts/`

…then re-apply path differences documented above.
