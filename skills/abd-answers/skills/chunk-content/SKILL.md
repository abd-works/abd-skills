---
name: chunk-content
description: >-
  Chunk pipeline markdown into smaller files for embedding. Use after
  convert-content has run, when chunks need refreshing, or when the chunking
  spec changes.
---
# chunk-content

## Purpose

Stage 2 of the abd-answers memory pipeline: split converted markdown into
chunk files under `abd-answers-memory-pipeline/chunked/`.

## Commands (run from the agent root: agents/abd-answers/)

**Full chunk:**

```bash
python skills/chunk-content/scripts/chunk_markdown.py --path "<path-under-data/assets>"
```

**Incremental (skip unchanged):**

```bash
python skills/chunk-content/scripts/chunk_markdown.py --path "<path>" --update
```

**Force re-chunk:**

```bash
python skills/chunk-content/scripts/chunk_markdown.py --path "<path>" --update --force
```

**With logging:**

```bash
python -u skills/chunk-content/scripts/chunk_markdown.py --path "<path>" --update --log-file data/pipeline-chunk.log
```

## Incremental behavior

With `--update`, skips re-chunking when each chunk output is newer than its
pipeline markdown source.

## Paths

- Input: `abd-answers-memory-pipeline/markdown/`
- Output: `abd-answers-memory-pipeline/chunked/`
- Config: `skills/chunk-content/scripts/_config.py` — `PIPELINE_CHUNKED`
- Contract: `skills/convert-content/scripts/PIPELINE_CONTRACT.md`
