# Output structure

After `index_memory.py --path <source>`:

```
<source>/                       ← topic root (--path or CONTENT_MEMORY_ROOT in conf/.secrets; see AGENTS.md)
  scripts/                       ← optional: corpus-only preprocess (see below)
    prepare_*.py, README.md
  markdown/
    .../<file>.md              ← converted from originals
    structural_scan_report.txt ← structural scan (assess converted markdown; same text as console)
    structural_scan_report.md
  archive/                       ← optional: backups (e.g. pre-normalization .md)
  memory/                        ← chunks + chunking spec (not structural scan)
    context_chunking_spec.yaml   ← chunking rules + taxonomy (draft after structure looks OK)
    .../<file>__slide_01.md      ← chunks (front matter when spec active)
    .../<file>__section_00.md
    rag/
      index.faiss
      metadata.json
```

**Legacy:** older runs may have `context_chunking_spec.yaml` under `markdown/` or at `<source>/` (topic root). The chunker checks **`memory/`** first, then those paths.

## Corpus `scripts/` (topic root)

Optional **`scripts/`** under `<source>/` holds **corpus-only** preprocess (normalize Markdown so chunking can split). Not the shared tools in `skills/abd-context-to-memory/scripts/`. **Full convention** (why, naming, docs, `archive/`, `chunk_inputs`) → [../process.md](../process.md) → subsection *Corpus preprocess scripts (`<topic_root>/scripts/`)*.

## Chunk naming

- PowerPoint: `<stem>__slide_01.md`, `__slide_02.md`, …
- Prose: `<stem>__section_00.md`, `__section_01.md`, …
- Short file (one chunk): `<stem>.md`

## Chunk content (without spec)

Each chunk includes `<!-- Source: path -->` for traceability.

## Chunk content (with spec)

Each chunk has YAML front matter:

```yaml
---
chunk_id: <stem>__section_00
source:
  canonical_path: <relative path to source md>
evidence_type: mixed
chunk_type: prose_block
section_path: ["Chapter 3", "Powers"]
---

<chunk body text>
```

`evidence_type` and `chunk_type` come from `context_chunking_spec.yaml → defaults` until you relabel per chunk. Legacy key `modeling_kind` in old specs maps to `chunk_type` in the chunker.
