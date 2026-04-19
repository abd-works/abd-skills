import { resolvePineconeNamespace } from './pinecone-namespace.js';

/**
 * Effective Pinecone URI for chat/API from deployment env (`PINECONE_API_KEY` + `PINECONE_INDEX`)
 * and namespace rules shared with Build RAG / sync. Hubs do not store a vector ref.
 */
export function deploymentPineconeRagRef(memoryRootId: string | undefined): string {
  const apiKey = process.env.PINECONE_API_KEY?.trim();
  const index = process.env.PINECONE_INDEX?.trim();
  if (!apiKey || !index) return '';
  const ns = resolvePineconeNamespace(memoryRootId);
  return `pinecone://${index}/${ns}`;
}
