# PDF extraction: outlines, tags, and heading promotion

This doc clarifies what **MarkItDown + pdfminer** (used by `convert_to_markdown.py`) does *not* give you, and how **outline/tag-based structure** and **heading heuristics** relate to `pdf_markdown_post.py`.

## What the default pipeline produces

- **Linear text** in reading order, with typical PDF noise (repeated margin titles, page numbers, duplicate ALL-CAPS strips).
- **`pdf_markdown_post`** (after MarkItDown) runs, in order:
  1. **Banner collapse** — consecutive duplicate ALL-CAPS margin strips.
  2. **Dotted-leader promotion** — lines like `Section name ........ 123` (TOC/body stubs—not a markdown table) → `### Section name 123` so page refs stay on the heading. Skips lines that will become `##` in the next step (`CHAPTER n…`, `APPENDIX …`, `PART …`). Disable: `PDF_SKIP_DOTTED_LEADER_HEADINGS=1`.
  3. **Regex heading promotion** (shared, conservative) — lines matching `CHAPTER n…`, `APPENDIX …`, `PART ONE|…|roman|digit` → `##` / `###`, with dot leaders before the page number stripped to a trailing page (e.g. `## CHAPTER 4: SKILLS 113`). Disable: `PDF_SKIP_REGEX_HEADINGS=1`.
  4. **Outline alignment** — if **`pip install pymupdf`** is available and the PDF has bookmarks, TOC titles are matched to lines (page segments when `\f` breaks align with page count, else global search). Lines already marked with `#` are left alone. Disable: `PDF_SKIP_OUTLINE_HEADINGS=1`.

That is still **not** a guarantee that every table-of-contents entry becomes a heading—only where the extract text matches the outline title and heuristics apply.

## True PDF outline / tagged structure → markdown headings

**Outline (bookmarks):** Many PDFs expose a **bookmark tree** (`/Outlines`) with titles and **destination page numbers** (or similar). That is **documented structure** from the authoring tool or print pipeline—not inferred from glyph positions.

**Tagged PDF:** PDF/UA or structure trees can associate content with **structure types** (e.g. `H1`, `P`). Few arbitrary “print to PDF” books expose this cleanly; extraction stacks vary.

**Why a separate pass:** MarkItDown’s PDF path does not expose outline/tags as markdown headings. To turn outlines/tags into `#` lines you typically:

1. Open the PDF with a library that reads **outline** or **structure**, e.g. **PyMuPDF (`fitz`)**, **pypdf**, or **pdfminer.six** at a lower level than MarkItDown.
2. Decide how to **align** outline entries to **chunks of text** in the extracted markdown (page boundaries, search for title strings, or insert headings by page range—each has tradeoffs).
3. Run that as a **post-pass** on the `.md` (or merge during extraction), optionally **behind a flag** or **corpus config** so generic conversions stay unchanged.

**Implemented in this skill** (`skills/abd-context-to-memory/scripts/`): `pdf_outline_headings.py` + optional PyMuPDF. For a **single** book that needs custom rules, add a **corpus script** under `<topic>/scripts/` instead of hardcoding in core modules.

## Heading-promotion heuristics (shared vs corpus-specific)

The **shared** stage in `pdf_markdown_post.promote_regex_section_headings` handles a few high-signal patterns (`CHAPTER n`, `APPENDIX`, `PART …`) and skips lines that are already headings. **Banner collapse** stays separate (format noise, not semantic promotion).

**Heading promotion** more broadly means: turn **plain lines** in the extract into markdown headings, e.g. ALL-CAPS one-line section titles → `### …` when not a margin banner—those extra rules are **heuristic** and often **corpus-specific**.

So:

| Approach | Where it lives |
|----------|----------------|
| **Shared, conservative** | `promote_regex_section_headings` in `pdf_markdown_post.py` (env to skip); outline pass in `pdf_outline_headings.py`. |
| **Corpus-specific** | `<topic>/scripts/prepare_*.py` or YAML-driven rules keyed to one publisher/layout—**not** hardcoded in the core skill. |

**Chunking without `#` headings:** Even without promotion, `draft_chunking_spec.py` can use **regex section boundaries** (`chapter_break_regex`, etc.) so `chunk_markdown.py` still splits on structure—headings in markdown are ideal for RAG, not strictly required for boundaries.

## Summary

- **Outline/tags → `#` headings** = PyMuPDF + `pdf_outline_headings.py` when installed; otherwise skipped.
- **Banner collapse** = format noise; **regex promotion** = shared content heuristics; **corpus-specific** rules stay in topic scripts.
