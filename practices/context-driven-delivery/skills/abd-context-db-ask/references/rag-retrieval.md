# RAG Semantic Retrieval

Build the FAISS index on **your machine**, next to your source tree (see [config.md](config.md)). Point `--rag` at that folder when searching—there is no default index path inside this skill repo.

When the user asks about content in memory, run semantic search and inject results.

## Trigger Phrases

Run `search_memory "<query>"` when the user says:

- "use memory", "search memory", "what does memory say"
- "from our content", "from ABD materials", "from our decks"
- "what do we have on [topic]"
- Asks about Agile, training, proposals, service offerings, or any ingested materials

## Agent Flow

1. **Derive query** — Extract a semantic query from the user's question.
2. **Run search** — From a shell where paths resolve (topic folder, or **`CONTENT_MEMORY_ROOT`** in **`conf/.secrets`** — see [AGENTS.md](../../../AGENTS.md)):
   ```bash
   python skills/abd-context-to-memory/abd-search-memory/scripts/search_memory.py "<query>" --rag <source>/memory/rag --k 5
   ```
3. **Inject results** — Use the returned chunks in your response.
4. **Cite sources** — Include path and slide/section when using retrieved content. If chunks have front matter, also note `evidence_type` / `chunk_type` to signal how much weight to give the result.

## Requirements

- RAG deps: `pip install -r agents/abd-context-to-memory/requirements-rag.txt` (from repo root; adjust if your checkout layout differs)
- `OPENAI_API_KEY` set
- Index exists: run `index_memory.py --path <source>` first

## Output Layout

```
<source>/memory/rag/
  index.faiss
  metadata.json
```

## Chunk front matter (when spec was active during chunking)

Results may include chunks with YAML front matter. Use the labels to calibrate your response:

| `chunk_type` (corpus-specific) | How to use |
|----------------|-----------|
| Normative roles (e.g. `stat_block`, `powers`, rules-like sections) | Cite carefully — check against source |
| Illustration / example scenes | Use as illustration unless corroborated |
| `toc_or_index`, `noise_or_art`, navigation-like | Low weight |
