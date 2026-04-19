import type { MemoryRoot } from '@abd-answers/shared';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { deploymentPineconeRagRef } from './rag/pinecone-deployment-rag.js';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * Single on-disk pipeline tree under repo `data/assets` (`<resolveRepoDataAssetsAbs()>/<ABD_ANSWERS_PIPELINE_DIR>`).
 * The wire string `files/data/assets` is a **virtual** hub label (same disk tree as `data/assets`); see {@link normalizeRepoRelativeHubPath}.
 * Not affected by `ANSWERS_DEFAULT_HUB_PATH` (topics hub).
 */
export const ABD_ANSWERS_PIPELINE_DIR = 'abd-answers-memory-pipeline';

/**
 * Subfolders under the pipeline root — fixed layout for convert → chunk → embed/rag.
 * Must stay in sync with `scripts/source-convert/_config.py` (`PIPELINE_*_SEGMENT`).
 */
export const PIPELINE_MARKDOWN_SEGMENT = 'markdown';
export const PIPELINE_CHUNKED_SEGMENT = 'chunked';
export const PIPELINE_RAG_SEGMENT = 'rag';

/** Chat embed markdown lives under `markdown/users/...` (not loose files in `markdown/`). */
export const PIPELINE_USERS_SEGMENT = 'users';

/**
 * abd-answers git root (folder whose package.json has "name": "abd-answers").
 * Override with ABD_ANSWERS_REPO_ROOT when cwd / install layout differs.
 */
export function getAbdAnswersRepoRoot(): string {
  const env = process.env.ABD_ANSWERS_REPO_ROOT?.trim();
  if (env) return path.resolve(env);
  let dir = path.resolve(__dirname);
  for (let i = 0; i < 14; i++) {
    const pkg = path.join(dir, 'package.json');
    if (existsSync(pkg)) {
      try {
        const j = JSON.parse(readFileSync(pkg, 'utf8')) as { name?: string };
        if (j.name === 'abd-answers') return dir;
      } catch {
        /* ignore */
      }
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return path.resolve(process.cwd());
}

/**
 * Configured “hub” path used when code needs a single configured root (often same as source root in dev).
 * - `ANSWERS_DEFAULT_HUB_PATH` → that directory
 * - Else repo `data/assets` (dev)
 */
export function resolveConfiguredHubRootAbs(): string {
  const env = process.env.ANSWERS_DEFAULT_HUB_PATH?.trim();
  if (env) {
    const abs = path.resolve(env);
    if (existsSync(abs)) return abs;
  }
  return path.join(getAbdAnswersRepoRoot(), 'data', 'assets');
}

/**
 * Root directory for Source panel API (browse / upload under virtual `/assets/...`).
 * With `ANSWERS_DEFAULT_HUB_PATH`, uses `<hub>/assets` when that folder exists; otherwise the hub root.
 * Repo dev: `data/assets` (topics live directly here).
 */
export function resolveSourceFilesRootAbs(): string {
  const env = process.env.ANSWERS_DEFAULT_HUB_PATH?.trim();
  if (env) {
    const hub = path.resolve(env);
    if (existsSync(hub)) {
      const junction = path.join(hub, 'assets');
      if (existsSync(junction)) return junction;
      return hub;
    }
  }
  return path.join(getAbdAnswersRepoRoot(), 'data', 'assets');
}

/**
 * Source tree root for a known hub directory (same rules as {@link resolveSourceFilesRootAbs} when the hub exists):
 * prefer `<hub>/assets` when that folder exists, else `hub`.
 */
export function resolveSourceFilesRootForHubAbs(hubAbs: string): string {
  const hub = path.resolve(hubAbs);
  const junction = path.join(hub, 'assets');
  if (existsSync(junction)) return junction;
  return hub;
}

/** Repo-relative path for a new default memory root (canonical on-disk tree under repo `data/assets`). */
export function defaultDevHubRelativePath(): string {
  return 'data/assets';
}

/**
 * Repo `data/assets` — pipeline tree (markdown, chunked, rag). Not the same as {@link resolveSourceFilesRootAbs}
 * when `ANSWERS_DEFAULT_HUB_PATH` points elsewhere.
 */
export function resolveRepoDataAssetsAbs(): string {
  return path.join(getAbdAnswersRepoRoot(), 'data', 'assets');
}

/** Pipeline root: `<resolveRepoDataAssetsAbs()>/<ABD_ANSWERS_PIPELINE_DIR>` — markdown, chunked, rag subfolders only. */
export function resolvePipelineRootAbs(): string {
  return path.join(resolveRepoDataAssetsAbs(), ABD_ANSWERS_PIPELINE_DIR);
}

export function resolvePipelineMarkdownAbs(): string {
  return path.join(resolvePipelineRootAbs(), PIPELINE_MARKDOWN_SEGMENT);
}

const CHAT_SPACE_SEGMENT_MAX = 120;

/**
 * Single path segment for chat-space folder or chat name under `users/...`.
 */
export function sanitizeChatSpacePathSegment(name: string): string {
  const s = name
    .trim()
    .replace(/[/\\]+/g, '-')
    .replace(/[^a-zA-Z0-9 _.-]+/g, '_')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, CHAT_SPACE_SEGMENT_MAX);
  return s || 'untitled';
}

/**
 * Absolute directory for embedded chat markdown:
 * `<pipeline>/markdown/users/<userKeySanitized>/<...folderAndChatSegments>`.
 */
export function resolveUserEmbeddingsDirectoryAbs(
  userKeySanitized: string,
  folderAndChatSegments: string[],
): string {
  const segs = folderAndChatSegments.map(sanitizeChatSpacePathSegment).filter(Boolean);
  return path.join(resolvePipelineMarkdownAbs(), PIPELINE_USERS_SEGMENT, userKeySanitized, ...segs);
}

export function resolvePipelineChunkedAbs(): string {
  return path.join(resolvePipelineRootAbs(), PIPELINE_CHUNKED_SEGMENT);
}

export function resolvePipelineRagAbs(): string {
  return path.join(resolvePipelineRootAbs(), PIPELINE_RAG_SEGMENT);
}

/**
 * Repo-relative hub strings may use a virtual `files/` prefix (same meaning as “local” / API `files` routes — not a disk folder under the repo).
 * Strip it before joining to the repo root so `files/data/assets` → `data/assets`.
 */
export function normalizeRepoRelativeHubPath(repoRelative: string): string {
  const s = repoRelative.trim().replace(/\\/g, '/').replace(/^\/+/, '');
  return s.replace(/^files\//i, '');
}

export function resolveLocalHubAbsolute(hubRaw: string): string {
  const t = hubRaw.trim();
  if (!t) return '';
  if (path.isAbsolute(t)) return path.normalize(t);
  const normalized = normalizeRepoRelativeHubPath(t);
  return path.normalize(path.join(getAbdAnswersRepoRoot(), normalized));
}

/**
 * Effective Pinecone URI for chat: **deployment** env (`PINECONE_API_KEY`, `PINECONE_INDEX`,
 * optional `PINECONE_NAMESPACE`) and memory-root id — not stored on hubs.
 */
export function resolveMemoryRootVectorRagRef(
  root: MemoryRoot | undefined,
  _ragDiskEnvFallback?: string,
): string {
  if (!root) return '';
  return deploymentPineconeRagRef(root.id);
}

/** @deprecated Use {@link resolveMemoryRootVectorRagRef}. */
export const resolveMemoryRootRagPathForDisk = resolveMemoryRootVectorRagRef;

export function isPathInsideParent(fileAbs: string, parentAbs: string): boolean {
  const f = path.resolve(fileAbs);
  const p = path.resolve(parentAbs);
  const rel = path.relative(p, f);
  return rel !== '' && !rel.startsWith('..') && !path.isAbsolute(rel);
}

/**
 * Same-origin URL path for a file under the served source tree (static /files/source).
 * Prefer {@link sourceRelToFilesDownloadUrl} for links that must match the content hub
 * download endpoint.
 * `urlPrefix` is typically `/api/answers/files/source`.
 */
export function sourceFileToDownloadUrlPath(
  fileAbs: string,
  sourceRootAbs: string,
  urlPrefix: string,
): string | undefined {
  if (!isPathInsideParent(fileAbs, sourceRootAbs)) return undefined;
  const rel = path.relative(path.resolve(sourceRootAbs), path.resolve(fileAbs));
  const relPosix = rel.split(path.sep).join('/');
  const parts = relPosix.split('/').filter(Boolean).map((seg) => encodeURIComponent(seg));
  const base = urlPrefix.replace(/\/+$/, '');
  return `${base}/${parts.join('/')}`;
}

/**
 * `/api/answers/files/download?...` URL for a file under the hub assets root — same resolution
 * as the content hub (not static `/files/source/`, which can 404 or bypass virtual path rules).
 * `apiAnswersPrefix` is typically `/api/answers` (strip `/files/source` from `sourceUrlPathPrefix`).
 */
export function sourceRelToFilesDownloadUrl(
  fileAbs: string,
  sourceRootAbs: string,
  apiAnswersPrefix: string,
): string | undefined {
  if (!isPathInsideParent(fileAbs, sourceRootAbs)) return undefined;
  const rel = path.relative(path.resolve(sourceRootAbs), path.resolve(fileAbs));
  const relPosix = rel.split(path.sep).join('/');
  const base = apiAnswersPrefix.replace(/\/+$/, '');
  const q = new URLSearchParams({ scope: 'assets', path: relPosix });
  return `${base}/files/download?${q.toString()}`;
}
