/**
 * domainName.api.ts — API client (fetch wrapper).
 *
 * Provides typed functions for calling the backend REST API.
 * Imports types from shared/ for compile-time contract safety.
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
