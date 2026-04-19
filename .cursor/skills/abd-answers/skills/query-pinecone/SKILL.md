---
name: query-pinecone
description: >-
  Search abd-answers Pinecone index and return grounded context. Use when
  the user activates abd-answers for chat, asks questions about content hub
  topics, or requests RAG-backed answers.
---
# query-pinecone

## Purpose

Query the abd-answers Pinecone vector index and return relevant chunks for
grounding agent responses.

## Chat activation

When the user says **"Use abd-answers for this chat"** (or equivalent):

1. Treat substantive questions in the thread as requiring Pinecone-backed
   context about the content hub.
2. Before answering, run retrieval with the user's question (or a derived
   search query).
3. Cite chunk titles / `sourceUrl` from results when grounding answers.

## Commands (run from the agent root: agents/abd-answers/)

**Basic query:**

```bash
npm run rag:query -- "your search question" --k 8
```

**With folder scope:**

```bash
npm run rag:query -- "your search question" --folders "folder/a,folder/b"
```

**With memory root ID:**

```bash
npm run rag:query -- "your question" --memory-root-id "<memoryRootId>"
```

Optional: `--rag-ref pinecone://<index>/<namespace>` when defaults are wrong.

## Path filters (conversation scope)

- **Set filter:** User says "only use path1, path2" or "scope to folder X" —
  treat as memory folder roots (forward slashes, relative to content hub),
  OR'd together. Pass as `--folders`.
- **Clear filter:** User says "clear abd-answers path filter" or "search
  everything" — stop passing `--folders`.
- **Remember** the active filter for the current chat session only.

## Using results

Parse JSON stdout. Use `chunks[].bodyPreview` for grounding; expand with
file reads only when needed. Cite `sourceUrl` or chunk title.

## Code references

- Script: `skills/query-pinecone/scripts/agent-pinecone-query.ts`
- Search impl: `scripts/shared/rag/pinecone-rag.ts` (`memoryScopeFolders`)
- Secrets: `conf/.secrets` — `PINECONE_API_KEY`, `PINECONE_INDEX`, OpenAI keys
