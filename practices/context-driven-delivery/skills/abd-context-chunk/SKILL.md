---
name: abd-context-chunk
description: >-
  Split converted Markdown into retrieval-sized chunks with evidence labels,
  guided by a structure-based chunking spec. Use when the user wants to
  "chunk documents", "split for RAG", "draft a chunking strategy", or
  prepare markdown for embedding and semantic search.
context-fidelity:
  - level: context
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Chunk Markdown

Split large Markdown files into **retrieval-sized chunks** with **evidence labels** so each piece is a coherent unit for search and prompting.

## Two-step process

### 1. Draft a chunking spec

Analyze converted markdown structure and produce `memory/context_chunking_spec.yaml` — the strategy for where to cut, how big chunks should be, and what labels to apply.

```bash
python scripts/draft_chunking_spec.py --path <source_folder>
```

This writes:
- `markdown/structural_scan_report.txt` — heading/table metrics for the converted markdown
- `memory/context_chunking_spec.yaml` — draft chunking rules (skipped if spec already exists; use `--force` to overwrite)

### 2. Chunk the markdown

```bash
python scripts/chunk_markdown.py --path <source_folder> --output <source_folder>/memory
```

Cuts markdown into files under `memory/`. When a spec exists, chunks get YAML front matter with `chunk_id`, `evidence_type`, `chunk_type`, and `section_path`.

## Strategy pass vs straight-through

If the user does not mention strategy, **ask once**: **strategy pass** (review/edit the YAML before chunking) vs **straight through** (chunk immediately with the draft spec). Do not assume straight-through.

**Strategy pass workflow:**
1. Run `draft_chunking_spec.py` to get the draft
2. Review and edit `memory/context_chunking_spec.yaml` (especially taxonomy and boundaries)
3. Then chunk: `chunk_markdown.py --path <source_folder>`

## Chunking spec shape

```yaml
chunk_inputs: ["markdown/PrimarySource.md"]  # optional: restrict which files to chunk

section_boundaries:
  chapter_break_regex: "^CHAPTER\\s+\\d+"
  section_break_regex: "^##\\s+"
  all_caps_standalone: true

splitting:
  min_chunk_chars: 400
  max_chunk_chars: 8000
  keep_markdown_tables_intact: true
  split_on_heading_level: 2

defaults:
  evidence_type: mixed
  chunk_type: prose_block

taxonomy:
  evidence_type: []   # fill from actual corpus
  chunk_type: []      # fill from actual corpus
```

For full spec detail, see [references/chunking-spec.md](references/chunking-spec.md).

## Quality loop (agent obligation)

After chunking, **check** how many chunks were written and whether splits match the document. If results are wrong (e.g. one giant chunk, absurd split counts):

1. Edit the spec (regexes, `split_on_heading_level`, `chunk_inputs`)
2. Optionally preprocess markdown (inject headings, dedupe running headers)
3. Re-run `chunk_markdown.py`
4. Re-verify

Repeat until boundaries and sizes look right. Do not tell the user "fix the spec yourself" as the first response.

## Chunk naming

- PowerPoint: `<stem>__slide_01.md`, `__slide_02.md`, ...
- Prose: `<stem>__section_00.md`, `__section_01.md`, ...
- Short file (one chunk): `<stem>.md`

## evidence_type vs chunk_type

| Axis | Question | Examples |
|------|----------|----------|
| `evidence_type` | What does this chunk look like as text? (form) | `prose`, `table`, `list`, `mixed`, `metadata_noise` |
| `chunk_type` | What role or structure in this manuscript? | Corpus-specific: `chapter`, `stat_block`, `powers`, `toc_or_index` |

## Topic folder

**Workspace:** **[AGENTS.md](../../../AGENTS.md)** (*Workspace (topic root) — config first*). Set **`CONTENT_MEMORY_ROOT=`** in **`conf/.secrets`**, pass **`--path`**, or **`cd`** to the corpus folder. Chunks go to `<source>/memory/`. The spec lives at `<source>/memory/context_chunking_spec.yaml`.

## Gotchas

- `draft_chunking_spec.py` leaves `taxonomy` lists empty by design — fill them after reading the source.
- The chunker only cuts along boundaries the markdown and spec already expose; it does not rebuild hierarchy from a wall of text. Fix structure in conversion (see [abd-convert-to-markdown](../abd-convert-to-markdown/SKILL.md)).
- `chunk_inputs` limits which `.md` files are chunked — use it when the folder has backups or duplicates.
