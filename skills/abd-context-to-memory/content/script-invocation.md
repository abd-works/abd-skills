# Script Invocation

Run from workspace root.

**Memory root (ROOT):** With **`--path`**, ROOT is the **source folder** you pass. Chunks go to **`ROOT/memory/`** (or **`parent/memory/context/`** when the folder is named `context`). **Embedding is off by default**; use **`--embed`** or run **`embed_and_index.py`** separately. Set `CONTENT_MEMORY_ROOT` only when running `--memory` without a source.

**Dependencies**: `pip install "markitdown[all]"` (convert)

## link_workspace_source.py

Creates a junction (Windows) or symlink (Unix) so a folder is accessible under `source/`. **Run on request** when adding content to memory and the link does not yet exist.

**Usage:**
```bash
python scripts/link_workspace_source.py --path <folder_path> [--name <link_name>]
python scripts/link_workspace_source.py --workspace <workspace_folder_name> [--name <link_name>]
```

- `--path`: Any folder (absolute or relative to ROOT). Use for arbitrary folders.
- `--workspace`: Shorthand for `workspace/<name>/source` (workspace RFQ folders).
- `--name`: Link name under `source/` (default: last component of target path).

**Examples:**
```bash
python scripts/link_workspace_source.py --path "C:/docs/RFQ materials" --name "JBOM"
python scripts/link_workspace_source.py --path "workspace/Scotia Talent Journey/source" --name "JBOM Agile Support"
python scripts/link_workspace_source.py --workspace "Scotia Talent Journey Based Operating Model" --name "JBOM Agile Support"
```

**When to run:** Before `convert_to_markdown.py --memory` for a folder, if the user requests adding that content to memory and the link is not yet present.

## add_root.py

Registers a **context root** and optional **chunked** junction for multi-root workspaces. Manifest: `roots/roots.json`; each root lives under `roots/<name>/`.

**Usage:**
```bash
python scripts/add_root.py --name <name> [--memory-path <path>] [--workspace <dir>]
```

- `--name`: Folder name under `roots/` (normalized to lowercase, spaces → underscores).
- `--memory-path`: If set, creates `roots/<name>/chunked` as a junction/symlink to this folder (must exist for junction to succeed).
- `--workspace`: Workspace root (default: current directory).

**When to run:** User says "add a new root" or you need to register another content/memory pair in `roots/roots.json`.

## link_chunked.py

Creates `roots/<name>/chunked` → memory folder (where chunked markdown lives). Uses `memory_path` from `roots.json` for that root if `--memory-path` is omitted.

**Usage:**
```bash
python scripts/link_chunked.py --root <name> [--memory-path <path>] [--workspace <dir>]
```

**When to run:** User says "add something to this root" or you need to (re)link the chunked junction after `memory_path` is known.

## convert_to_markdown.py

Converts source files to markdown. Writes each `.md` under **`<topic_root>/markdown/…`** mirroring the source tree (e.g. `notes/deck.pptx` → `markdown/notes/deck.md`). If the topic folder is named `context`, output is **`../markdown/…`** next to that folder. Does not walk into existing `markdown/` or `memory/` when discovering sources.

**Single file (when user asks for one file):**
```bash
python scripts/convert_to_markdown.py --file <file_path>
```

**Folder (when user explicitly wants folder processed):**
```bash
python scripts/convert_to_markdown.py --memory <source_path>
```

- `--file`: Process ONLY the specified file. Use when user says "one file", "this file", "just X.pdf". Output: **`markdown/…`** under the topic root (see `--topic-root`). Optional **`--topic-root`** when the file is not directly under the topic folder.
- `--memory`: Process all supported files in folder. Tries under `Assets/` first, then workspace root.
- **OneDrive → SharePoint auto-injection:** When source is under a configured OneDrive path (e.g. `OneDrive - Agile by Design`), SharePoint URLs are auto-injected from `sharepoint_mapping.json`. No `--sharepoint-base` needed. Add mappings in `skills/abd-context-to-memory/sharepoint_mapping.json`.
- `--sharepoint-base <url>`: Override or use when source is not in OneDrive. Base URL to the folder (e.g. `https://.../Scotiabank/GTB`). Appends relative path and `?csf=1&web=1` (or `--sharepoint-query`).
- `--sharepoint-query <query>`: Optional. Default `csf=1&web=1`. Add `e=XXX` from a current SharePoint link if needed.

## chunk_markdown.py

Chunks markdown. For each logical document (folder + stem), prefers **`markdown/…/<stem>.md`** at the topic root, then legacy **`…/markdown/<stem>.md`**, otherwise sibling **`…/<stem>.md`**, never both. Writes chunks under **`memory/`** (or `--output`) mirroring the source tree **without** a `markdown` path segment. If **`--path`** points at a folder named **`context`**, the script scans the **parent** folder so markdown under **`../markdown/`** is included.

**Usage:**
```bash
python scripts/chunk_markdown.py --path <source_folder> [--memory <memory_name>]
```

- `--path`: Topic / source folder root
- `--memory`: Optional. Memory folder name under workspace when not using `--output` (default: last component of source path)
- Run convert first (or ensure `.md` exists). Excludes chunked output (__slide_, __section_) from input.

## sync_sharepoint_urls.py

Syncs SharePoint URLs in memory chunks. **Run after chunk** when source lines have `source/... | https://...`. Replaces source path with SharePoint URL, fixes malformed URL order (path before query), and adds `wdSlideIndex` (pptx) or `page` (pdf) for direct slide/page links.

**Usage:**
```bash
python scripts/sync_sharepoint_urls.py [--memory <memory_name>]
```

- `--memory`: Optional. Memory folder name (e.g. `JBOM`). Operates on `memory/<name>/*.md`. If omitted, processes all .md under `memory/`.
- Run after `chunk_markdown.py`

## add_sharepoint_mapping.py

Adds a OneDrive → SharePoint mapping so convert can generate shareable links. **Use when convert warns about missing mapping**, or when adding a new OneDrive root.

**Usage:**
```bash
python scripts/add_sharepoint_mapping.py --prefix "OneDrive - Org" --base "<sharepoint_url>"
python scripts/add_sharepoint_mapping.py --path <file_in_onedrive> --base "<sharepoint_url>"
```

- `--prefix`: OneDrive folder name (e.g. `OneDrive - Agile by Design`).
- `--base`: SharePoint URL. Paste the full file URL from the browser; script strips to document library base.
- `--path`: File under OneDrive; prefix is extracted automatically.
- `--query`: Optional. Default `csf=1&web=1`.

**When to run:** When convert prints "WARNING: Source is in OneDrive but no SharePoint mapping is configured."

## markdown_to_excel.py

Generic markdown → Excel. Parses headings, tables, paragraphs; writes to a new workbook.

**Dependencies**: `pip install openpyxl`

**Usage:**
```bash
python scripts/markdown_to_excel.py <input.md> [output.xlsx]
python scripts/markdown_to_excel.py --file <input.md> [--out <output.xlsx>]
```

**When to run:** When user wants to export markdown to Excel. For project-specific formats (e.g. JBOM B&T template), use workspace scripts.

## markdown_to_docx.py

Generic markdown → Word. Uses pypandoc.

**Dependencies**: `pip install pypandoc`. Requires pandoc binary: https://pandoc.org/installing.html

**Usage:**
```bash
python scripts/markdown_to_docx.py <input.md> [output.docx]
python scripts/markdown_to_docx.py --file <input.md> [--out <output.docx>]
```

## markdown_to_pdf.py

Generic markdown → PDF. Uses pypandoc.

**Dependencies**: `pip install pypandoc`. Requires pandoc + a PDF engine (pdflatex, weasyprint, or wkhtmltopdf).

**Usage:**
```bash
python scripts/markdown_to_pdf.py <input.md> [output.pdf]
python scripts/markdown_to_pdf.py --file <input.md> --pdf-engine weasyprint
```

If pdflatex is not installed: `pip install weasyprint` then use `--pdf-engine weasyprint`.

## index_memory.py

Default pipeline: convert → chunk → sync SharePoint (**no embed**). Pass **`--embed`** to also build/update per-topic vector index under that topic’s `memory/rag/`. For a **shared** hub index, run **`embed_and_index.py`** separately (no `--memory`).

**Dependencies**: `pip install -r skills/abd-context-to-memory/requirements-rag.txt` (OpenAI API key for embeddings)

**API key**: Prefer `agilebydesign-skills/conf/.secrets` or `conf/.env` (same `KEY=value` format as dotenv)—loaded automatically by `scripts/_config.py`. Optionally set `OPENAI_API_KEY` in the project `.env` (cwd; overrides repo conf) or in the environment.

**Usage:**
```bash
python scripts/index_memory.py --path <source_folder>
python scripts/index_memory.py --path <source_folder> --embed   # also per-topic FAISS under memory/rag/
python scripts/index_memory.py --path <source_folder> --skip-convert   # .md already beside sources; skip markitdown
python scripts/index_memory.py --path <source_folder> --memory-root <hub_root>
python scripts/index_memory.py --path <source_folder> --junction-workspace <hub_root>
python scripts/index_memory.py --path <source_folder> --no-junction
python scripts/index_memory.py --memory <memory_name>
python scripts/index_memory.py
python scripts/index_memory.py --replace
```

- `--path`: Source folder (e.g. `source/JBOM` or `Assets/04 Service Offering`). Default: convert → chunk → sync SharePoint. Add **`--embed`** for per-topic FAISS under `memory/rag/`.
- `--embed`: Opt in to **`embed_and_index.py`** after sync (per-topic index). Omitted by default.
- **Hub junction (after successful `--path`):** **`hub/<source_folder_name>` → absolute path to that source’s memory folder** (usually `<source>/memory`, or `<parent>/memory/context` when `--path` ends in `context`). `--memory-root` and `--junction-workspace` are aliases for the hub directory. Order: explicit flag, else `ABD_CONTENT_ROOT`, else cwd. Skip with `--no-junction` or `SKIP_MEMORY_JUNCTION=1`.
- `--memory`: Memory folder name (chunk + sync; **embed only with `--embed`**; convert already ran). Does **not** create a workspace junction (use `--path` for full ingest + junction).
- **No args:** When `skill_space_path` is set (in `skill-config.json` or `abd-story-synthesizer/conf/abd-config.json`), automatically runs on `{skill_space_path}/context`. Use when the user says "add to memory" or "refresh memory" without specifying a folder. Junction creation applies when this default `--path` flow completes successfully.
- `--replace`: Rebuild entire vector index from all memory (drops existing index).

**Memory root:** For **`--path "<source>"`**, normal flow uses **`source/memory/`** for chunks. Exception: **`--path` …/ `context`** uses **`parent`** as project root, chunks at **`memory/context/`**. Per-topic embed uses **`embed_and_index`** only when **`--embed`** is set.

**When to run:** After adding or updating content. For **semantic search**, build an index with **`embed_and_index.py`** (aggregate hub) or **`--embed`** (per-topic).

## embed_and_index.py

Builds/updates the FAISS + embeddings index (relative to `CONTENT_MEMORY_ROOT` / cwd).

- **`--memory <name>`:** Index chunks under **`memory/<name>/`** only. Writes index to **`memory/rag/`** (per-topic / project tree).
- **No `--memory`:** Indexes **(1)** every **subfolder** of **`assets/`** except reserved **`rag/`** when it sits under `assets/` (each other entry should be a junction to a topic `memory` tree — hub layout for **abd_content**, RPG content, etc.); chunk paths in metadata are prefixed with the folder name; **(2)** plus any **`memory/**/*.md`** (legacy). Produces **one** combined index; **default output** is **`assets/rag/`**, or a **configurable** aggregate folder (`CONTENT_MEMORY_RAG_PATH`, `content_memory_rag_path` in `skill-config.json`, or `rag_path` per hub in `conf/content_memory_roots.json`) so the vector store can live on OneDrive/SharePoint.
- **`--replace`:** Rebuild the index from scratch (use after adding `assets/` junctions or bulk chunk changes).

**Hub example (`abd_content`):** `cd` to `abd_content`, set `CONTENT_MEMORY_ROOT` to that folder, then `python scripts/embed_and_index.py --replace`.

## search_memory.py

Semantic search over indexed chunks. Returns top-k matches with source paths.

**Usage:**
```bash
python scripts/search_memory.py "<query>" [--k 5] [--format text|json]
```

- `"<query>"`: Semantic query (topic, concept, question).
- `--k`: Number of chunks to return (default: 5).
- `--format`: `text` (default) or `json`.

**When to run:** When user says "use memory", "search memory", "what does memory say about X", "from our content", "from ABD materials", or asks about Agile/training/proposals/ABD materials. Run from workspace root; inject results into response; cite sources.

See `content/rag-retrieval.md` for trigger phrases and agent flow.

## SharePoint Link Creation (OneDrive)

When content is in OneDrive, local file paths are not shareable. **If you run convert with OneDrive content but no mapping, you'll get a warning with instructions.**

### Add a mapping (when warned or for new OneDrive roots)

1. Open any file from the OneDrive folder in SharePoint/OneDrive web.
2. Copy the URL from the browser address bar.
3. Run:

```bash
python scripts/add_sharepoint_mapping.py --prefix "OneDrive - Agile by Design" --base "<paste_url_here>"
```

Or with a file path (prefix is auto-detected):

```bash
python scripts/add_sharepoint_mapping.py --path "C:/Users/.../OneDrive - Org/Shared Documents/file.pptx" --base "<paste_url_here>"
```

The script derives the base URL from a full file URL, so you can paste the URL as-is.

### Manual config

Edit `sharepoint_mapping.json` in the skill root and add entries to the `mappings` array:

```json
{
  "mappings": [
    {
      "onedrive_prefix": "OneDrive - Agile by Design",
      "sharepoint_base": "https://...sharepoint.com/:f:/r/sites/SiteName/Shared%20Documents",
      "sharepoint_query": "csf=1&web=1"
    }
  ]
}
```

Convert will auto-inject SharePoint URLs for any file under the configured OneDrive prefix. `sync_sharepoint_urls.py` (run automatically in `index_memory --path`) then adds `wdSlideIndex` (pptx) and `page` (pdf) for direct slide/page links.

## Layout

- **Converted markdown**: Written to **`<parent>/markdown/`** per source file
- **Chunked content**: Written under **memory/** (or `--output`), same relative layout as sources **minus** any `markdown` directory in the path. Sync and embed operate on these files.

## Key Behaviors

1. **Run convert before chunk** — Convert writes `.md` under topic-level `markdown/`; chunk dedupes sibling vs `markdown/` and writes chunks to `memory/` without a `markdown` segment in paths.
2. **SharePoint URLs** — When source is in OneDrive, convert auto-injects SharePoint URLs from `sharepoint_mapping.json`. `sync_sharepoint_urls` (in pipeline) makes links shareable and adds slide/page params.
3. **Handle errors gracefully** — Some files may fail. Log and continue.
4. **Long-running** — Large folders (100+ files) take time.
5. **RAG**: Run `index_memory` after adding content; run `search_memory` when user asks for memory retrieval.
