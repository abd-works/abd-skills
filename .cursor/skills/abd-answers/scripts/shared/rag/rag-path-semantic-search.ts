import type { RetrievalChunk } from '../types.js';
import { getOpenAiApiKeyCandidates } from './openai-keys.js';
import { isPineconeRagRef, searchPineconeRagPathSemantic } from './pinecone-rag.js';

export type RagSemanticSearchOpts = {
  /** Absolute root of served source tree (repo `data/assets` topics hub; may follow `ANSWERS_DEFAULT_HUB_PATH`). */
  sourceFilesRootAbs?: string;
  /** e.g. `/api/answers/files/source` for same-origin download links in the browser. */
  sourceUrlPathPrefix?: string;
  /** When set, Pinecone hits are limited to chunks under this memory folder path (see `memoryFolder` metadata). */
  memoryScopeFolder?: string;
  /** OR of folder roots; preferred over `memoryScopeFolder` when non-empty. */
  memoryScopeFolders?: string[];
};

/**
 * Semantic top-k for chat retrieval. Vector search uses Pinecone only (`pinecone://<index>/<namespace>`).
 * Uses OPENAI_API_KEY for query embeddings, with OPEN_API_KEY_2 / OPENAI_API_KEY_2 as fallbacks.
 */
export async function searchRagPathSemantic(
  ragPath: string | undefined,
  query: string,
  k: number,
  opts?: RagSemanticSearchOpts,
): Promise<RetrievalChunk[]> {
  if (!ragPath?.trim() || !query.trim() || getOpenAiApiKeyCandidates().length === 0) return [];
  if (isPineconeRagRef(ragPath)) {
    return searchPineconeRagPathSemantic(ragPath, query, k, opts);
  }
  return [];
}

/** Default cap so chat UI does not sit on "Retrieving context…" while embeddings/Pinecone run unbounded. */
const DEFAULT_CHAT_RAG_TIMEOUT_MS = 15_000;

function chatRagTimeoutMs(): number {
  const raw = process.env.ANSWERS_CHAT_RAG_TIMEOUT_MS?.trim();
  if (!raw) return DEFAULT_CHAT_RAG_TIMEOUT_MS;
  const n = Number(raw);
  return Number.isFinite(n) && n > 0 ? n : DEFAULT_CHAT_RAG_TIMEOUT_MS;
}

/**
 * Same as {@link searchRagPathSemantic} but rejects after a timeout so the chat handler can fall back
 * to keyword-only retrieval. Does not cancel in-flight HTTP (work may finish in the background).
 * Set `ANSWERS_CHAT_RAG_TIMEOUT_MS` (default 15000).
 */
export async function searchRagPathSemanticForChat(
  ragPath: string | undefined,
  query: string,
  k: number,
  opts?: RagSemanticSearchOpts,
): Promise<RetrievalChunk[]> {
  const ms = chatRagTimeoutMs();
  return await Promise.race([
    searchRagPathSemantic(ragPath, query, k, opts),
    new Promise<never>((_, reject) => {
      setTimeout(() => {
        reject(new Error(`Memory search timed out after ${ms}ms`));
      }, ms);
    }),
  ]);
}
