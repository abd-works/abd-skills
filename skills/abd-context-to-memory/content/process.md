# Pipeline Process

## What this skill actually does

You point it at a folder of documents. It:

1. Turns each supported original into **markdown** under a **`markdown/`** folder at the **topic root**, parallel to **`memory/`** (e.g. `slides/deck.pptx` → `markdown/slides/deck.md`). Sibling `.md` you already have is left as-is.
2. Splits markdown into **small chunk files**: for each logical document it uses **`markdown/…/<stem>.md` if present**, then legacy **`…/markdown/<stem>.md`**, otherwise the sibling `<stem>.md`, never both. Chunks land under **`memory/`** with the same folder layout **but without** a `markdown` segment in the path.
3. Optionally builds a **search index** (RAG) so `search_memory.py` can find relevant chunks.

Everything below is just **where those folders live** and **whether you use one big command or several**. Same Python scripts either way.

---

## Example: normal topic folder (the usual case)

Say your originals live here:

```text
D:/content/Training_2025/
  slides/
    onboarding.pptx
  policies/
    remote-work.pdf
```

You run from your workspace root (where the skill expects to run):

```bash
python skills/abd-context-to-memory/scripts/index_memory.py --path "D:/content/Training_2025"
```

**After convert:** markdown lives under **`markdown/`** next to **`memory/`** (same relative paths as originals, without interleaving):

```text
D:/content/Training_2025/
  slides/
    onboarding.pptx
  policies/
    remote-work.pdf
  markdown/
    slides/
      onboarding.md          ← new
    policies/
      remote-work.md         ← new
```

**After chunk:** chunks mirror the topic tree **without** `markdown` in the path (input was `markdown/slides/onboarding.md` → output under `memory/slides/`):

```text
D:/content/Training_2025/
  memory/
    slides/
      onboarding__slide_01.md   ← pattern: <original_stem>__<slide_NN or section_NN>.md
      onboarding__slide_02.md
      ...
    policies/
      remote-work__section_00.md
      ...
    chunk_index.json       ← list of chunk ids / paths (for tools like story-synthesizer)
    rag/                   ← vector index for semantic search (after embed step)
```

Nothing writes to a generic path like `context-to-memory/memory/` on your machine—the **topic folder** owns `memory/`. The scripts never treat `memory/` as input, so you do not get chunks-of-chunks.

---

## Example: one command vs. piece by piece

**One shot (typical):**

```bash
python skills/abd-context-to-memory/scripts/index_memory.py --path "D:/content/Training_2025"
```

That runs, in order: convert → chunk → `chunk_index.json` → fix SharePoint-style links in chunks → **embeddings/RAG only if you pass `--embed`** (default is no embed; use **`embed_and_index.py`** on the hub for a shared index). If your workspace uses a **hub** (see below), it also drops a **junction** so the hub can see this topic’s `memory/` without copying files.

**Markdown already in place (skip convert):** add `--skip-convert` so the pipeline starts at chunking. Use when you already have **`markdown/…/<stem>.md` and/or sibling `<stem>.md`** (the chunker picks one per stem). Example:  
`python skills/abd-context-to-memory/scripts/index_memory.py --path "D:/content/Training_2025" --skip-convert`

**By hand (same end state, for debugging):**

```bash
# cwd should be the topic root, or set CONTENT_MEMORY_ROOT to it
python skills/abd-context-to-memory/scripts/convert_to_markdown.py --memory "D:/content/Training_2025"
python skills/abd-context-to-memory/scripts/chunk_markdown.py --path "D:/content/Training_2025" --output "D:/content/Training_2025/memory"
python skills/abd-context-to-memory/scripts/sync_sharepoint_urls.py
python skills/abd-context-to-memory/scripts/embed_and_index.py
```

(Exact flags for embed depend on whether you are indexing one topic or a whole hub; use **`index_memory --embed`** for per-topic, or **`embed_and_index.py`** on the hub for aggregate.)

---

## Special case: the folder is literally named `context`

Some projects keep sources in a folder called `context`:

```text
C:/my-project/skill-space/context/
  notes.docx
```

If you pass **that** path to `--path`, converted markdown and chunks are stored **next to the project**, not inside `context/`:

```text
C:/my-project/
  markdown/
    notes.md              ← from context/notes.docx
  memory/context/
    notes__section_00.md
    ...
```

So the “project root” holds parallel **`markdown/`** and **`memory/`**, and RAG/chunks still have a stable home. If your folder is **not** named `context`, chunks stay at **`<that folder>/memory/`** as in the Training_2025 example.

---

## “Hub” layout (shortcut + shared search)—with an example

Many teams keep a central folder (call it the **hub**), e.g. `C:/work/abd_content`. They add a small JSON config (often `conf/content_memory_roots.json`) that says: “this directory is the hub,” “put the big shared search index here,” and “put topic shortcuts under `assets/`” (the name `assets` is configurable).

After you index a topic, the script can create a **junction** (Windows) or **symlink** (Mac/Linux) so the hub shows the topic without duplicating data:

```text
C:/work/abd_content/
  assets/
    Training_2025/    ← junction → D:/content/Training_2025/memory
  conf/
    content_memory_roots.json
```

So: **real files** still live under `D:/content/Training_2025/memory/`. **`C:/work/abd_content/assets/Training_2025`** is just a door into that folder. Skip junctions with `--no-junction` or `SKIP_MEMORY_JUNCTION=1` if you do not want that link.

The **shared** vector index path is often configured separately (e.g. `rag_path` in that JSON, or env vars)—so search can live on a drive or SharePoint location even when sources are local. Details: `content/config.md`.

---

## Optional `roots/` layout (only if you asked for it)

Some workspaces want a **manifest file** that lists named roots and a fixed place for “chunked” links:

```text
C:/work/my-workspace/
  roots/
    roots.json
    proposals/
      chunked/   ← junction → wherever the real memory folder is
```

You build that with `scripts/add_root.py` and `scripts/link_chunked.py`. **`index_memory` does not maintain `roots/` for you.** Use this when you explicitly want that registry; otherwise ignore `roots/` and use the topic `memory/` + hub junction pattern above.

---

## Chunking rules (what the splits look like)

- **PowerPoint-style decks:** converter adds `<!-- Slide number: N -->` markers; chunker makes **one file per slide**.
- **Long prose** (over ~200 lines): split at lines that start with `#` or `##`.
- **Short files:** one chunk.

Real names look like `onboarding__slide_01.md` or `remote-work__section_00.md`. A short doc that stays one chunk may be just `readme.md` (no `__` suffix).

---

## Supported input formats

`.pdf`, `.pptx`, `.docx`, `.xlsx`, `.xls`, `.html`, `.htm`, `.txt`, `.csv`, `.json`, `.xml`

---

## When something fails

- Wrong or missing path → convert/chunk exits with errors.
- Unsupported file type → that file is skipped or errors; others may still run.
- RAG/embed → needs API key and `requirements-rag.txt` deps; see `SKILL.md`.
