/**
 * CLI: semantic search against abd-answers Pinecone (same path + embeddings as the Answers app).
 *
 * Loads env like app-server: abd-answers/.env, conf/.secrets (OPENAI + PINECONE).
 *
 * Usage (from abd-answers repo root):
 *   npm run rag:query -- "your question" --k 8
 *   npm run rag:query -- "your question" --folders "topic/a,topic/b"
 *   npm run rag:query -- "q" --memory-root-id <id>
 *   npm run rag:query -- "q" --rag-ref pinecone://my-index/my-ns
 *
 * `--folders` values are memoryFolder roots (forward slashes), OR-matched — same as chat scope in the app.
 */

import { readFileSync } from 'node:fs';
import path from 'node:path';
import {
  applyConfSecretsEnv,
  applyOpenAiKeyFromConf,
  applyPineconeFromConfSecrets,
  applyRootEnvFile,
} from '../../../scripts/shared/load-conf-openai-key.js';
import { getAbdAnswersRepoRoot, resolvePipelineRagAbs } from '../../../scripts/shared/abd-answers-paths.js';
import { deploymentPineconeRagRef } from '../../../scripts/shared/rag/pinecone-deployment-rag.js';
import { searchRagPathSemantic } from '../../../scripts/shared/rag/rag-path-semantic-search.js';

function readRagRefFromManifest(manifestPath: string): string | null {
  try {
    const raw = readFileSync(manifestPath, 'utf8');
    const m = JSON.parse(raw) as { indexName?: string; namespace?: string };
    if (typeof m?.indexName === 'string' && typeof m?.namespace === 'string' && m.indexName && m.namespace) {
      return `pinecone://${m.indexName}/${m.namespace}`;
    }
  } catch {
    /* missing */
  }
  return null;
}

function parseArgs(argv: string[]): {
  query: string;
  k: number;
  folders?: string[];
  memoryRootId?: string;
  ragRef?: string;
} {
  const rest = argv.slice(2).filter((a) => a !== '--');
  let k = 8;
  let folders: string[] | undefined;
  let memoryRootId: string | undefined;
  let ragRef: string | undefined;
  const positional: string[] = [];

  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--k' && rest[i + 1]) {
      k = Math.max(1, parseInt(rest[++i], 10) || 8);
      continue;
    }
    if (a === '--folders' && rest[i + 1]) {
      folders = rest[++i]
        .split(/[,;]/)
        .map((s) => s.trim().replace(/\\/g, '/'))
        .filter(Boolean);
      continue;
    }
    if (a === '--memory-root-id' && rest[i + 1]) {
      memoryRootId = rest[++i].trim() || undefined;
      continue;
    }
    if (a === '--rag-ref' && rest[i + 1]) {
      ragRef = rest[++i].trim() || undefined;
      continue;
    }
    if (a.startsWith('-')) {
      throw new Error(`Unknown flag: ${a}`);
    }
    positional.push(a);
  }

  const query = positional.join(' ').trim();
  if (!query) {
    throw new Error(
      'Usage: npm run rag:query -- "<query>" [--k N] [--folders "p1,p2"] [--memory-root-id id] [--rag-ref pinecone://index/ns]',
    );
  }

  return { query, k, folders, memoryRootId, ragRef };
}

async function main(): Promise<void> {
  const repo = getAbdAnswersRepoRoot();
  process.env.ABD_ANSWERS_REPO_ROOT = repo;
  applyRootEnvFile(repo);
  applyConfSecretsEnv(repo);
  applyOpenAiKeyFromConf(repo);
  applyPineconeFromConfSecrets(repo);

  const { query, k, folders, memoryRootId, ragRef: ragRefArg } = parseArgs(process.argv);

  let ragRef = ragRefArg?.trim() || '';
  if (!ragRef) {
    const manifest = path.join(resolvePipelineRagAbs(), 'pinecone-manifest.json');
    ragRef = readRagRefFromManifest(manifest) || '';
  }
  if (!ragRef) {
    ragRef = deploymentPineconeRagRef(memoryRootId);
  }
  if (!ragRef) {
    console.error(
      JSON.stringify({
        error:
          'No Pinecone RAG ref. Build RAG once (see skill) or set PINECONE_API_KEY + PINECONE_INDEX, or pass --rag-ref.',
      }),
    );
    process.exit(1);
  }

  const opts =
    folders && folders.length > 0 ?
      { memoryScopeFolders: folders }
    : {};

  const chunks = await searchRagPathSemantic(ragRef, query, k, opts);

  const out = {
    ragRef,
    query,
    k,
    folders: folders ?? null,
    memoryRootId: memoryRootId ?? null,
    chunks: chunks.map((c) => ({
      title: c.title,
      similarity: c.similarity,
      sourceUrl: c.sourceUrl,
      bodyPreview: c.body.length > 1200 ? `${c.body.slice(0, 1200)}…` : c.body,
    })),
  };

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => {
  console.error(e instanceof Error ? e.message : String(e));
  process.exit(1);
});
