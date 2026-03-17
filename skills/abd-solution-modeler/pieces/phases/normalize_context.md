# Phase 1 — Normalize Context

**Actor:** Code

## Purpose

Prepare raw materials for reasoning. Load chunks from `chunk_index` or `context_path`, apply noise filters, and write normalized output.

## Trigger

normalize context, chunk context, prepare context, convert context to memory

## Inputs

- `chunk_index_path` or `context_path` from `solution.conf`

## Instructions

- Load chunks from chunk_index.json or scan context_path for .md files
- Assign stable IDs (hash of path + content prefix)
- Preserve source location
- Apply default noise filters (TOC, section headers, page numbers, short header-only chunks)
- Do not interpret text
- Write filtered chunks to output

## Noise Filtering

Default filters remove:

- Table of contents, appendix, index, license
- TOC-style lines (e.g. `CHAPTER 8: TITLE ......... 235`)
- Page numbers only
- Very short header-only chunks
- Chunks that are mostly repeated headers (e.g. same chapter title 3+ times)

Use `--no-filter` to skip filtering (for debugging).

**Note:** The script may apply additional workspace filters from `concept_guidance.json` when re-running after Phase 4 (Concept synthesis). On first run, that file does not exist; only default filters apply.

## Outputs

- `context/context_chunks.json` — filtered chunks as a single JSON array
- `context/<chunk_id>.md` — one file per chunk for direct context access

## Run

```bash
python scripts/pipeline.py run normalize_context
```

Script: `scripts/normalize_context.py`
