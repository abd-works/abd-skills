/**
 * domainName.api.ts — API client (fetch wrapper).
 *
 * Provides typed functions for calling the backend REST API.
 * Imports types from shared/ for compile-time contract safety.
 *
 * IMPORTANT: This file must export a function for EVERY route defined
 * in the server's routes file. If the server exposes POST/PUT endpoints,
 * this file must have corresponding create/update functions so the client
 * tier can call them from forms and detail views.
 */
import { DomainName } from '@appName/domainName-shared';

const API_BASE = '/api/domainNames';

export async function fetchDomainNames(
  filters?: { activeOnly?: boolean }
): Promise<DomainName[]> {
  const params = new URLSearchParams();
  if (filters?.activeOnly) params.set('activeOnly', 'true');
  const response = await fetch(`${API_BASE}?${params}`);
  const data = await response.json();
  return data.items;
}

export async function fetchDomainNameById(id: string): Promise<DomainName> {
  const response = await fetch(`${API_BASE}/${id}`);
  return response.json();
}

export async function createDomainName(
  input: Record<string, unknown>
): Promise<DomainName> {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  return response.json();
}
