---
name: abd-search-memory
description: >-
  Semantic search over a local FAISS vector index built from document chunks.
  Use when the user says "use memory", "search memory", "what does memory say",
  "from our content", "what do we have on [topic]", or asks about content that
  has been ingested into agent memory.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Search Memory

Run **semantic search** against a FAISS index and inject the best-matching chunks into the conversation. Matches by **meaning**, not only keywords.

## How to search

```bash
python scripts/search_memory.py "<query>" --rag <source>/memory/rag --k 5
```

- `--rag`: Path to the `rag/` folder (default: `<ROOT>/memory/rag`)
- `--k`: Number of results (default 5)
- `--format`: `text` (default) or `json`

## Agent flow

1. **Derive query** — Extract a semantic query from the user's question
2. **Run search** — Execute `search_memory.py` with the query against the corpus index
3. **Inject results** — Use the returned chunks in your response
4. **Cite sources** — Include path and slide/section when using retrieved content. If chunks have front matter, note `evidence_type` / `chunk_type` to signal weight

## Active memory for this conversation

When the user points at a corpus — by naming a topic folder, having **`CONTENT_MEMORY_ROOT`** in **`conf/.secrets`**, passing `--rag`, or saying "use this memory" — **treat that `memory/rag/` as the active retrieval source for the rest of this conversation.** For later questions, run semantic search against that same index by default until the user explicitly changes or clears it (e.g. "use a different memory folder", "stop using that corpus"). Do not make them repeat the path on every turn. **Workspace policy:** **[AGENTS.md](../../../AGENTS.md)**.

## Chunk front matter (when spec was active during chunking)

Results may include chunks with YAML front matter. Use the labels to calibrate your response:

| `chunk_type` | How to use |
|---|---|
| Normative roles (e.g. `stat_block`, rules-like sections) | Cite carefully — check against source |
| Illustration / example scenes | Use as illustration unless corroborated |
| `toc_or_index`, `noise_or_art`, navigation-like | Low weight |

## Configuration

- **`OPENAI_API_KEY`** must be set (for query embedding)
- Index must exist: run embedding first (see [abd-embed-vectors](../abd-embed-vectors/SKILL.md))
- Dependencies: `pip install -r requirements-rag.txt`

## Gotchas

- If `--rag` is omitted, search uses `<ROOT>/memory/rag` where `ROOT` comes from **`CONTENT_MEMORY_ROOT`** (usually set in **`conf/.secrets`**) or **cwd**.
- Search requires the same embedding model used to build the index.
- An empty or missing index returns no results — run the embed skill first.
