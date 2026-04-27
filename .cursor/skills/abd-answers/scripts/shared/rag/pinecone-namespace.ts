import { createHash } from 'node:crypto';
import path from 'node:path';

export function normalizeRel(p: string): string {
  return p.split(path.sep).join('/');
}

function sha(input: string): string {
  return createHash('sha256').update(input).digest('hex');
}

function sanitizeNamespaceSegment(v: string): string {
  const s = v.toLowerCase().replace(/[^a-z0-9_-]+/g, '_').replace(/_+/g, '_').replace(/^_+|_+$/g, '');
  return s || 'root';
}

function toPineconeNamespace(memoryRootId: string | undefined, relPath: string): string {
  const base = memoryRootId ? `mr_${sanitizeNamespaceSegment(memoryRootId)}` : 'memory';
  const rel = relPath.trim();
  if (!rel) return `${base}__root`;
  const parts = normalizeRel(rel)
    .split('/')
    .filter(Boolean)
    .map((p) => sanitizeNamespaceSegment(p))
    .slice(0, 8);
  const joined = parts.join('__');
  const out = `${base}__${joined}`;
  return out.length <= 240 ? out : `${out.slice(0, 220)}__${sha(out).slice(0, 16)}`;
}

/**
 * One logical vector store per deployment: a single Pinecone namespace for all memory content.
 * Folder scope is carried in `memoryFolder` metadata and query-time filters — not separate namespaces.
 * Optional `PINECONE_NAMESPACE` overrides the derived namespace (must match query-time Pinecone ref).
 */
export function resolvePineconeNamespace(memoryRootId: string | undefined): string {
  const env = process.env.PINECONE_NAMESPACE?.trim();
  if (env) {
    return env.length <= 240 ? env : `${env.slice(0, 220)}__${sha(env).slice(0, 16)}`;
  }
  return toPineconeNamespace(memoryRootId, '');
}
