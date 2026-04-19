/**
 * Local type definitions extracted from @abd-answers/shared so the skill tree
 * can run standalone without the abd-answers monorepo workspace package.
 */

export type MemoryRoot = {
  id: string;
  path: string;
  label: string;
  junctionsDir?: string;
  diskHubPath?: string;
  instructions?: string;
};

export type RetrievalChunk = {
  id: string;
  title: string;
  body: string;
  score: number;
  tokenCount: number;
  similarity: number;
  sourceUrl?: string;
  tombstoned?: boolean;
};
