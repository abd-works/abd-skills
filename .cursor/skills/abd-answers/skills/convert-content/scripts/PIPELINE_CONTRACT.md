# abd-answers memory pipeline — path contract

**Do not invent alternate folders** for converted markdown, chunks, or RAG metadata. Everything lives under one pipeline root under the **repo** `data/assets` tree (not the optional hub override).

## Pipeline root

`<repo>/data/assets/abd-answers-memory-pipeline/` (or `files/data/assets/...` when `data/assets` is absent)

- Resolved by `resolveRepoDataAssetsAbs()` + `ABD_ANSWERS_PIPELINE_DIR` in TypeScript; `resolve_repo_data_assets_root()` in Python.
- **Not** the same as topics root when `ANSWERS_DEFAULT_HUB_PATH` points outside the repo — pipeline stays on disk under the abd-answers repo.

## PDF → markdown (generic post-process)

After MarkItDown extracts text from a `.pdf`, `convert_to_markdown.py` runs **`pdf_markdown_post.postprocess_pdf_markdown`** with the source path: **banner collapse**, **conservative regex heading promotion** (`CHAPTER` / `APPENDIX` / `PART` patterns), and **optional** PDF-outline alignment via **`pdf_outline_headings`** when **PyMuPDF** is installed (`pip install pymupdf`). Env: `PDF_SKIP_REGEX_HEADINGS`, `PDF_SKIP_OUTLINE_HEADINGS`.

**Corpus-specific** cleanup (one RPG book’s bespoke rules, chunking prep) belongs in a **downstream script or config**, not hardcoded for a single title in core modules.

## Stages (fixed subfolders)

| Stage        | Subfolder   | Role |
|-------------|-------------|------|
| Convert     | `markdown/` | Mirrored `.md` from PDFs etc.; chat embeds under `markdown/users/<user>/…/<chat>/` |
| Chunk       | `chunked/`  | Chunked markdown for embedding |
| RAG metadata | `rag/`     | Pinecone sync manifest (`pinecone-manifest.json`) — **TypeScript** `syncFolderToPineconeDelta` reads **`chunked/`** only for hub content (not `markdown/`) |

There is **no** local FAISS index or Python embed step in this repo; vector search is **Pinecone-only**.

## Source panel (assets scope)

Under `abd-answers-memory-pipeline/`, browse lists **only** a virtual `users/` folder (disk: `markdown/users/`). Chunked/RAG and the raw `markdown/` layout are not shown as siblings—operators only navigate **user** subfolders for include/exclude.

## Single sources of truth

- **TypeScript**: `packages/answers/server/src/abd-answers-paths.ts` — `resolvePipelineRootAbs()`, `resolvePipelineMarkdownAbs()`, `resolvePipelineChunkedAbs()` (Pinecone sync uses **chunked** only), `PIPELINE_*_SEGMENT`.
- **Python**: `scripts/source-convert/_config.py` — `PIPELINE_ROOT`, `PIPELINE_MARKDOWN`, `PIPELINE_CHUNKED`, `PIPELINE_RAG`.

New code must call these helpers or import `_config` — **never** hardcode a different `memory/` or `pipeline/` path unless migrating legacy data.

## Logging (full pipeline)

Use **`--log-file <path>`** on `convert_to_markdown.py` and `chunk_markdown.py` so each stage writes its own file (same style as historical `data/pipeline-full.log`: `=== <ISO> START|END ... ===` plus tee of stdout/stderr). **`run-full-pipeline.ps1`** uses `data/pipeline-convert.log`, `data/pipeline-chunk.log`, and a short `data/pipeline-run.log` for PowerShell step banners. Run Python with **`python -u`** (or `PYTHONUNBUFFERED=1`) so logs stay current.
