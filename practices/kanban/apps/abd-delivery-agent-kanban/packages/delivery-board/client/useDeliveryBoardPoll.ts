import { useCallback, useEffect, useRef, useState } from 'react';
import type { KanbanBoardSnapshot } from '@deliveryforge/delivery-board-shared';
import { fetchBoardSnapshot } from './deliveryBoard.api';

function ticketPosition(snapshot: KanbanBoardSnapshot, ticketId: string): string {
  for (const col of snapshot.columnViews) {
    const ticket = col.tickets.find((t) => t.ticketId === ticketId);
    if (ticket) {
      return col.id + ':' + (ticket.stage ?? '') + ':' + (ticket.activeSkillId ?? '');
    }
  }
  const archived = snapshot.archivedTickets.find((t) => t.ticketId === ticketId);
  if (archived) return 'archived';
  return 'unknown';
}

export function useDeliveryBoardPoll(planningRoot: string, intervalMs = 3000) {
  const [snapshot, setSnapshot] = useState<KanbanBoardSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const etagRef = useRef<string | undefined>();
  const prevPositionsRef = useRef<Map<string, string>>(new Map());

  const poll = useCallback(async () => {
    if (!planningRoot) return;
    try {
      const next = await fetchBoardSnapshot(planningRoot, etagRef.current);
      if (next) {
        etagRef.current = next.etag;
        setSnapshot(next);
        setError(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Poll failed');
    } finally {
      setLoading(false);
    }
  }, [planningRoot]);

  useEffect(() => {
    setLoading(true);
    etagRef.current = undefined;
    void poll();
    const id = window.setInterval(() => void poll(), intervalMs);
    return () => window.clearInterval(id);
  }, [poll, intervalMs]);

  const movedTickets = new Set<string>();
  if (snapshot) {
    const allIds = new Set<string>();
    for (const col of snapshot.columnViews) {
      for (const t of col.tickets) allIds.add(t.ticketId);
    }
    for (const t of snapshot.archivedTickets) allIds.add(t.ticketId);

    for (const ticketId of allIds) {
      const key = 'ticket-' + ticketId;
      const pos = ticketPosition(snapshot, ticketId);
      const prev = prevPositionsRef.current.get(key);
      if (prev && prev !== pos) movedTickets.add(key);
      prevPositionsRef.current.set(key, pos);
    }
  }

  const refresh = useCallback(async () => {
    etagRef.current = undefined;
    await poll();
  }, [poll]);

  const injectSnapshot = useCallback((next: KanbanBoardSnapshot) => {
    etagRef.current = next.etag;
    setSnapshot(next);
    setError(null);
  }, []);

  return { snapshot, error, loading, movedTickets, refresh, injectSnapshot };
}
