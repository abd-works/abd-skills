import type { RetrievalChunk } from '../types.js';

export function estimateTokens(text: string): number {
  return Math.max(1, Math.ceil(text.length / 4));
}

/**
 * Deterministic keyword overlap ranking over in-memory chunks (not embeddings / Pinecone).
 * Excludes tombstoned chunks. Respects a rough request token budget for augmentation.
 */
export function rankChunksByKeywordOverlap(
  chunks: RetrievalChunk[],
  query: string,
  maxAugmentationTokens: number,
): RetrievalChunk[] {
  const q = query.toLowerCase().trim();
  const terms = q.length ? q.split(/\s+/).filter((t) => t.length > 1) : [];
  const active = chunks.filter((c) => !c.tombstoned);
  const scored = active.map((c) => {
    const hay = `${c.title} ${c.body}`.toLowerCase();
    let score = 0;
    for (const t of terms) {
      if (hay.includes(t)) score += 1;
    }
    if (terms.length === 0) score = 0.01;
    const similarity = Math.min(1, score / Math.max(1, terms.length || 1));
    return {
      chunk: { ...c, score, similarity },
    };
  });
  scored.sort((a, b) => b.chunk.score - a.chunk.score);
  const out: RetrievalChunk[] = [];
  let used = 0;
  for (const { chunk } of scored) {
    const cost = estimateTokens(chunk.body) + estimateTokens(chunk.title);
    if (used + cost > maxAugmentationTokens) break;
    out.push(chunk);
    used += cost;
  }
  return out;
}

/**
 * Prefer `primary` (e.g. vector hits), then add `secondary` (e.g. keyword) without duplicate bodies, until token budget.
 */
export function mergeRetrievalsWithinBudget(
  primary: RetrievalChunk[],
  secondary: RetrievalChunk[],
  maxAugmentationTokens: number,
): RetrievalChunk[] {
  const seen = new Set<string>();
  const out: RetrievalChunk[] = [];
  let used = 0;
  for (const chunk of [...primary, ...secondary]) {
    const key = chunk.body.trim().slice(0, 500);
    if (seen.has(key)) continue;
    seen.add(key);
    const cost = estimateTokens(chunk.body) + estimateTokens(chunk.title);
    if (used + cost > maxAugmentationTokens) break;
    out.push(chunk);
    used += cost;
  }
  return out;
}
