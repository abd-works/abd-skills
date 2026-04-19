/**
 * Strip BOM, zero-width, and line breaks often introduced when pasting keys into `.secrets`.
 */
export function sanitizeOpenAiApiKeySecret(secret: string): string {
  let s = secret.replace(/^\uFEFF/, '');
  s = s.replace(/[\u200B-\u200D\uFEFF]/g, '');
  s = s.replace(/\r\n/g, '\n').replace(/\r/g, '');
  s = s.replace(/\n/g, '').trim();
  return s;
}

/**
 * JSON POST headers for OpenAI: Bearer key plus optional org/project (see conf/.secrets.example).
 */
export function openAiJsonRequestHeaders(apiKey: string): Record<string, string> {
  const key = sanitizeOpenAiApiKeySecret(apiKey);
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${key}`,
  };
  const org =
    process.env.OPENAI_ORGANIZATION?.trim() ||
    process.env.OPENAI_ORG_ID?.trim() ||
    process.env.OPENAI_ORGANIZATION_ID?.trim();
  const project = process.env.OPENAI_PROJECT_ID?.trim();
  if (org) headers['OpenAI-Organization'] = org;
  if (project) headers['OpenAI-Project'] = project;
  return headers;
}

/**
 * Primary OpenAI key plus optional fallbacks (set in env or conf/.secrets).
 */
export function getOpenAiApiKeyCandidates(): string[] {
  const raw = [
    process.env.OPENAI_API_KEY?.trim(),
    process.env.OPEN_API_KEY_2?.trim(),
    process.env.OPENAI_API_KEY_2?.trim(),
  ]
    .filter((k): k is string => Boolean(k))
    .map((k) => sanitizeOpenAiApiKeySecret(k));
  const seen = new Set<string>();
  const out: string[] = [];
  for (const k of raw) {
    if (!k || seen.has(k)) continue;
    seen.add(k);
    out.push(k);
  }
  return out;
}

export function firstOpenAiApiKey(): string | undefined {
  return getOpenAiApiKeyCandidates()[0];
}

export function parseOpenAiChatHttpStatusFromMessage(message: string): number | undefined {
  const m = message.match(/OpenAI error (\d{3})/);
  return m ? Number(m[1]) : undefined;
}

export function parseOpenAiEmbeddingsHttpStatusFromMessage(message: string): number | undefined {
  const m = message.match(/OpenAI embeddings (\d{3})/);
  return m ? Number(m[1]) : undefined;
}

export function shouldRetryOpenAiWithDifferentKey(err: Error): boolean {
  const msg = err.message;
  if (msg.includes('OpenAI returned an empty assistant message')) return false;
  if (msg.includes('OpenAI stream ended with empty assistant message')) return false;
  const s =
    parseOpenAiChatHttpStatusFromMessage(msg) ?? parseOpenAiEmbeddingsHttpStatusFromMessage(msg);
  if (s !== undefined) {
    if (s === 400) {
      if (/invalid model|model.*not found|does not exist|unknown model/i.test(msg)) return false;
      return true;
    }
    return s === 401 || s === 402 || s === 403 || s === 429 || (s >= 500 && s <= 599);
  }
  return true;
}
