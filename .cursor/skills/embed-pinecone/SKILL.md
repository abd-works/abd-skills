---
name: embed-pinecone
description: >-
  Embed chunked content into Pinecone via delta sync. Use after chunk-content
  has run, when vectors need refreshing, or when new chunks appear.
---
# embed-pinecone

## Purpose

Stage 3 of the abd-answers memory pipeline: embed `chunked/` files into
Pinecone using content-hash delta sync.

## Commands (run from the agent root: agents/abd-answers/)

**Full embed (all chunks):**

```bash
node --import tsx skills/embed-pinecone/scripts/migrate-memory-to-pinecone.ts
```

**Scoped to a folder (path relative to `chunked/`, forward slashes):**

```bash
node --import tsx skills/embed-pinecone/scripts/migrate-memory-to-pinecone.ts --rel "01 Agile Practices/6) Agile Change"
```

**Single file after incremental convert + chunk:**

```bash
node --import tsx skills/embed-pinecone/scripts/migrate-memory-to-pinecone.ts --rel "01 Agile Practices/6) Agile Change/Change-Canvas-Template.md"
```

## Delta behavior

For each `.md` in `chunked/`, compares content hash and chunk IDs against
`rag/pinecone-manifest.json`. Unchanged files are skipped (logged as
`unchangedFiles`).

**Reconcile:** Full-namespace list+fetch is skipped when using `--rel`. Use a
full run (no `--rel`) or `PINECONE_SYNC_FORCE_RECONCILE=1` for a whole-index
sweep. `PINECONE_SYNC_SKIP_RECONCILE=1` skips reconcile on full runs.

## Additional flags

See `skills/embed-pinecone/scripts/migrate-memory-to-pinecone.ts` header: `--wipe`,
`--resume-from-log`, `--memory-root-id`, `--log`, `--no-log-file`.

## Alternative: HTTP (if app-server running)

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:3001/api/answers/files/build-rag" -Method Post -ContentType "application/json" -Body '{"scope":"memory"}'
```

## Requirements

`PINECONE_API_KEY`, `PINECONE_INDEX` (and optional namespace) in `conf/.secrets`.
OpenAI (or configured) keys for embeddings.

## Paths

- Input: `abd-answers-memory-pipeline/chunked/`
- Manifest: `abd-answers-memory-pipeline/rag/pinecone-manifest.json`
- Script: `skills/embed-pinecone/scripts/migrate-memory-to-pinecone.ts`
- Shared paths: `scripts/shared/abd-answers-paths.ts`
