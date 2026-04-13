---
name: abd-embed-vectors
description: >-
  Embed text chunks into a local FAISS vector index for semantic search.
  Use when the user wants to "embed chunks", "build a vector index",
  "create embeddings", or prepare chunked content for RAG retrieval.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Embed Vectors

Turn chunked markdown into **vectors** and store them in a **local FAISS index** so semantic search can return the right passages for a question — not only keyword matches.

## How to embed

### From existing chunks

```bash
python scripts/embed_and_index.py --path <source_folder>/memory
```

### Rebuild index from scratch

```bash
python scripts/embed_and_index.py --path <source_folder>/memory --replace
```

The FAISS index is written to `<source_folder>/memory/rag/` — next to the chunks, not inside the skill directory.

## Output layout

```
<source>/memory/rag/
  index.faiss       # vector index
  metadata.json     # chunk paths and metadata
```

## Configuration

### Required

Set `OPENAI_API_KEY` for the embedding model. Place it in any of:

- `<repo>/conf/.secrets`
- `<repo>/conf/.env`
- `<skill_root>/.env`
- `cwd/.env`

The config module loads it automatically.

### Topic folder

Set **`CONTENT_MEMORY_ROOT`**, pass **`--path`**, or **`cd`** to the corpus folder. When `--path` is omitted, embed uses `<ROOT>/memory` by default.

## Dependencies

```bash
pip install -r requirements-rag.txt
```

Requires `openai`, `faiss-cpu`, and related packages.

## Gotchas

- Embedding requires an API key and network access — it calls the OpenAI embedding endpoint.
- The index is written next to the corpus (`<source>/memory/rag/`), not inside the skill package.
- If chunks change, rebuild the index with `--replace` to avoid stale vectors.
- Each run embeds all chunks in the `memory/` folder; use `chunk_inputs` in the chunking spec (see [abd-chunk-markdown](../abd-chunk-markdown/SKILL.md)) to control what gets chunked before embedding.
