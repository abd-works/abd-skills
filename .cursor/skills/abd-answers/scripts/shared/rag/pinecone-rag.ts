import type { RetrievalChunk } from '../types.js';
import { Pinecone } from '@pinecone-database/pinecone';
import { randomUUID, createHash } from 'node:crypto';
import { appendFile, mkdir, readFile, readdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { sourceRelToFilesDownloadUrl } from '../abd-answers-paths.js';
import { estimateTokens } from './chunk-keyword-rank.js';
import { normalizeRel, resolvePineconeNamespace } from './pinecone-namespace.js';
export { resolvePineconeNamespace };
import {
  getOpenAiApiKeyCandidates,
  openAiJsonRequestHeaders,
  shouldRetryOpenAiWithDifferentKey,
} from './openai-keys.js';

const OPENAI_EMBEDDING_MODEL = 'text-embedding-3-small';
const OPENAI_EMBEDDING_DIMENSION = 1536;
const MAX_CHUNK_CHARS = 7000;
const EMBED_BATCH_SIZE = 8;
const UPSERT_BATCH_SIZE = 100;
const EMBED_MAX_RETRIES = 20;
/** Chat query embedding: fail faster so the UI is not stuck on "Working…" for minutes on 429 storms. */
const EMBED_QUERY_MAX_RETRIES = 4;
const PINECONE_DEFAULT_CLOUD = 'aws';
const PINECONE_DEFAULT_REGION = 'us-east-1';

type PineconeRagRecordMeta = {
  title: string;
  path: string;
  source: string;
  content: string;
  fileHash: string;
  /** Directory path under the memory content root (forward slashes), for query-time scope filtering. */
  memoryFolder: string;
};

type PineconeManifest = {
  version: 1;
  indexName: string;
  namespace: string;
  files: Record<string, { hash: string; ids: string[] }>;
  updatedAt: string;
  /** Bumped when embedded metadata shape changes; lower values force re-embed on next sync. */
  metadataVersion?: number;
};

/** Increment when chunk metadata must be rewritten (e.g. new `memoryFolder` field). */
const PINECONE_METADATA_VERSION = 3;

type LocalChunk = {
  id: string;
  pathRel: string;
  title: string;
  sourceRelToAssets: string;
  content: string;
};

export type PineconeSemanticSearchOpts = {
  sourceFilesRootAbs?: string;
  sourceUrlPathPrefix?: string;
  /** When set, only chunks whose `memoryFolder` metadata is this path or a subpath are returned. */
  memoryScopeFolder?: string;
  /** When set, chunk matches if it matches any of these folder roots (OR). Overrides `memoryScopeFolder` when non-empty. */
  memoryScopeFolders?: string[];
};

export type PineconeDeltaSyncResult = {
  ragRef: string;
  namespace: string;
  indexName: string;
  upserted: number;
  deleted: number;
  unchangedFiles: number;
  changedFiles: number;
  /** Files matched to Pinecone (hash + chunk ids) and merged into manifest state before embed. */
  reconciledFromPinecone?: number;
  /** Vectors removed because their `path` no longer exists on disk. */
  orphanVectorsDeleted?: number;
};

/** Directory path relative to memory hub root, aligned with UI virtual paths (forward slashes). */
export function memoryFolderFromSync(relPath: string, fileRel: string): string {
  const rel = normalizeRel(relPath).replace(/^\/+|\/+$/g, '');
  const posix = fileRel.split(path.sep).join('/');
  const dir = path.posix.dirname(posix);
  const dirNorm = dir === '.' ? '' : dir.replace(/^\/+|\/+$/g, '');
  if (!rel) return dirNorm;
  return dirNorm ? `${rel}/${dirNorm}` : rel;
}

function normalizeMemoryScopePath(p: string): string {
  return p.replace(/\\/g, '/').replace(/^\/+|\/+$/g, '');
}

function metadataMatchesMemoryScope(scope: string, meta: Record<string, unknown>): boolean {
  const mfRaw = meta.memoryFolder;
  if (typeof mfRaw !== 'string' || !mfRaw.trim()) return false;
  const scopeN = normalizeMemoryScopePath(scope);
  const mf = normalizeMemoryScopePath(mfRaw);
  return mf === scopeN || mf.startsWith(`${scopeN}/`);
}

function sha(input: string): string {
  return createHash('sha256').update(input).digest('hex');
}

/** Full path from memory hub root (forward slashes) for stable chunk ids in a shared namespace. */
export function globalRelForChunk(virtualPrefix: string, relWithinFolder: string): string {
  const a = normalizeRel(virtualPrefix).replace(/^\/+|\/+$/g, '');
  const b = normalizeRel(relWithinFolder).replace(/^\/+|\/+$/g, '');
  if (!a) return b;
  return b ? `${a}/${b}` : a;
}

function splitLongMarkdown(text: string): string[] {
  const src = text.trim();
  if (!src) return [];
  if (src.length <= MAX_CHUNK_CHARS) return [src];
  const out: string[] = [];
  let i = 0;
  while (i < src.length) {
    const end = Math.min(i + MAX_CHUNK_CHARS, src.length);
    out.push(src.slice(i, end).trim());
    i = end;
  }
  return out.filter(Boolean);
}

async function walkMarkdownFiles(rootAbs: string, curAbs: string, out: string[]): Promise<void> {
  const entries = await readdir(curAbs, { withFileTypes: true });
  for (const ent of entries) {
    if (ent.name.startsWith('.')) continue;
    const abs = path.join(curAbs, ent.name);
    if (ent.isDirectory()) {
      if (ent.name.toLowerCase() === 'rag') continue;
      await walkMarkdownFiles(rootAbs, abs, out);
      continue;
    }
    if (!ent.isFile()) continue;
    if (path.extname(ent.name).toLowerCase() !== '.md') continue;
    out.push(path.relative(rootAbs, abs));
  }
}

/** True if `fileRel` (chunk path under `folderAbs`) is `scope` or a file under that directory. */
function fileRelUnderScope(fileRel: string, scopePrefix: string): boolean {
  const fr = normalizeRel(fileRel).replace(/^\/+|\/+$/g, '');
  const sp = normalizeRel(scopePrefix).replace(/^\/+|\/+$/g, '');
  if (!sp) return true;
  return fr === sp || fr.startsWith(`${sp}/`);
}

async function collectLocalChunks(
  folderAbs: string,
  sourceFilesRootAbs: string,
  /**
   * When set (forward slashes, relative to `folderAbs`), only process:
   * - a **single** `.md` file if this path points to a file on disk, or
   * - all `.md` under a **directory** (recursive walk).
   * Chunk ids use full `rel` from `folderAbs` (same as a full-tree sync) so partial runs match existing vectors.
   */
  scopeRelPrefix: string,
): Promise<{ files: Record<string, { hash: string; chunks: LocalChunk[] }> }> {
  const markdownRels: string[] = [];
  const scope = normalizeRel(scopeRelPrefix).replace(/^\/+|\/+$/g, '');
  if (scope) {
    const subRoot = path.join(folderAbs, ...scope.split('/'));
    try {
      const st = await stat(subRoot);
      if (st.isFile() && subRoot.toLowerCase().endsWith('.md')) {
        // Single chunked file: only read/hash/embed this path (not the whole folder tree).
        markdownRels.push(normalizeRel(path.relative(folderAbs, subRoot)));
      } else if (st.isDirectory()) {
        await walkMarkdownFiles(folderAbs, subRoot, markdownRels);
      } else {
        return { files: {} };
      }
    } catch {
      return { files: {} };
    }
  } else {
    await walkMarkdownFiles(folderAbs, folderAbs, markdownRels);
  }
  const files: Record<string, { hash: string; chunks: LocalChunk[] }> = {};
  for (const relFs of markdownRels) {
    const abs = path.join(folderAbs, relFs);
    const raw = await readFile(abs, 'utf8');
    const fileHash = sha(raw);
    const rel = normalizeRel(relFs);
    const title = path.basename(rel);
    // Always relative to `sourceFilesRootAbs` (hub assets root). `sourceUrlFromMeta` joins this to
    // that root to build `/files/download?scope=assets&path=...`. If we stored paths relative only
    // to `folderAbs` (e.g. markdown pipeline root when `markdownMirrorsSourceTree` was true), URLs
    // pointed at `assets/<folder>/file.md` instead of `assets/abd-answers-memory-pipeline/markdown/...`.
    const sourceRel = normalizeRel(path.relative(sourceFilesRootAbs, abs));
    const idKey = globalRelForChunk('', rel);
    const parts = splitLongMarkdown(raw);
    const chunks: LocalChunk[] = parts.map((chunk, idx) => {
      const id = `md_${sha(`${idKey}#${idx}#${chunk}`)}`;
      return {
        id,
        pathRel: rel,
        title,
        sourceRelToAssets: sourceRel,
        content: chunk,
      };
    });
    files[rel] = { hash: fileHash, chunks };
  }
  return { files };
}

async function embedTextsWithSingleKey(
  apiKey: string,
  texts: string[],
  maxRetriesPerBatch: number = EMBED_MAX_RETRIES,
): Promise<number[][]> {
  const out: number[][] = [];
  for (let i = 0; i < texts.length; i += EMBED_BATCH_SIZE) {
    const batch = texts.slice(i, i + EMBED_BATCH_SIZE);
    let embedded: number[][] | null = null;
    for (let attempt = 0; attempt <= maxRetriesPerBatch; attempt++) {
      const res = await fetch('https://api.openai.com/v1/embeddings', {
        method: 'POST',
        headers: openAiJsonRequestHeaders(apiKey),
        body: JSON.stringify({
          model: OPENAI_EMBEDDING_MODEL,
          input: batch,
        }),
      });
      if (res.ok) {
        const json = (await res.json()) as { data?: Array<{ embedding?: number[] }> };
        embedded = (json.data ?? []).map((d) => d.embedding ?? []);
        break;
      }
      const body = await res.text();
      if ([429, 500, 502, 503, 504].includes(res.status) && attempt < maxRetriesPerBatch) {
        // Respect Retry-After when present; otherwise use exponential backoff.
        const retryAfter = Number(res.headers.get('retry-after') ?? '');
        const sleepMs =
          Number.isFinite(retryAfter) && retryAfter > 0 ?
            Math.ceil(retryAfter * 1000)
          : Math.min(60_000, 2_000 * Math.pow(2, attempt));
        await new Promise((resolve) => setTimeout(resolve, sleepMs));
        continue;
      }
      throw new Error(`OpenAI embeddings ${res.status}: ${body.slice(0, 200)}`);
    }
    if (!embedded || embedded.length !== batch.length || embedded.some((v) => v.length === 0)) {
      throw new Error('OpenAI embeddings: incomplete batch response after retries');
    }
    out.push(...embedded);
  }
  return out;
}

/** Uses OPENAI_API_KEY, then OPEN_API_KEY_2 / OPENAI_API_KEY_2 when the first key fails. */
async function embedTexts(
  texts: string[],
  opts?: { maxRetriesPerBatch?: number },
): Promise<number[][]> {
  const keys = getOpenAiApiKeyCandidates();
  if (keys.length === 0) {
    throw new Error('OPENAI_API_KEY is required for embeddings');
  }
  const maxRetries = opts?.maxRetriesPerBatch ?? EMBED_MAX_RETRIES;
  let last: Error | undefined;
  for (let ki = 0; ki < keys.length; ki++) {
    try {
      return await embedTextsWithSingleKey(keys[ki]!, texts, maxRetries);
    } catch (e) {
      last = e instanceof Error ? e : new Error(String(e));
      if (ki < keys.length - 1 && shouldRetryOpenAiWithDifferentKey(last)) continue;
      throw last;
    }
  }
  throw last ?? new Error('OpenAI embeddings failed');
}

function manifestPathFor(folderAbs: string, manifestDirAbs?: string): string {
  const dir = manifestDirAbs?.trim();
  if (dir) {
    return path.join(path.resolve(dir), 'pinecone-manifest.json');
  }
  return path.join(folderAbs, 'rag', 'pinecone-manifest.json');
}

async function loadManifest(folderAbs: string, manifestDirAbs?: string): Promise<PineconeManifest | null> {
  const p = manifestPathFor(folderAbs, manifestDirAbs);
  try {
    const raw = await readFile(p, 'utf8');
    const parsed = JSON.parse(raw) as PineconeManifest;
    if (!parsed || parsed.version !== 1 || typeof parsed.files !== 'object') return null;
    return parsed;
  } catch {
    return null;
  }
}

function setsEqualString(a: Set<string>, b: Set<string>): boolean {
  if (a.size !== b.size) return false;
  for (const x of a) {
    if (!b.has(x)) return false;
  }
  return true;
}

async function safeDeleteMany(
  index: { deleteMany: (o: { ids: string[] }) => Promise<void> },
  ids: string[],
): Promise<void> {
  if (ids.length === 0) return;
  try {
    await index.deleteMany({ ids });
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    if (msg.includes('404') || /not\s*found|NotFound/i.test(msg)) return;
    throw e;
  }
}

/** Run up to `concurrency` Pinecone fetches at once; merge results on the main thread (no shared-map races). */
async function fetchBatchesWithConcurrency(opts: {
  index: {
    fetch: (o: { ids: string[] }) => Promise<{
      records: Record<string, { metadata?: Record<string, unknown> } | undefined>;
    }>;
  };
  idBatches: string[][];
  concurrency: number;
  onProgress?: (doneBatches: number, totalBatches: number) => void;
}): Promise<Array<{ batch: string[]; records: Record<string, { metadata?: Record<string, unknown> } | undefined> }>> {
  const out: Array<{
    batch: string[];
    records: Record<string, { metadata?: Record<string, unknown> } | undefined>;
  }> = [];
  const { idBatches, concurrency } = opts;
  const total = idBatches.length;
  let done = 0;
  for (let i = 0; i < idBatches.length; i += concurrency) {
    const window = idBatches.slice(i, i + concurrency);
    const parts = await Promise.all(
      window.map(async (batch) => {
        const res = await opts.index.fetch({ ids: batch });
        return { batch, records: res.records ?? {} };
      }),
    );
    out.push(...parts);
    done += parts.length;
    opts.onProgress?.(done, total);
  }
  return out;
}

function envInt(name: string, fallback: number, min: number, max: number): number {
  const n = Number(process.env[name]?.trim());
  if (!Number.isFinite(n)) return fallback;
  return Math.min(max, Math.max(min, Math.floor(n)));
}

/**
 * Pinecone rejects malformed UTF-16 payloads (lone surrogates).
 * Replace invalid code units so one bad chunk cannot kill a long sync run.
 */
function sanitizeForJsonUtf16(input: string): string {
  if (!input) return input;
  return input.replace(
    /[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/g,
    '\uFFFD',
  );
}

function errorTypeKey(e: unknown): string {
  const name = (e as { name?: unknown } | null)?.name;
  const msg = e instanceof Error ? e.message : String(e);
  const n = typeof name === 'string' ? name : 'Error';
  if (/Missing low surrogate/i.test(msg)) return `${n}:MissingLowSurrogate`;
  if (/429|Too Many Requests/i.test(msg)) return `${n}:RateLimit`;
  return n;
}

async function appendSyncErrorReport(opts: {
  reportPath: string;
  fileRel: string;
  phase: string;
  errorType: string;
  error: unknown;
}): Promise<void> {
  const msg = opts.error instanceof Error ? opts.error.message : String(opts.error);
  const row = {
    ts: new Date().toISOString(),
    file: opts.fileRel,
    phase: opts.phase,
    errorType: opts.errorType,
    message: msg.slice(0, 1200),
  };
  await mkdir(path.dirname(opts.reportPath), { recursive: true });
  await appendFile(opts.reportPath, `${JSON.stringify(row)}\n`, 'utf8');
}

/**
 * When the local manifest is missing or incomplete, list + fetch vectors in the namespace and
 * rebuild per-file `{ hash, ids }` from metadata so we do not re-embed work already in Pinecone.
 * Also deletes vectors whose `path` is not present on disk (orphans).
 *
 * Set `PINECONE_SYNC_SKIP_RECONCILE=1` to skip (manifest-only mode).
 *
 * **Scoped sync (`--rel` / partial folder):** By default we also skip the full-namespace sweep —
 * listing and fetching every vector is O(entire index) and defeats “one file” runs. Manifest +
 * per-file hash compare is enough for normal updates. Use full migrate (no `--rel`) or set
 * `PINECONE_SYNC_FORCE_RECONCILE=1` when you need a full reconcile (e.g. lost manifest recovery).
 */
async function hydratePrevFilesFromPinecone(opts: {
  index: {
    listPaginated: (o?: {
      prefix?: string;
      limit?: number;
      paginationToken?: string;
    }) => Promise<{ vectors?: Array<{ id?: string }>; pagination?: { next?: string } }>;
    fetch: (o: { ids: string[] }) => Promise<{
      records: Record<string, { metadata?: Record<string, unknown> } | undefined>;
    }>;
    deleteMany: (o: { ids: string[] }) => Promise<void>;
  };
  currentFiles: Record<string, { hash: string; chunks: LocalChunk[] }>;
  prevFiles: Record<string, { hash: string; ids: string[] }>;
  onProgress?: (line: string) => void;
  /** When set, do not treat paths outside this prefix as orphans (partial sync). */
  scopeRelPrefix?: string;
}): Promise<{
  prevFiles: Record<string, { hash: string; ids: string[] }>;
  reconciledFromPinecone: number;
  orphanVectorsDeleted: number;
}> {
  if (process.env.PINECONE_SYNC_SKIP_RECONCILE?.trim() === '1') {
    opts.onProgress?.('reconcile: skipped (PINECONE_SYNC_SKIP_RECONCILE=1)');
    return { prevFiles: opts.prevFiles, reconciledFromPinecone: 0, orphanVectorsDeleted: 0 };
  }

  const scope = (opts.scopeRelPrefix ?? '').trim();
  if (scope && process.env.PINECONE_SYNC_FORCE_RECONCILE?.trim() !== '1') {
    opts.onProgress?.(
      'reconcile: skipped (scoped sync — not scanning full namespace; manifest + per-file hash only. Full sweep: migrate without --rel, or PINECONE_SYNC_FORCE_RECONCILE=1',
    );
    return { prevFiles: opts.prevFiles, reconciledFromPinecone: 0, orphanVectorsDeleted: 0 };
  }

  const listLimit = Math.min(99, Math.max(1, Number(process.env.PINECONE_RECONCILE_LIST_LIMIT) || 99));
  // Keep batches small: Pinecone fetch may use request URIs; long `md_*` ids × large batches → 414.
  const fetchBatch = Math.min(
    200,
    Math.max(10, Number(process.env.PINECONE_RECONCILE_FETCH_BATCH) || 80),
  );
  const fetchConcurrency = envInt('PINECONE_FETCH_CONCURRENCY', 6, 1, 32);

  const allIds: string[] = [];
  let token: string | undefined;
  try {
    do {
      const page = await opts.index.listPaginated({
        prefix: 'md_',
        limit: listLimit,
        paginationToken: token,
      });
      const vecs = page.vectors ?? [];
      for (const v of vecs) {
        const id = v.id?.trim();
        if (id) allIds.push(id);
      }
      token = page.pagination?.next;
    } while (token);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    opts.onProgress?.(
      `reconcile: could not list vectors (${msg.slice(0, 200)}); continuing with manifest only`,
    );
    return { prevFiles: opts.prevFiles, reconciledFromPinecone: 0, orphanVectorsDeleted: 0 };
  }

  if (allIds.length === 0) {
    opts.onProgress?.('reconcile: namespace has no md_* vectors');
    return { prevFiles: opts.prevFiles, reconciledFromPinecone: 0, orphanVectorsDeleted: 0 };
  }

  const firstListed = allIds[0] ?? '';
  const lastListed = allIds[allIds.length - 1] ?? '';
  const sortedIds = [...allIds].sort();
  const lexFirst = sortedIds[0] ?? '';
  const lexLast = sortedIds[sortedIds.length - 1] ?? '';
  opts.onProgress?.(
    `reconcile: Pinecone list sweep complete — totalVectors=${allIds.length} lastIdInListOrder=${lastListed || '(none)'} firstIdInListOrder=${firstListed || '(none)'}`,
  );
  opts.onProgress?.(
    `reconcile: Pinecone id bounds (lexicographic) — minId=${lexFirst || '(none)'} maxId=${lexLast || '(none)'} (use maxId as “last record” if you need a single stable anchor)`,
  );
  opts.onProgress?.(
    `reconcile: fetching metadata for ${allIds.length} vector id(s) (batch=${fetchBatch} concurrent=${fetchConcurrency})…`,
  );

  type Agg = { ids: Set<string>; fileHashes: Set<string> };
  const byPath = new Map<string, Agg>();

  const idBatches: string[][] = [];
  for (let i = 0; i < allIds.length; i += fetchBatch) {
    idBatches.push(allIds.slice(i, i + fetchBatch));
  }

  const fetchedParts = await fetchBatchesWithConcurrency({
    index: opts.index,
    idBatches,
    concurrency: fetchConcurrency,
    onProgress: (doneBatches, totalBatches) => {
      if (doneBatches % 20 === 0 || doneBatches === totalBatches) {
        opts.onProgress?.(`reconcile: fetch waves ${doneBatches}/${totalBatches} batch(es)…`);
      }
    },
  });

  for (const { batch, records } of fetchedParts) {
    for (const id of batch) {
      const rec = records[id];
      const meta = rec?.metadata ?? {};
      const pathRaw = typeof meta.path === 'string' ? meta.path : '';
      const fileRel = normalizeRel(pathRaw);
      if (!fileRel) continue;
      const fh = typeof meta.fileHash === 'string' ? meta.fileHash : '';
      let agg = byPath.get(fileRel);
      if (!agg) {
        agg = { ids: new Set<string>(), fileHashes: new Set<string>() };
        byPath.set(fileRel, agg);
      }
      agg.ids.add(id);
      if (fh) agg.fileHashes.add(fh);
    }
  }

  const pathsFromDb = [...byPath.keys()].sort();
  const lastPathLex = pathsFromDb[pathsFromDb.length - 1] ?? '';
  const firstPathLex = pathsFromDb[0] ?? '';
  opts.onProgress?.(
    `reconcile: Pinecone metadata — distinctPaths=${byPath.size} lastPathLexicographic=${lastPathLex || '(none)'} firstPathLexicographic=${firstPathLex || '(none)'}`,
  );

  let orphanVectorsDeleted = 0;
  const currentKeys = new Set(Object.keys(opts.currentFiles));
  for (const [fileRel, agg] of byPath) {
    if (currentKeys.has(fileRel)) continue;
    if (scope && !fileRelUnderScope(fileRel, scope)) continue;
    if (agg.ids.size === 0) continue;
    const ids = [...agg.ids];
    try {
      await safeDeleteMany(opts.index, ids);
      orphanVectorsDeleted += ids.length;
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      opts.onProgress?.(`reconcile: orphan delete failed for ${fileRel} (${msg.slice(0, 120)})`);
    }
  }
  if (orphanVectorsDeleted > 0) {
    opts.onProgress?.(`reconcile: removed ${orphanVectorsDeleted} orphan vector(s) (paths not on disk)`);
  }

  const out = { ...opts.prevFiles };
  let reconciledFromPinecone = 0;
  for (const [fileRel, cur] of Object.entries(opts.currentFiles)) {
    const agg = byPath.get(fileRel);
    if (!agg || agg.ids.size === 0) continue;
    if (agg.fileHashes.size > 1) continue;
    const fh = [...agg.fileHashes][0] ?? '';
    if (!fh || fh !== cur.hash) continue;
    const expected = new Set(cur.chunks.map((c) => c.id));
    if (!setsEqualString(expected, agg.ids)) continue;
    out[fileRel] = { hash: cur.hash, ids: [...agg.ids] };
    reconciledFromPinecone += 1;
  }

  if (reconciledFromPinecone > 0) {
    opts.onProgress?.(
      `reconcile: matched ${reconciledFromPinecone} file(s) to Pinecone (same hash and chunk ids as disk) — will skip re-embed`,
    );
  }

  return { prevFiles: out, reconciledFromPinecone, orphanVectorsDeleted };
}

async function saveManifest(
  folderAbs: string,
  manifest: PineconeManifest,
  manifestDirAbs?: string,
): Promise<void> {
  const p = manifestPathFor(folderAbs, manifestDirAbs);
  await mkdir(path.dirname(p), { recursive: true });
  const payload = JSON.stringify(manifest, null, 2);
  for (let attempt = 0; attempt < 8; attempt++) {
    try {
      await writeFile(p, payload, 'utf8');
      return;
    } catch (e) {
      const code = (e as { code?: string } | null)?.code;
      if ((code === 'EBUSY' || code === 'EPERM') && attempt < 7) {
        await new Promise((resolve) => setTimeout(resolve, 250 * (attempt + 1)));
        continue;
      }
      throw e;
    }
  }
}

function parseRagRef(ragRef: string): { indexName: string; namespace: string } {
  const t = ragRef.trim();
  if (!t.startsWith('pinecone://')) throw new Error('Not a pinecone rag ref');
  const rest = t.slice('pinecone://'.length);
  const slash = rest.indexOf('/');
  if (slash <= 0 || slash === rest.length - 1) {
    throw new Error(`Invalid pinecone rag ref: ${ragRef}`);
  }
  return {
    indexName: rest.slice(0, slash),
    namespace: rest.slice(slash + 1),
  };
}

function ragRef(indexName: string, namespace: string): string {
  return `pinecone://${indexName}/${namespace}`;
}

/** `meta.source` must be relative to `opts.sourceFilesRootAbs` (hub assets root), as produced at Pinecone sync. */
function sourceUrlFromMeta(meta: Record<string, unknown>, opts?: PineconeSemanticSearchOpts): string | undefined {
  const source = typeof meta.source === 'string' ? meta.source : '';
  if (!source) return undefined;
  if (/^https?:\/\//i.test(source)) return source;
  if (!opts?.sourceFilesRootAbs || !opts?.sourceUrlPathPrefix) return undefined;
  const abs = path.join(opts.sourceFilesRootAbs, source.replace(/^[/\\]+/, ''));
  const apiRoot = opts.sourceUrlPathPrefix.replace(/\/files\/source\/?$/, '').replace(/\/+$/, '') || '/api/answers';
  return sourceRelToFilesDownloadUrl(abs, opts.sourceFilesRootAbs, apiRoot);
}

async function ensurePineconeIndex(pc: Pinecone, indexName: string): Promise<void> {
  const existing = await pc.listIndexes();
  const names = new Set((existing.indexes ?? []).map((i) => i.name).filter(Boolean));
  if (names.has(indexName)) return;

  const cloud = (process.env.PINECONE_CLOUD?.trim() || PINECONE_DEFAULT_CLOUD) as
    | 'aws'
    | 'gcp'
    | 'azure';
  const region = process.env.PINECONE_REGION?.trim() || PINECONE_DEFAULT_REGION;
  await pc.createIndex({
    name: indexName,
    dimension: OPENAI_EMBEDDING_DIMENSION,
    metric: 'cosine',
    spec: { serverless: { cloud, region } },
  });

  // Wait until index is ready before first upsert/query.
  for (let i = 0; i < 60; i++) {
    const desc = await pc.describeIndex(indexName);
    const ready = Boolean(desc?.status?.ready);
    if (ready) return;
    await new Promise((resolve) => setTimeout(resolve, 2_000));
  }
  throw new Error(`Pinecone index "${indexName}" was created but is not ready yet`);
}

export function isPineconeRagRef(ragPath: string): boolean {
  return ragPath.trim().startsWith('pinecone://');
}

/** Delta-sync `.md` files under `folderAbs` to Pinecone. For hub RAG, `folderAbs` should be `resolvePipelineChunkedAbs()` (or a subfolder), not `resolvePipelineMarkdownAbs()`. */
export async function syncFolderToPineconeDelta(opts: {
  folderAbs: string;
  relPath: string;
  memoryRootId?: string;
  sourceFilesRootAbs: string;
  /** When set, `pinecone-manifest.json` lives here instead of `<folderAbs>/rag/`. */
  manifestDirAbs?: string;
  /** Progress lines for CLI / log files (e.g. one line per embedded file, not per unchanged file). */
  onProgress?: (line: string) => void;
  /** Optional resume checkpoint: skip files up to and including this relative path. */
  startAfterFileRel?: string;
}): Promise<PineconeDeltaSyncResult> {
  const pineconeApiKey = process.env.PINECONE_API_KEY?.trim();
  const pineconeIndex = process.env.PINECONE_INDEX?.trim();
  if (getOpenAiApiKeyCandidates().length === 0) {
    throw new Error('OPENAI_API_KEY is required for Pinecone sync');
  }
  if (!pineconeApiKey) throw new Error('PINECONE_API_KEY is required for Pinecone sync');
  if (!pineconeIndex) throw new Error('PINECONE_INDEX is required for Pinecone sync');

  const folderStat = await stat(opts.folderAbs);
  if (!folderStat.isDirectory()) throw new Error('Pinecone sync target must be a folder');

  const namespace = resolvePineconeNamespace(opts.memoryRootId);
  const indexName = pineconeIndex;
  const pc = new Pinecone({ apiKey: pineconeApiKey });
  await ensurePineconeIndex(pc, indexName);
  const index = pc.index(indexName).namespace(namespace);

  opts.onProgress?.(`index=${indexName} namespace=${namespace}`);
  const scopePrefix = normalizeRel(opts.relPath ?? '').replace(/^\/+|\/+$/g, '');
  const current = await collectLocalChunks(opts.folderAbs, opts.sourceFilesRootAbs, scopePrefix);
  const allFileEntries = Object.entries(current.files);
  let fileEntries = allFileEntries;
  const totalFiles = allFileEntries.length;
  opts.onProgress?.(
    scopePrefix ?
      `scanned ${totalFiles} chunked .md file(s) under ${opts.folderAbs} — scope: ${scopePrefix}`
    : `scanned ${totalFiles} chunked .md file(s) under ${opts.folderAbs} (pipeline markdown/ is not used)`,
  );
  if (opts.startAfterFileRel) {
    const checkpoint = normalizeRel(opts.startAfterFileRel);
    const ix = allFileEntries.findIndex(([fileRel]) => normalizeRel(fileRel) === checkpoint);
    if (ix >= 0) {
      fileEntries = allFileEntries.slice(ix + 1);
      opts.onProgress?.(
        `resume: checkpoint found at [${ix + 1}/${totalFiles}] ${checkpoint}; processing remaining ${fileEntries.length} file(s)`,
      );
    } else {
      opts.onProgress?.(`resume: checkpoint path not found in current scan (${checkpoint}); processing full scan`);
    }
  }
  const previous = await loadManifest(opts.folderAbs, opts.manifestDirAbs);
  let prevFiles: Record<string, { hash: string; ids: string[] }> = { ...(previous?.files ?? {}) };
  const forceMetaUpgrade = (previous?.metadataVersion ?? 0) < PINECONE_METADATA_VERSION;

  const hydrated = await hydratePrevFilesFromPinecone({
    index,
    currentFiles: current.files,
    prevFiles,
    onProgress: opts.onProgress,
    scopeRelPrefix: scopePrefix || undefined,
  });
  prevFiles = hydrated.prevFiles;
  const reconciledFromPinecone = hydrated.reconciledFromPinecone;
  const orphanVectorsDeleted = hydrated.orphanVectorsDeleted;

  let unchangedFiles = 0;
  let changedFiles = 0;
  let deleted = orphanVectorsDeleted;
  let upserted = 0;
  const nextManifestFiles: PineconeManifest['files'] = {};
  if (scopePrefix) {
    for (const [k, v] of Object.entries(prevFiles)) {
      if (!fileRelUnderScope(k, scopePrefix)) {
        nextManifestFiles[k] = v;
      }
    }
  }
  const errorReportPath = path.join(path.dirname(manifestPathFor(opts.folderAbs, opts.manifestDirAbs)), 'pinecone-sync-errors.jsonl');
  const maxConsecutiveSameError = envInt('PINECONE_MAX_CONSECUTIVE_SAME_ERROR', 5, 1, 100);
  let consecutiveSameErrorType = 0;
  let lastErrorType = '';

  // Delete files removed from disk (manifest paths not present in current scan). Scoped sync only removes in-scope paths.
  let deletedStale = 0;
  for (const [oldPath, oldInfo] of Object.entries(prevFiles)) {
    if (current.files[oldPath]) continue;
    if (scopePrefix && !fileRelUnderScope(oldPath, scopePrefix)) continue;
    if (oldInfo.ids.length > 0) {
      await safeDeleteMany(index, oldInfo.ids);
      deletedStale += oldInfo.ids.length;
      deleted += oldInfo.ids.length;
    }
  }
  if (deletedStale > 0) {
    opts.onProgress?.(
      `removed ${deletedStale} stale vector id(s) (in-scope files removed from disk since last manifest)`,
    );
  }

  let fileNum = 0;
  for (const [fileRel, info] of fileEntries) {
    fileNum += 1;
    const prev = prevFiles[fileRel];
    const unchanged =
      !forceMetaUpgrade &&
      prev &&
      prev.hash === info.hash &&
      prev.ids.length === info.chunks.length;
    if (unchanged) {
      unchangedFiles += 1;
      nextManifestFiles[fileRel] = { hash: prev.hash, ids: [...prev.ids] };
      continue;
    }
    changedFiles += 1;
    opts.onProgress?.(
      `[${fileNum}/${totalFiles}] embedding ${info.chunks.length} vector(s): ${fileRel}`,
    );
    try {
      if (prev?.ids?.length) {
        await safeDeleteMany(index, prev.ids);
        deleted += prev.ids.length;
      }
      if (info.chunks.length > 0) {
        const embeddings = await embedTexts(info.chunks.map((x) => x.content));
        const upsertConcurrency = envInt('PINECONE_UPSERT_CONCURRENCY', 4, 1, 16);
        const upsertSlices: { start: number; items: LocalChunk[] }[] = [];
        for (let i = 0; i < info.chunks.length; i += UPSERT_BATCH_SIZE) {
          upsertSlices.push({ start: i, items: info.chunks.slice(i, i + UPSERT_BATCH_SIZE) });
        }
        for (let w = 0; w < upsertSlices.length; w += upsertConcurrency) {
          const window = upsertSlices.slice(w, w + upsertConcurrency);
          const wave = await Promise.all(
            window.map(async ({ start, items }) => {
              const mf = memoryFolderFromSync('', fileRel);
              const records = items.map((chunk, idx) => {
                const emb = embeddings[start + idx]!;
                const meta: PineconeRagRecordMeta = {
                  title: sanitizeForJsonUtf16(chunk.title),
                  path: sanitizeForJsonUtf16(chunk.pathRel),
                  source: sanitizeForJsonUtf16(chunk.sourceRelToAssets),
                  content: sanitizeForJsonUtf16(chunk.content),
                  fileHash: info.hash,
                  memoryFolder: sanitizeForJsonUtf16(mf),
                };
                return {
                  id: chunk.id,
                  values: emb,
                  metadata: meta,
                };
              });
              await index.upsert({ records });
              return records.length;
            }),
          );
          upserted += wave.reduce((a, n) => a + n, 0);
        }
      }
      nextManifestFiles[fileRel] = { hash: info.hash, ids: info.chunks.map((c) => c.id) };
      // Persist incrementally so large migrations can resume after rate-limit / transient failures.
      await saveManifest(
        opts.folderAbs,
        {
          version: 1,
          indexName,
          namespace,
          metadataVersion: PINECONE_METADATA_VERSION,
          files: nextManifestFiles,
          updatedAt: new Date().toISOString(),
        },
        opts.manifestDirAbs,
      );
      consecutiveSameErrorType = 0;
      lastErrorType = '';
    } catch (e) {
      const t = errorTypeKey(e);
      consecutiveSameErrorType = t === lastErrorType ? consecutiveSameErrorType + 1 : 1;
      lastErrorType = t;
      await appendSyncErrorReport({
        reportPath: errorReportPath,
        fileRel,
        phase: 'upsert_file',
        errorType: t,
        error: e,
      });
      const msg = e instanceof Error ? e.message : String(e);
      opts.onProgress?.(
        `[warn] skip file due to ${t} (${consecutiveSameErrorType}/${maxConsecutiveSameError} consecutive): ${fileRel} :: ${msg.slice(0, 180)}`,
      );
      if (consecutiveSameErrorType >= maxConsecutiveSameError) {
        throw new Error(
          `Aborting after ${consecutiveSameErrorType} consecutive ${t} errors. See ${errorReportPath}`,
        );
      }
      continue;
    }
  }

  // Finalize manifest with only files that exist in the current folder tree.
  const manifest: PineconeManifest = {
    version: 1,
    indexName,
    namespace,
    metadataVersion: PINECONE_METADATA_VERSION,
    files: nextManifestFiles,
    updatedAt: new Date().toISOString(),
  };
  await saveManifest(opts.folderAbs, manifest, opts.manifestDirAbs);

  opts.onProgress?.(
    `done: upserted=${upserted} deleted=${deleted} unchangedFiles=${unchangedFiles} changedFiles=${changedFiles} reconciledFromPinecone=${reconciledFromPinecone} orphanVectorsDeleted=${orphanVectorsDeleted}`,
  );

  return {
    ragRef: ragRef(indexName, namespace),
    namespace,
    indexName,
    upserted,
    deleted,
    unchangedFiles,
    changedFiles,
    reconciledFromPinecone,
    orphanVectorsDeleted,
  };
}

export async function searchPineconeRagPathSemantic(
  ragPath: string,
  query: string,
  k: number,
  opts?: PineconeSemanticSearchOpts,
): Promise<RetrievalChunk[]> {
  const pineconeApiKey = process.env.PINECONE_API_KEY?.trim();
  if (!pineconeApiKey) {
    throw new Error('PINECONE_API_KEY is required for pinecone:// retrieval');
  }
  const { indexName, namespace } = parseRagRef(ragPath);
  const pc = new Pinecone({ apiKey: pineconeApiKey });
  const q = (await embedTexts([query], { maxRetriesPerBatch: EMBED_QUERY_MAX_RETRIES }))[0]!;
  const index = pc.index(indexName).namespace(namespace);
  const foldersRaw = opts?.memoryScopeFolders?.filter((p) => p?.trim());
  const folders =
    foldersRaw && foldersRaw.length > 0 ?
      foldersRaw.map((p) => normalizeMemoryScopePath(p))
    : opts?.memoryScopeFolder?.trim() ?
      [normalizeMemoryScopePath(opts.memoryScopeFolder)]
    : [];
  const queryTopK =
    folders.length > 0 ?
      Math.min(200, Math.max(k * 12, k))
    : Math.max(1, k);
  const response = await index.query({
    vector: q,
    topK: queryTopK,
    includeMetadata: true,
  });
  const rawMatches = response.matches ?? [];
  const scopeFiltered =
    folders.length > 0 ?
      rawMatches.filter((m) => {
        const meta = (m.metadata ?? {}) as Record<string, unknown>;
        return folders.some((s) => metadataMatchesMemoryScope(s, meta));
      })
    : rawMatches;
  const limited = scopeFiltered.slice(0, Math.max(1, k));
  return limited.map((m) => {
    const meta = (m.metadata ?? {}) as Record<string, unknown>;
    const body = typeof meta.content === 'string' ? meta.content : '';
    const title = typeof meta.title === 'string' && meta.title.trim() ? meta.title : 'Retrieved chunk';
    const score = typeof m.score === 'number' ? m.score : 0;
    const similarity = Math.max(0, Math.min(1, (score + 1) / 2));
    const sourceUrl = sourceUrlFromMeta(meta, opts);
    return {
      id: randomUUID(),
      title,
      body: body || '(empty chunk)',
      score,
      tokenCount: estimateTokens(body) + estimateTokens(title),
      similarity,
      ...(sourceUrl ? { sourceUrl } : {}),
    };
  });
}
