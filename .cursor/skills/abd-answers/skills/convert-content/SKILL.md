---
name: convert-content
description: >-
  Convert source files (PDF, DOCX, PPTX, etc.) under data/assets to mirrored
  markdown in the pipeline. Use when new content is added, files change, or
  the user asks to refresh the markdown layer.
---
# convert-content

## Purpose

Stage 1 of the abd-answers memory pipeline: convert source files to markdown
under `abd-answers-memory-pipeline/markdown/`.

## Commands (run from the agent root: agents/abd-answers/)

**Full convert:**

```bash
python skills/convert-content/scripts/convert_to_markdown.py --memory "<path-under-data/assets>"
```

`--memory` path is relative to `data/assets/` (no `data/assets/` prefix).

**Incremental (skip up-to-date):**

```bash
python skills/convert-content/scripts/convert_to_markdown.py --memory "<path>" --update
```

**Force re-convert:**

```bash
python skills/convert-content/scripts/convert_to_markdown.py --memory "<path>" --update --force
```

**With logging:**

```bash
python -u skills/convert-content/scripts/convert_to_markdown.py --memory "<path>" --update --log-file data/pipeline-convert.log
```

## PDF post-processing

After MarkItDown extraction, `pdf_markdown_post.postprocess_pdf_markdown`
runs automatically: banner collapse, regex heading promotion, and optional
PDF-outline alignment via `pdf_outline_headings` (requires `pip install pymupdf`).

Env overrides: `PDF_SKIP_REGEX_HEADINGS`, `PDF_SKIP_OUTLINE_HEADINGS`.

## Paths

- Config: `skills/convert-content/scripts/_config.py` — `PIPELINE_MARKDOWN`
- Shared paths: `scripts/shared/abd-answers-paths.ts`
- Contract: `skills/convert-content/scripts/PIPELINE_CONTRACT.md`
