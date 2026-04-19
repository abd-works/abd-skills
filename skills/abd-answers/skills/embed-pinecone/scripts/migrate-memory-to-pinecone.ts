import { appendFile, mkdir, readFile } from 'node:fs/promises';
import { existsSync, unlinkSync } from 'node:fs';
import path from 'node:path';
import { Pinecone } from '@pinecone-database/pinecone';
import {
  applyConfMemoryEnv,
  applyConfSecretsEnv,
  applyPineconeFromConfSecrets,
  applyRootEnvFile,
} from '../../../scripts/shared/load-conf-openai-key.js';
import {
  getAbdAnswersRepoRoot,
  resolvePipelineChunkedAbs,
  resolvePipelineRagAbs,
  resolveSourceFilesRootAbs,
} from '../../../scripts/shared/abd-answers-paths.js';
import { resolvePineconeNamespace } from '../../../scripts/shared/rag/pinecone-namespace.js';
import { syncFolderToPineconeDelta } from '../../../scripts/shared/rag/pinecone-rag.js';

/**
 * Delta-sync chunked pipeline `.md` to Pinecone (reads **`chunked/`** only — not `markdown/`).
 *
 * Env loading matches app-server: `abd-answers/.env` → `conf/answers-memory.env` →
 * `conf/.secrets` (multi-root) → `PINECONE_*` from `conf/secrets` then `conf/.secrets` (overrides).
 *
 * **Progress log (default):** `data/pinecone-chunk-sync.log` under the abd-answers repo root
 * (same lines as stdout, each line prefixed with ISO timestamp). Override with `--log <path>`;
 * disable file logging with `--no-log-file`.
 *
 * Usage:
 *   node --import tsx scripts/migrate-memory-to-pinecone.ts
 *   node --import tsx scripts/migrate-memory-to-pinecone.ts --wipe
 *   node --import tsx scripts/migrate-memory-to-pinecone.ts --wipe-only
 *   node --import tsx scripts/migrate-memory-to-pinecone.ts --resume-from-log
 *
 * `--rel <path>`: only embed chunked files under this path (relative to `chunked/`). Does not wipe
 * or remove vectors outside this scope. Examples:
 *   - folder: `--rel "12 AI Augmented Delivery/Augmented AI Delivery"`
 *   - **single file** (only read/hash/embed that one): `--rel "01 Agile Practices/6) Agile Change/Change-Canvas-Template.md"`
 *
 * **Unchanged files:** for each scoped file, sync compares SHA of disk content to `pinecone-manifest.json`.
 * Matching hash + same chunk id count → **no embedding** for that file (`unchangedFiles` in the done line).
 * Use `PINECONE_SYNC_SKIP_RECONCILE=1` to skip the full-namespace reconcile (faster incremental runs).
 *
 * `--wipe`: delete all vectors in the Pinecone namespace for `--memory-root-id`, remove
 * `pinecone-manifest.json`, then embed the full chunked tree (default folder).
 *
 * `--wipe-only`: same Pinecone delete + remove manifest, then **exit** (no re-embed). Use this
 * when you want an empty namespace before running a separate embed job.
 *
 * **Resume / manifest loss:** `syncFolderToPineconeDelta` reconciles from **Pinecone** before
 * embedding: it lists `md_*` vector ids, fetches metadata (`path`, `fileHash`), and skips
 * re-embed when disk hash and chunk ids match the index (so a deleted `pinecone-manifest.json`
 * does not force a full re-embed). Orphan vectors (paths not on disk) are deleted.
 *
 * Env (optional):
 * - **Scoped `--rel`:** full-namespace list+fetch reconcile is **skipped by default** (otherwise one-file runs scan the whole index). Manifest + hash handles normal updates. For a full sweep (e.g. lost manifest), run migrate **without** `--rel` or set `PINECONE_SYNC_FORCE_RECONCILE=1`.
 * - `PINECONE_SYNC_SKIP_RECONCILE=1` — skip DB reconcile (manifest-only; faster, less safe). Redundant when using `--rel` (already skipped).
 * - `PINECONE_SYNC_FORCE_RECONCILE=1` — with `--rel`, force the slow full-namespace reconcile anyway.
 * - `PINECONE_RECONCILE_LIST_LIMIT` — list page size (default 1000, max 10000).
 * - `PINECONE_RECONCILE_FETCH_BATCH` — fetch batch size (default 500, max 1000).
 * - `PINECONE_FETCH_CONCURRENCY` — parallel reconcile `fetch` waves (default 6, max 32). Raise to
 *   shorten list+metadata phase; lower if Pinecone returns 429.
 * - `PINECONE_UPSERT_CONCURRENCY` — parallel upsert batches per file after embed (default 4, max 16).
 *
 * Resume flag:
 * - `--resume-from-log` — uses last `embedding ... : <file>` line as checkpoint and starts after it.
 *   If `PINECONE_SYNC_SKIP_RECONCILE` is unset, this mode sets it to `1` for faster restart.
 */

function argValue(flag: string): string | undefined {
  const i = process.argv.indexOf(flag);
  if (i < 0 || i >= process.argv.length - 1) return undefined;
  return process.argv[i + 1];
}

const DEFAULT_PROGRESS_LOG = path.join('data', 'pinecone-chunk-sync.log');

async function readLastEmbeddedFileFromLog(logAbs: string): Promise<string | undefined> {
  try {
    const raw = await readFile(logAbs, 'utf8');
    const lines = raw.split(/\r?\n/);
    for (let i = lines.length - 1; i >= 0; i--) {
      const line = lines[i] ?? '';
      const m = line.match(/\]\s+\[[0-9]+\/[0-9]+\]\s+embedding\s+[0-9]+\s+vector\(s\):\s+(.+)$/);
      if (m?.[1]) return m[1].trim();
    }
    return undefined;
  } catch {
    return undefined;
  }
}

async function main(): Promise<void> {
  const repoRoot = getAbdAnswersRepoRoot();
  applyRootEnvFile(repoRoot);
  applyConfMemoryEnv(repoRoot);
  applyConfSecretsEnv(repoRoot);
  applyPineconeFromConfSecrets(repoRoot);

  const wipeOnly = process.argv.includes('--wipe-only');
  const wipe = process.argv.includes('--wipe') || wipeOnly;
  const noLogFile = process.argv.includes('--no-log-file');
  const logArg = argValue('--log')?.trim();
  const logAbs =
    noLogFile ? null : path.resolve(repoRoot, logArg || DEFAULT_PROGRESS_LOG);

  async function logLine(line: string): Promise<void> {
    console.log(line);
    if (!logAbs) return;
    await mkdir(path.dirname(logAbs), { recursive: true });
    const ts = new Date().toISOString();
    await appendFile(logAbs, `[${ts}] ${line}\n`, 'utf8');
  }

  const folderAbs = argValue('--folder')?.trim() || resolvePipelineChunkedAbs();
  const relPath = argValue('--rel')?.trim() || '';
  const memoryRootId =
    argValue('--memory-root-id')?.trim() || '831ca1cf-a4bd-4a24-a432-9a8563c50726';
  const ragDir = resolvePipelineRagAbs();
  const manifestPath = path.join(ragDir, 'pinecone-manifest.json');

  await logLine(
    logAbs ?
      `log file: ${logAbs} (override: --log <path>, disable: --no-log-file)`
    : 'file logging disabled (--no-log-file)',
  );
  await logLine(`chunked source (only): ${folderAbs}`);

  const resumeFromLog = process.argv.includes('--resume-from-log');
  let startAfterFileRel: string | undefined;
  if (resumeFromLog && logAbs) {
    startAfterFileRel = await readLastEmbeddedFileFromLog(logAbs);
    if (startAfterFileRel) {
      await logLine(`resume-from-log: last embedded file checkpoint = ${startAfterFileRel}`);
      if (process.env.PINECONE_SYNC_SKIP_RECONCILE == null) {
        process.env.PINECONE_SYNC_SKIP_RECONCILE = '1';
        await logLine('resume-from-log: set PINECONE_SYNC_SKIP_RECONCILE=1 (manifest/log checkpoint mode)');
      }
    } else {
      await logLine('resume-from-log: no embedding checkpoint found in log; using normal reconcile');
    }
  }

  if (wipe) {
    const pineconeApiKey = process.env.PINECONE_API_KEY?.trim();
    const pineconeIndex = process.env.PINECONE_INDEX?.trim();
    if (!pineconeApiKey) throw new Error('PINECONE_API_KEY is required for --wipe / --wipe-only');
    if (!pineconeIndex) throw new Error('PINECONE_INDEX is required for --wipe / --wipe-only');
    const ns = resolvePineconeNamespace(memoryRootId);
    await logLine(`Wiping Pinecone namespace: ${ns}`);
    const pc = new Pinecone({ apiKey: pineconeApiKey });
    await pc.index(pineconeIndex).namespace(ns).deleteAll();
    await logLine('Pinecone namespace cleared.');
    if (existsSync(manifestPath)) {
      unlinkSync(manifestPath);
      await logLine(`Removed local manifest: ${manifestPath}`);
    }
  }

  if (wipeOnly) {
    await logLine('Done (--wipe-only: skipped re-embed).');
    return;
  }

  const result = await syncFolderToPineconeDelta({
    folderAbs,
    relPath,
    memoryRootId,
    sourceFilesRootAbs: resolveSourceFilesRootAbs(),
    manifestDirAbs: ragDir,
    startAfterFileRel,
    onProgress: (line) => {
      void logLine(line);
    },
  });
  await logLine(JSON.stringify(result, null, 2));
}

void main().catch(async (error) => {
  const repoRoot = getAbdAnswersRepoRoot();
  const noLogFile = process.argv.includes('--no-log-file');
  const logArg = argValue('--log')?.trim();
  const logAbs = noLogFile ? null : path.resolve(repoRoot, logArg || DEFAULT_PROGRESS_LOG);
  const message = error instanceof Error ? error.message : String(error);
  const stack = error instanceof Error ? error.stack : undefined;
  const fatalLine = `FATAL sync error: ${message}`;

  console.error(fatalLine);
  if (stack) console.error(stack);

  if (logAbs) {
    try {
      await mkdir(path.dirname(logAbs), { recursive: true });
      const ts = new Date().toISOString();
      await appendFile(logAbs, `[${ts}] ${fatalLine}\n`, 'utf8');
      if (stack) {
        await appendFile(logAbs, `[${ts}] ${stack}\n`, 'utf8');
      }
    } catch {
      // Last-ditch path: never rethrow from fatal logger.
    }
  }
  process.exitCode = 1;
});
