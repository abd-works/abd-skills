# AGENTS — abd-answers

## Purpose

Orchestrate the abd-answers **convert → chunk → embed → query** pipeline.
Detect when content changes under `data/assets/`, route to the right stage,
and suggest Pinecone-backed RAG when it would help the user's chat.

---

## Skills (route by stage)

| Skill | Stage | SKILL.md |
|-------|-------|----------|
| Convert | 1 — Source files → markdown | [skills/convert-content/SKILL.md](skills/convert-content/SKILL.md) |
| Chunk | 2 — Markdown → chunk files | [skills/chunk-content/SKILL.md](skills/chunk-content/SKILL.md) |
| Embed | 3 — Chunks → Pinecone vectors | [skills/embed-pinecone/SKILL.md](skills/embed-pinecone/SKILL.md) |
| Query | 4 — Semantic search over index | [skills/query-pinecone/SKILL.md](skills/query-pinecone/SKILL.md) |

Each skill documents its own commands, flags, and incremental behavior.

---

## Pipeline layout

All pipeline artifacts live under the repo at
`data/assets/abd-answers-memory-pipeline/`. See
`scripts/source-convert/PIPELINE_CONTRACT.md` for the authoritative path
contract.

| Subfolder | Contents |
|-----------|----------|
| `markdown/` | Converted `.md` from source files |
| `chunked/` | Chunk files ready for embedding |
| `rag/` | Pinecone sync manifest only (no local FAISS) |

Path resolvers: Python `scripts/source-convert/_config.py`, TypeScript
`packages/answers/server/src/abd-answers-paths.ts`.

---

## Secrets

`conf/.secrets` must have `PINECONE_API_KEY`, `PINECONE_INDEX`, and
OpenAI keys. See `conf/.secrets.example` and `conf/answers-memory.env.example`.

---

## Change detection workflow

When content under `data/assets/` changes (files added, modified, or deleted):

1. **Identify what changed** — which source files under `data/assets/` are
   new, modified, or deleted.
2. **Convert** — run `convert-content` with `--update` on the affected path.
   This is incremental; unchanged files are skipped.
3. **Chunk** — run `chunk-content` with `--update` on the same path. Skips
   chunks whose source markdown hasn't changed.
4. **Embed** — run `embed-pinecone` with `--rel` scoped to the changed
   folder. Delta sync skips unchanged content hashes.
5. **Deleted files** — if source files were removed, run a full embed (no
   `--rel`) so reconcile detects orphaned vectors, or use
   `PINECONE_SYNC_FORCE_RECONCILE=1`.

### Full pipeline (PowerShell shortcut)

```powershell
.\scripts\rag\run-pipeline-stages.ps1 -SourcePath "<path-under-data/assets>"
```

Use `-SkipConvert`, `-SkipChunk`, or `-SkipBuildRag` to skip stages.

---

## RAG chat suggestion

Watch for signals that abd-answers context would help the conversation:

- The user asks about agile practices, delivery methods, or topics that
  match content hub material.
- The user references documents, training content, or knowledge base entries.
- The user is working in a domain covered by the abd-answers content.

When you detect these signals, **suggest** (do not force):

> "This sounds like something in the abd-answers content hub. Want me to
> use abd-answers for this chat?"

Once activated, follow the query-pinecone skill protocol: retrieve before
answering, cite chunks, honor path filters.

---

## Orchestration rules

1. **Stage order matters.** Convert before chunk, chunk before embed. Never
   embed stale chunks.
2. **Prefer incremental.** Use `--update` and `--rel` by default. Full runs
   only when reconciling deletes or when the user asks for a clean rebuild.
3. **Report what happened.** After each pipeline run, summarize: files
   converted, chunks created/updated, vectors upserted/unchanged. The user
   should know what changed.
4. **Don't auto-embed without confirmation.** Embedding costs money (OpenAI
   API calls). Always tell the user what will be embedded and approximate
   scope before running stage 3.

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| `No Pinecone RAG ref` | Run stage 3 after chunking; verify `PINECONE_*` in `conf/.secrets` |
| Empty query results | Run `npm run rag:query` with and without `--folders` to check filter scope |
| Convert/chunk errors | `pip install "markitdown[all]"`; run from repo root so `_config.py` resolves |
| build-rag 401 | Answers auth enabled — use CLI `migrate-memory-to-pinecone.ts` instead |

---

## Code references

- Shared modules: `scripts/shared/` (env loader, path resolver, rag core)
- Pipeline paths: `skills/convert-content/scripts/_config.py`, `scripts/shared/abd-answers-paths.ts`
- Pipeline contract: `skills/convert-content/scripts/PIPELINE_CONTRACT.md`
- Pinecone search: `scripts/shared/rag/pinecone-rag.ts`
- CLI embed: `skills/embed-pinecone/scripts/migrate-memory-to-pinecone.ts`
- CLI query: `skills/query-pinecone/scripts/agent-pinecone-query.ts`
