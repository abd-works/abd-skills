import {
  useCallback, useEffect, useLayoutEffect, useRef, useState,
  type RefObject,
} from 'react';
import {
  KanbanBoard as DomainKanbanBoard,
  parseKanbanBoard,
  type KanbanBoardData,
  type KanbanBoardSnapshot,
  type KanbanColumnView,
} from '@deliveryforge/kanban-shared';
import { Ticket } from './Ticket';

const API_BASE: string = (import.meta as unknown as { env: Record<string, string> }).env.VITE_API_BASE ?? '';
const PLANNING_ROOT_OVERRIDE_KEY = 'planningRootOverride';
const FLIP_DURATION_MS = 680;
const FLIP_EASING = 'cubic-bezier(0.16, 1, 0.3, 1)';
const MIN_DELTA_PX = 0.75;

/**
 * Presentation-layer KanbanBoard — extends domain aggregate.
 * Owns: column view hydration, snapshot polling, FLIP animation,
 * planning-root configuration, snapshot hydration, and board HTTP API calls.
 */
export class KanbanBoard extends DomainKanbanBoard {
  constructor(data: KanbanBoardData) {
    super(data);
  }

  static parse(raw: unknown): KanbanBoard {
    return new KanbanBoard(parseKanbanBoard(raw));
  }

  override columnViews(): KanbanColumnView[] {
    return super.columnViews().map((col) => ({
      ...col,
      tickets: col.tickets.map((t) => Ticket.fromDomain(t)),
    }));
  }

  override archivedTickets(): Ticket[] {
    return super.archivedTickets().map((t) => Ticket.fromDomain(t));
  }

  // ── Planning root configuration ──────────────────────────────────────────

  static readonly DEFAULT_PLANNING_ROOT: string =
    (import.meta as unknown as { env: Record<string, string> }).env.VITE_PLANNING_ROOT ??
    'C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning';

  /** User-set override from the Connect form (stored in localStorage). */
  static readPlanningRootOverride(): string | null {
    return localStorage.getItem(PLANNING_ROOT_OVERRIDE_KEY);
  }

  static savePlanningRootOverride(root: string): void {
    localStorage.setItem(PLANNING_ROOT_OVERRIDE_KEY, root);
  }

  /** Resolve the active planning root: env var → localStorage override → default. */
  static resolvePlanningRoot(): string {
    const env = (import.meta as unknown as { env: Record<string, string> }).env;
    if (env.VITE_PLANNING_ROOT) return env.VITE_PLANNING_ROOT;
    return KanbanBoard.readPlanningRootOverride() ?? KanbanBoard.DEFAULT_PLANNING_ROOT;
  }

  // ── Snapshot hydration ────────────────────────────────────────────────────

  /**
   * Rebuild a wire snapshot (plain objects from JSON) so the board and tickets
   * are proper class instances with domain methods available in the UI.
   */
  static fromSnapshot(json: KanbanBoardSnapshot): KanbanBoardSnapshot {
    const boardData =
      json.board instanceof DomainKanbanBoard
        ? json.board.toJSON()
        : parseKanbanBoard(json.board as unknown);

    const board = new KanbanBoard(boardData);
    return {
      ...json,
      board,
      columnViews: board.columnViews(),
      archivedTickets: board.archivedTickets(),
    };
  }

  // ── Board HTTP API ────────────────────────────────────────────────────────

  /** GET /api/board with ETag; returns null when server responds 304 (not modified). */
  static async fetchSnapshot(
    etag?: string,
  ): Promise<KanbanBoardSnapshot | null> {
    const planningRoot = KanbanBoard.resolvePlanningRoot();
    const headers: HeadersInit = {};
    if (etag) headers['If-None-Match'] = etag;
    const url = API_BASE + '/api/board?planningRoot=' + encodeURIComponent(planningRoot);
    const response = await fetch(url, { headers });
    if (response.status === 304) return null;
    if (!response.ok) {
      const body = await response.json().catch(() => ({})) as { error?: string };
      throw new Error(body.error ?? 'Board fetch failed (' + response.status + ')');
    }
    return KanbanBoard.fromSnapshot((await response.json()) as KanbanBoardSnapshot);
  }

  /** GET /api/board/config — returns the server's current planning root. */
  static async fetchConfig(): Promise<string> {
    const response = await fetch(API_BASE + '/api/board/config');
    if (!response.ok) throw new Error('Failed to read server planning root');
    const body = (await response.json()) as { planningRoot?: string };
    return body.planningRoot ?? '';
  }

  /** POST /api/board/config — set a new planning root on the server. */
  static async updateConfig(planningRoot: string): Promise<KanbanBoardSnapshot> {
    const response = await fetch(API_BASE + '/api/board/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ planningRoot }),
    });
    if (!response.ok) {
      const body = await response.json().catch(() => ({})) as { error?: string };
      throw new Error(body.error ?? 'Config update failed');
    }
    return KanbanBoard.fromSnapshot((await response.json()) as KanbanBoardSnapshot);
  }

  /** POST /api/board/mode — toggle between automatic and manual board mode. */
  static async toggleMode(): Promise<KanbanBoardSnapshot> {
    const planningRoot = KanbanBoard.resolvePlanningRoot();
    const res = await fetch(API_BASE + '/api/board/mode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ planningRoot }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({})) as { error?: string };
      throw new Error(body.error ?? 'Mode toggle failed');
    }
    return KanbanBoard.fromSnapshot((await res.json()) as KanbanBoardSnapshot);
  }

  // ── Snapshot polling ──────────────────────────────────────────────────────

  /**
   * React hook — poll the server for snapshot updates on an interval.
   * Uses ETag-based conditional fetching; only updates state when the board changes.
   */
  static usePoll(intervalMs = 3000): {
    snapshot: KanbanBoardSnapshot | null;
    error: string | null;
    loading: boolean;
    refresh: () => Promise<void>;
    injectSnapshot: (next: KanbanBoardSnapshot) => void;
  } {
    const [snapshot, setSnapshot] = useState<KanbanBoardSnapshot | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const etagRef = useRef<string | undefined>();

    const poll = useCallback(async () => {
      try {
        const next = await KanbanBoard.fetchSnapshot(etagRef.current);
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
    }, []);

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

  // ── FLIP ticket animation ─────────────────────────────────────────────────

  /**
   * React layout effect hook — animates ticket cards from their previous DOM
   * positions to their new positions whenever snapshotKey changes (FLIP technique).
   * Respects prefers-reduced-motion.
   */
  static useFlipAnimations(
    boardRef: RefObject<HTMLElement | null>,
    snapshotKey: string | undefined,
  ): void {
    const prevRectsRef = useRef<Map<string, DOMRect>>(new Map());
    const seededRef = useRef(false);

    useLayoutEffect(() => {
      const root = boardRef.current;
      if (!root || !snapshotKey) return;

      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const nextRects = KanbanBoard.collectTicketRects(root);

      if (!seededRef.current) {
        seededRef.current = true;
        prevRectsRef.current = nextRects;
        return;
      }

      if (reducedMotion) {
        prevRectsRef.current = nextRects;
        return;
      }

      const prevRects = prevRectsRef.current;
      const animating: HTMLElement[] = [];

      for (const el of root.querySelectorAll<HTMLElement>('[data-ticket]')) {
        const id = el.dataset.ticket;
        if (!id) continue;
        const prev = prevRects.get(id);
        const next = nextRects.get(id);
        if (!prev || !next) continue;
        const dx = prev.left - next.left;
        const dy = prev.top - next.top;
        if (Math.abs(dx) < MIN_DELTA_PX && Math.abs(dy) < MIN_DELTA_PX) continue;
        const farMove = Math.hypot(dx, dy) > 120;
        KanbanBoard.prepareFlip(el, dx, dy, farMove);
        animating.push(el);
      }

      if (animating.length === 0) {
        prevRectsRef.current = nextRects;
        return;
      }

      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          for (const el of animating) {
            el.style.transition = `transform ${FLIP_DURATION_MS}ms ${FLIP_EASING}`;
            el.style.transform = 'translate3d(0, 0, 0)';
          }
        });
      });

      const timers = animating.map((el) =>
        window.setTimeout(() => KanbanBoard.cleanupFlip(el), FLIP_DURATION_MS + 80),
      );
      for (const el of animating) {
        el.addEventListener(
          'transitionend',
          (ev) => { if (ev.propertyName === 'transform') KanbanBoard.cleanupFlip(el); },
          { once: true },
        );
      }

      prevRectsRef.current = nextRects;
      return () => {
        for (const id of timers) window.clearTimeout(id);
        for (const el of animating) KanbanBoard.cleanupFlip(el);
      };
    }, [boardRef, snapshotKey]);
  }

  // ── Private: FLIP helpers ─────────────────────────────────────────────────

  private static collectTicketRects(root: HTMLElement): Map<string, DOMRect> {
    const rects = new Map<string, DOMRect>();
    for (const el of root.querySelectorAll<HTMLElement>('[data-ticket]')) {
      const id = el.dataset.ticket;
      if (id) rects.set(id, el.getBoundingClientRect());
    }
    return rects;
  }

  private static prepareFlip(el: HTMLElement, dx: number, dy: number, farMove: boolean): void {
    KanbanBoard.cleanupFlip(el);
    el.classList.add('kb-ticket--flip');
    if (farMove) el.classList.add('kb-ticket--flip-far');
    el.style.willChange = 'transform';
    el.style.zIndex = farMove ? '20' : '5';
    el.style.transform = `translate3d(${dx}px, ${dy}px, 0)`;
  }

  private static cleanupFlip(el: HTMLElement): void {
    el.classList.remove('kb-ticket--flip', 'kb-ticket--flip-far');
    el.style.transition = '';
    el.style.transform = '';
    el.style.zIndex = '';
    el.style.willChange = '';
    el.style.boxShadow = '';
  }
}
