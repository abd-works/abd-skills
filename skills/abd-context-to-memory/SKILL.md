---
name: abd-context-to-memory
description: >-
  Converts documents (PDF, PPTX, DOCX, XLSX, etc.) to markdown and chunks them
  for agent memory. Supports vector RAG search.   Chunked junctions usually live on the workspace root; optional roots/ manifest
  only if requested. Use when the user wants to "add
  to memory", "convert and chunk", "ingest content for agent", "refresh memory",
  "use memory", or process a folder of documents for AI agent context.
license: MIT
metadata:
  author: agilebydesign
  version: "1.2.4"
---

# Ace-Context-to-Memory

Converts source documents to markdown and chunks them for agent memory. Pipeline: **convert** (documents → markdown + images) → **chunk** (markdown → smaller files); **embed** (vector index) is optional — **`index_memory --embed`** or **`embed_and_index.py`** separately.

## When to Activate

- User asks to "add content to memory" or "refresh memory"
- Wants to convert a folder of documents (PPTX, PDF, DOCX, XLSX) for agent context
- Mentions "convert and chunk", "ingest for agent", or "memory pipeline"
- Has added new files and wants them processed
- **"Use memory" / semantic retrieval:** User says "use memory", "search memory", "what does memory say about X", "from our content", "from ABD materials", "what do we have on [topic]" — run `search_memory "<query>"` and inject results into your response
- **Adding content from any folder:** When adding a folder's content to memory, run `link_workspace_source.py --path <folder>` first (on request) if the link does not yet exist
- **Junction-only hubs (generic, reusable):** Configure hubs in **your workspace** (e.g. **`abd_content/conf/content_memory_roots.json`**), not inside the skill repo. Copy **`agilebydesign-skills/conf/content_memory_roots.example.json`** as a template. Each entry needs **`path`** (local hub root) and **`rag_path`** (where the **aggregate** FAISS index lives — usually **not** inside `path`, e.g. SharePoint). Optional **`junctions_dir`** (default **`assets`**) is the **local** subfolder under `path` where topic junctions live — name it anything (`links`, `sources`, …); it is **not** tied to SharePoint’s “Assets” library name. **`index_memory --path "<source folder>"`** writes chunks under **`<source>/memory/`** and auto-creates **`<hub>/<junctions_dir>/<source_folder_name>` → that `memory` folder**. Hub root: **`--memory-root`** / **`--junction-workspace`**, **`ABD_CONTENT_ROOT`**, or cwd. **`--no-junction`** to skip. **`CONTENT_MEMORY_JUNCTIONS_DIR`** overrides `junctions_dir` for one run. Discovery: **`CONTENT_MEMORY_WORKSPACE`**, **`CONTENT_MEMORY_ROOTS_CONFIG`**, walk cwd, or **`conf/content_memory_workspace.json`**. See **`agilebydesign-skills/conf/README.md`**.

## CRITICAL: Respect User Scope

- **One file**: When user says "one file", "this file", "just X.pdf", or names a specific file → use `--file <path>`. Process ONLY that file.
- **Folder**: When user says "folder", "all", "everything in X", or explicitly requests a folder → use `--memory <path>`.
- **Do NOT** process entire folders when the user asked for a single file.

## OneDrive Folder Clarification

When the user refers to "OneDrive", "OneDrive folder", "slash OneDrive", or similar without specifying which OneDrive:

- **Ask which OneDrive folder** they mean (e.g. "OneDrive - Agile by Design", "OneDrive - Personal", "OneDrive - Company Name").
- If multiple OneDrive folders exist under the user's home and the configured path is missing or unclear, scripts will list them and prompt for choice — **do not guess**; ask the user to pick.
- If the user's request is ambiguous (e.g. "use OneDrive" or "get to OneDrive"), ask: "Which OneDrive folder do you want to use? For example: OneDrive - Agile by Design, OneDrive - Personal, or another?"

## Source Folder Structure

`source/` (under workspace root) contains content sources. Workspace folders can be linked for skill access:

- `source/<link_name>` — Junction/symlink to your content folder

Use `link_workspace_source.py` to create links before converting.

**Memory root:** For **`--path`**, ROOT is the **source folder** you pass (`memory/` holds chunks). Embedding is separate unless **`--embed`**. Set `CONTENT_MEMORY_ROOT` only when running `--memory` without a source.

## Chunk junctions and optional `roots/` manifest

**Default:** After **`index_memory.py --path "<source>"`**, auto-junction is **`<hub>/<junctions_dir>/<source_folder_name>` → `<source>/memory`** (`junctions_dir` from **`content_memory_roots.json`**, default **`assets`**; or **`…/memory/context`** for a `context` folder). Hub root: **`--memory-root`** / **`--junction-workspace`**, **`ABD_CONTENT_ROOT`**, or cwd. Disable with **`--no-junction`** or **`SKIP_MEMORY_JUNCTION=1`**. **Legacy** `chunked_*` layouts exist in `memory_junction.ensure_memory_junction` for manual use only. **Do not** use `roots/` unless the user explicitly wants that structure.

**Optional `roots/` layout:** For workspaces that want a **manifest** (`roots/roots.json`) and `roots/<name>/chunked`, each junction points at the absolute **memory** folder for that tree.

Example `roots/roots.json`:

```json
{
  "roots": [
    {
      "name": "assets",
      "memory_path": "C:/Users/<you>/OneDrive - Agile by Design/Shared Documents/Assets/memory",
      "chunked_junction": "chunked"
    }
  ]
}
```

- **name** — Folder under `roots/` (e.g. `roots/assets/`).
- **memory_path** — Absolute path to the memory folder (chunk+embed output). Junction target for `chunked`.
- **chunked_junction** — Name of the junction under the root folder (default `chunked`).

**Agent flow — add hub link (default):** (1) **`--path`** = source folder; junction **`<hub>/<source name>`** → **`<source>/memory`**. (2) Override hub with **`--memory-root <abd_content>`**. (3) Manual rename: remove junction and `mklink /J "<hub>\\<name>" "<absolute path to …\\memory>"`.

**Agent flow — `roots/` only when requested:** Same as before using `add_root.py` / `link_chunked.py` and `roots/roots.json`.

Run scripts from workspace root; use `--workspace <path>` if the working directory is not the workspace.

## Pipeline Overview

1. **Convert**: Use `markitdown` to convert supported files to markdown under **`<topic_root>/markdown/…`**, parallel to **`memory/`** (same relative paths as originals). Images extracted and referenced. **SharePoint links**: When source is in OneDrive, SharePoint URLs are auto-injected from `sharepoint_mapping.json` so links work for anyone.
2. **Chunk**: Split large markdown by slides (decks) or headings (docs). Small files stay as single chunks. For each stem, prefer **`markdown/…/<stem>.md`**, then legacy **`…/markdown/<stem>.md`**, else sibling **`<stem>.md`**, never both. Output under **`<source>/memory/`** mirrors subfolders **without** a `markdown` segment (e.g. `markdown/notes/x.md` → `memory/notes/…`). **`.md` under `<source>/memory/` is never chunk input** (avoids `memory/memory/` duplication).
3. **Index chunks**: Build `chunk_index.json` (reverse index: chunk ID → path, heading, size) alongside the chunk folder under `memory/`. Use for evidence lookup (which chunk file/section a passage came from).
4. **Sync SharePoint URLs**: Replace source paths with SharePoint URLs; fix URL order; add `wdSlideIndex` (pptx) / `page` (pdf) for direct slide/page links. Run automatically in `index_memory --path` pipeline.
5. **Embed + Index** (RAG): Not run by **`index_memory`** unless **`--embed`**. Otherwise run **`embed_and_index.py`** (hub aggregate) or **`index_memory --embed`** (per-topic **`memory/rag/`**). **Hub** (aggregate, no `--memory`): set **`rag_path`** per hub in **`conf/content_memory_roots.json`**, or use **`content_memory_rag_path`** / **`CONTENT_MEMORY_RAG_PATH`**. Fallback: **`<hub>/<junctions_dir>/rag`**.

## Semantic Search (RAG)

When the user says "use memory", "search memory", "what does memory say about X", "from our content", or asks about ABD materials:

1. Run from workspace root: `python skills/abd-context-to-memory/scripts/search_memory.py "<query>" --k 5`
2. Inject the returned chunks into your response
3. Cite sources (path, slide/page) when using retrieved content

Requires RAG deps: `pip install -r skills/abd-context-to-memory/requirements-rag.txt`

**API key:** Put `OPENAI_API_KEY` in **`agilebydesign-skills/conf/.secrets`** (or `conf/.env`) — same dotenv format as `.env`. Scripts load this via `_config.py` before embed/search. A `.env` in the current working directory can override for a specific project.

See `conf/README.md` in the skills repo. See `content/rag-retrieval.md` for trigger phrases and agent flow.

## Scripts

Run from workspace root. Scripts in `skills/abd-context-to-memory/scripts/`.

**RAG (vector search):**
- `index_memory.py --path <source_folder> [--embed] [--memory-root <hub>] [--junction-workspace <hub>] [--no-junction]` — convert → chunk → sync SharePoint → **embed only with `--embed`** (default skips embed); optional **`<hub>/<source name>`** junction to that source’s memory folder
- `index_memory.py` — when `skill_space_path` is set and no folder specified, runs on `{skill_space_path}/context` automatically
- `index_memory.py --replace` — rebuild entire vector index from all memory
- `search_memory.py "<query>" [--k 5] [--format text|json]` — semantic search; returns top-k chunks

**Convert + chunk + index:**
- `link_workspace_source.py --path <folder> [--name <link_name>]` or `--workspace <folder_name>` — **run on request** when adding content to memory; creates junction/symlink in `source/` so skills can access the folder
- `add_root.py` / `link_chunked.py` — **only if the user wants a `roots/` layout**; otherwise use `mklink /J` (or symlink) on the workspace root to each `memory/` folder
- `convert_to_markdown.py --file <file_path> [--topic-root <topic_folder>]` — **single file only** (use when user asks for one file); writes markdown under **`markdown/…`** under the topic root
- `convert_to_markdown.py --memory <source_path>` — folder (all supported files). When source is in OneDrive, SharePoint URLs are auto-injected via `sharepoint_mapping.json`.
- `chunk_markdown.py --path <source_folder> [--memory <memory_name>]` — reads from source, writes to memory/<name>/
- `index_chunks.py --context-path <chunk_folder> [--output <path>]` — build chunk_index.json (chunk_id → path, heading). Run after chunk. Writes to `<chunk_folder>/chunk_index.json` by default (under memory).
- `embed_and_index.py [--memory <memory_name>] [--replace]` — embed chunks; aggregate hub writes to configurable RAG dir (default **`assets/rag/`**) or **`memory/rag/`** (when `--memory` set). Called by **`index_memory`** only when **`--embed`** is passed.
- `sync_sharepoint_urls.py [--memory <memory_name>]` — run after chunk when source has `source/... | https://...`; replaces with SharePoint URL, fixes URL order, adds `wdSlideIndex` (pptx) / `page` (pdf) for direct links
- `add_sharepoint_mapping.py --prefix "OneDrive - X" --base "<url>"` — add OneDrive→SharePoint mapping. Paste URL from browser; script derives base. Use when convert warns about missing mapping.

**Export (markdown → Excel, Word, PDF):**
- `markdown_to_excel.py <input.md> [output.xlsx]` — generic md → Excel (headings, tables, paragraphs)
- `markdown_to_docx.py <input.md> [output.docx]` — md → Word (requires pandoc)
- `markdown_to_pdf.py <input.md> [output.pdf]` — md → PDF (requires pandoc + PDF engine). Use `--pdf-engine weasyprint` if pdflatex not installed.

Requires: `pip install -r requirements-export.txt` (openpyxl, pypandoc). Project-specific exports (e.g. JBOM format) stay in workspace.

**When adding content from a folder to memory:** Run `link_workspace_source.py` first if the link does not yet exist. Examples:
```bash
python scripts/link_workspace_source.py --path "C:/docs/RFQ materials" --name "JBOM"
python scripts/link_workspace_source.py --workspace "Scotia Talent Journey Based Operating Model" --name "JBOM Agile Support"
```

**SharePoint link creation:** When copying content from OneDrive, local paths are not shareable. Configure `sharepoint_mapping.json` (OneDrive prefix → SharePoint base URL). Convert will auto-inject SharePoint URLs so links work for anyone. **If you run convert with OneDrive content but no mapping, you'll get a warning with instructions.** Add the mapping with `add_sharepoint_mapping.py --prefix "OneDrive - X" --base "<paste_url_from_browser>"` (paste any file URL; script derives the base).

See `content/script-invocation.md` for script usage; `content/rag-retrieval.md` for semantic search flow.

## Build

```bash
cd skills/abd-context-to-memory
python scripts/build.py
```
