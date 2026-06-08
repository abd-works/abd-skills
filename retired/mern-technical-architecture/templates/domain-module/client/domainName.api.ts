/**
 * domainName.api.ts — API client (fetch wrapper).
 *
 * Function names match the domain verb exactly:
 *   listDomainNames, getDomainName, createDomainName
 *
 * Arg names match the domain model — only the type narrows (object → ID string).
 * JSON bodies use snake_case; TypeScript uses camelCase.
 *
 * Every function returns the same aggregate snapshot type so the client
 * can replace its state atomically after any mutation.
 */
import { DomainName, DomainNameSnapshot } from '@appName/domainName-shared';

const API_BASE = '/api/domainNames';

export async function listDomainNames(
  filters?: { activeOnly?: boolean }
): Promise<DomainNameSnapshot> {
  const params = new URLSearchParams();
  if (filters?.activeOnly) params.set('active_only', 'true');
  const response = await fetch(`${API_BASE}?${params}`);
  return response.json();
}

export async function getDomainName(domainName: string): Promise<DomainNameSnapshot> {
  const response = await fetch(`${API_BASE}/${domainName}`);
  return response.json();
}

export async function createDomainName(
  input: Record<string, unknown>
): Promise<DomainNameSnapshot> {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  return response.json();
}
