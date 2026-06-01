import type { KanbanBoardSnapshot, StageId } from '@deliveryforge/delivery-board-shared';

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

export async function toggleBoardMode(planningRoot: string): Promise<KanbanBoardSnapshot> {
  const res = await fetch(API_BASE + '/api/board/mode', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ planningRoot }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error ?? 'Mode toggle failed');
  }
  return res.json() as Promise<KanbanBoardSnapshot>;
}

export async function postResumeTicketInProgress(
  planningRoot: string,
  ticketId: string,
): Promise<KanbanBoardSnapshot> {
  return postMoveTicketToStage(planningRoot, ticketId, null);
}

export type MoveTicketPlacement = 'in_progress' | 'stage_done';

export async function postMoveTicketToStage(
  planningRoot: string,
  ticketId: string,
  targetStage: StageId | null,
  placement: MoveTicketPlacement = 'in_progress',
): Promise<KanbanBoardSnapshot> {
  const url =
    targetStage === null
      ? API_BASE + '/api/board/ticket/resume-in-progress'
      : API_BASE + '/api/board/ticket/move-to-stage';
  const body =
    targetStage === null
      ? { planningRoot, ticket_id: ticketId }
      : {
          planningRoot,
          ticket_id: ticketId,
          target_stage: targetStage,
          placement,
        };
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const payload = await res.json().catch(() => ({}));
    throw new Error(payload.error ?? 'Move ticket failed');
  }
  return res.json() as Promise<KanbanBoardSnapshot>;
}

export type LeadScanResult = {
  must_spawn?: boolean;
  spawns?: Array<{ role: string; instance: number }>;
  actions?: string[];
};

export async function postActionIntent(
  planningRoot: string,
  ticketId: string,
  skill: string,
  agentRole: string,
): Promise<{ ok: boolean; lead_scan: LeadScanResult | null }> {
  const res = await fetch(API_BASE + '/api/board/action-intent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ planningRoot, ticket_id: ticketId, skill, agent_role: agentRole }),
  });
  if (!res.ok) {
    const payload = await res.json().catch(() => ({}));
    throw new Error((payload as { error?: string }).error ?? 'Action intent failed');
  }
  return res.json() as Promise<{ ok: boolean; lead_scan: LeadScanResult | null }>;
}

export async function postLeadScan(planningRoot: string): Promise<LeadScanResult> {
  const res = await fetch(API_BASE + '/api/board/lead-scan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ planningRoot }),
  });
  if (!res.ok) {
    const payload = await res.json().catch(() => ({}));
    throw new Error((payload as { error?: string }).error ?? 'Lead scan failed');
  }
  return res.json() as Promise<LeadScanResult>;
}

export function ticketKey(ticketId: string): string {
  return 'ticket-' + ticketId;
}
