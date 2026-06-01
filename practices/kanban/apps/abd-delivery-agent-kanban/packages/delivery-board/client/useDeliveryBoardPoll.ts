import { useCallback, useEffect, useRef, useState } from 'react';
import type { KanbanBoardSnapshot } from '@deliveryforge/delivery-board-shared';
import { fetchBoardSnapshot } from './deliveryBoard.api';

export function useDeliveryBoardPoll(planningRoot: string, intervalMs = 3000) {
  const [snapshot, setSnapshot] = useState<KanbanBoardSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const etagRef = useRef<string | undefined>();

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

  const refresh = useCallback(async () => {
    etagRef.current = undefined;
    await poll();
  }, [poll]);

  const injectSnapshot = useCallback((next: KanbanBoardSnapshot) => {
    etagRef.current = next.etag;
    setSnapshot(next);
    setError(null);
  }, []);

  return { snapshot, error, loading, refresh, injectSnapshot };
}
