import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';

/** Same line format as orchestrator / `conf/README.md`: KEY=value, # comments. */
function parseDotEnvStyle(content: string): Record<string, string> {
  const raw = content.startsWith('\ufeff') ? content.slice(1) : content;
  const out: Record<string, string> = {};
  for (const line of raw.split(/\r?\n/)) {
    let t = line.trim();
    if (!t || t.startsWith('#')) continue;
    if (t.toLowerCase().startsWith('export ')) {
      t = t.slice(7).trim();
    }
    const eq = t.indexOf('=');
    if (eq <= 0) continue;
    const key = t.slice(0, eq).trim();
    let val = t.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    out[key] = val;
  }
  return out;
}

/**
 * Load `abd-answers/.env` into `process.env` for keys not already set.
 * Enables PORT and other keys without a separate dotenv package.
 */
export function applyRootEnvFile(abdAnswersRoot: string): void {
  const envPath = path.join(abdAnswersRoot, '.env');
  if (!existsSync(envPath)) return;
  try {
    const map = parseDotEnvStyle(readFileSync(envPath, 'utf8'));
    for (const [k, v] of Object.entries(map)) {
      if (process.env[k] === undefined && v !== '') process.env[k] = v;
    }
  } catch {
    // ignore malformed .env
  }
}

/**
 * Load `conf/answers-memory.env` (optional, gitignored) for local hub defaults.
 * Same KEY=value format as `.env`. Does not override keys already set in the environment or root `.env`.
 */
export function applyConfMemoryEnv(abdAnswersRoot: string): { loadedFrom?: string } {
  const p = path.join(abdAnswersRoot, 'conf', 'answers-memory.env');
  if (!existsSync(p)) return {};
  try {
    const map = parseDotEnvStyle(readFileSync(p, 'utf8'));
    for (const [k, v] of Object.entries(map)) {
      if (process.env[k] === undefined && v !== '') process.env[k] = v;
    }
    return { loadedFrom: path.join('conf', 'answers-memory.env') };
  } catch {
    return {};
  }
}

function uniqueResolvedRoots(candidates: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const c of candidates) {
    const r = path.resolve(c);
    if (seen.has(r)) continue;
    seen.add(r);
    out.push(r);
  }
  return out;
}

/** Pinecone client + index + optional namespace — must match server, RAG, and CLI scripts. */
const PINECONE_ENV_KEYS = ['PINECONE_API_KEY', 'PINECONE_INDEX', 'PINECONE_NAMESPACE'] as const;

/**
 * After `applyRootEnvFile` / `applyConfMemoryEnv` / `applyConfSecretsEnv`, overwrite `PINECONE_*`
 * from `conf/secrets` then `conf/.secrets` at each candidate root (same roots as `applyConfSecretsEnv`).
 * **`abdAnswersRoot` is applied last** so this repo’s `conf/.secrets` wins over parent `cwd` copies.
 * Values overwrite root `.env` and earlier partial loads.
 */
export function applyPineconeFromConfSecrets(abdAnswersRoot: string): {
  loadedFrom?: string[];
} {
  const envRoot = process.env.ABD_ANSWERS_ROOT?.trim();
  const resolvedEnvRoot = envRoot ? path.resolve(envRoot) : undefined;
  const roots = uniqueResolvedRoots([
    process.cwd(),
    path.resolve(process.cwd(), '..'),
    path.resolve(process.cwd(), '../..'),
    ...(resolvedEnvRoot ? [resolvedEnvRoot] : []),
    path.resolve(abdAnswersRoot),
  ]);

  const appliedFiles: string[] = [];
  for (const root of roots) {
    for (const name of ['secrets', '.secrets'] as const) {
      const secretsPath = path.join(root, 'conf', name);
      if (!existsSync(secretsPath)) continue;
      try {
        const map = parseDotEnvStyle(readFileSync(secretsPath, 'utf8'));
        let applied = false;
        for (const key of PINECONE_ENV_KEYS) {
          const v = map[key]?.trim();
          if (v) {
            process.env[key] = v;
            applied = true;
          }
        }
        if (applied) appliedFiles.push(path.join(root, 'conf', name));
      } catch {
        /* ignore malformed file */
      }
    }
  }
  return { loadedFrom: appliedFiles.length ? [...new Set(appliedFiles)] : undefined };
}

/**
 * Load all env vars from `conf/.secrets` or `conf/secrets` under candidate roots.
 * Existing process env vars are not overwritten.
 */

export function applyConfSecretsEnv(
  abdAnswersRoot: string,
): { loadedFrom?: string; checkedFiles?: string[] } {
  const envRoot = process.env.ABD_ANSWERS_ROOT?.trim();
  const resolvedEnvRoot = envRoot ? path.resolve(envRoot) : undefined;

  const roots = uniqueResolvedRoots([
    ...(resolvedEnvRoot ? [resolvedEnvRoot] : []),
    abdAnswersRoot,
    process.cwd(),
    path.resolve(process.cwd(), '..'),
    path.resolve(process.cwd(), '../..'),
  ]);

  const checkedFiles: string[] = [];
  for (const root of roots) {
    for (const name of ['.secrets', 'secrets'] as const) {
      const secretsPath = path.join(root, 'conf', name);
      if (!existsSync(secretsPath)) {
        checkedFiles.push(secretsPath);
        continue;
      }
      checkedFiles.push(secretsPath);
      try {
        const map = parseDotEnvStyle(readFileSync(secretsPath, 'utf8'));
        let loadedAny = false;
        for (const [k, v] of Object.entries(map)) {
          if (!k || !v || process.env[k] !== undefined) continue;
          process.env[k] = v;
          loadedAny = true;
        }
        if (loadedAny) {
          return { loadedFrom: path.join('conf', name), checkedFiles };
        }
      } catch {
        // try next file
      }
    }
  }
  return { checkedFiles };
}

/** Env vars that `getOpenAiApiKeyCandidates()` reads (see `packages/answers/server/src/rag/openai-keys.ts`). */
const OPENAI_KEY_ENV_NAMES = ['OPENAI_API_KEY', 'OPEN_API_KEY_2', 'OPENAI_API_KEY_2'] as const;

/**
 * After `conf/.secrets` / `applyOpenAiKeyFromConf` may inject keys, E2E runs with
 * `ANSWERS_TEST_MODE=1` and `ANSWERS_SYNTHETIC_CHAT=1` — delete those keys so no outbound
 * OpenAI (chat, embeddings) or RAG paths that depend on `hasOpenAiKey` can run.
 */
export function stripOpenAiKeysForSyntheticTestMode(): void {
  if (process.env.ANSWERS_TEST_MODE !== '1' || process.env.ANSWERS_SYNTHETIC_CHAT !== '1') {
    return;
  }
  for (const k of OPENAI_KEY_ENV_NAMES) {
    if (process.env[k]) delete process.env[k];
  }
}

export function isSyntheticTestModeNoOpenAi(): boolean {
  return process.env.ANSWERS_TEST_MODE === '1' && process.env.ANSWERS_SYNTHETIC_CHAT === '1';
}

/**
 * If OPENAI_API_KEY is not already set, try `conf/.secrets` then `conf/secrets`
 * under candidate repo roots (package-relative path, then cwd fallbacks).
 * Set ABD_ANSWERS_ROOT to the abd-answers repo root if auto-detection misses conf/.secrets.
 */
export function applyOpenAiKeyFromConf(abdAnswersRoot: string): { loadedFrom?: string; checkedFiles?: string[] } {
  if (process.env.OPENAI_API_KEY?.trim()) {
    return {};
  }

  const envRoot = process.env.ABD_ANSWERS_ROOT?.trim();
  const resolvedEnvRoot = envRoot ? path.resolve(envRoot) : undefined;

  const roots = uniqueResolvedRoots([
    ...(resolvedEnvRoot ? [resolvedEnvRoot] : []),
    abdAnswersRoot,
    process.cwd(),
    path.resolve(process.cwd(), '..'),
    path.resolve(process.cwd(), '../..'),
  ]);

  const checkedFiles: string[] = [];

  for (const root of roots) {
    for (const name of ['.secrets', 'secrets'] as const) {
      const secretsPath = path.join(root, 'conf', name);
      if (!existsSync(secretsPath)) {
        checkedFiles.push(secretsPath);
        continue;
      }
      checkedFiles.push(secretsPath);
      try {
        const map = parseDotEnvStyle(readFileSync(secretsPath, 'utf8'));
        const key = map.OPENAI_API_KEY?.trim() || map.openai_api_key?.trim();
        if (key) {
          process.env.OPENAI_API_KEY = key;
          return { loadedFrom: path.join('conf', name), checkedFiles };
        }
      } catch {
        // try next file
      }
    }
  }
  return { checkedFiles };
}
