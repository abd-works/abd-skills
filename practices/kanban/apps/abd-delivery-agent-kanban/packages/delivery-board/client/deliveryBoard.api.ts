import type { KanbanBoardSnapshot } from '@deliveryforge/delivery-board-shared';

const API_BASE = import.meta.env.VITE_API_BASE ?? '';

export async function fetchBoardSnapshot(
  planningRoot: string,
  etag?: string,
): Promise<KanbanBoardSnapshot | null> {
  const headers: HeadersInit = {};
  if (etag) headers['If-None-Match'] = etag;

  const url = API_BASE + '/api/board?planningRoot=' + encodeURIComponent(planningRoot);
  const response = await fetch(url, { headers });

  if (response.status === 304) return null;
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error ?? 'Board fetch failed (' + response.status + ')');
  }
  return response.json() as Promise<KanbanBoardSnapshot>;
}

export async function updatePlanningRoot(planningRoot: string): Promise<KanbanBoardSnapshot> {
  const response = await fetch(API_BASE + '/api/board/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ planningRoot }),
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error ?? 'Config update failed');
  }
  return response.json() as Promise<KanbanBoardSnapshot>;
}

export function ticketKey(ticketId: string): string {
  return 'ticket-' + ticketId;
}
