import type { AgentRole, KanbanBoardSnapshot } from '@deliveryforge/kanban-shared';
import { KanbanBoard } from './KanbanBoard';

export const ROLE_LABELS: Record<AgentRole, string> = {
  'product-owner': 'PO',
  'business-expert': 'BE',
  'ux-designer': 'UX',
  engineer: 'ENG',
};

export const ROLE_FULL: Record<AgentRole, string> = {
  'product-owner': 'Product Owner',
  'business-expert': 'Business Expert',
  'ux-designer': 'UX Designer',
  engineer: 'Engineer',
};

/**
 * Presentation-layer Heartbeat — agent pool display helpers and server API calls.
 * Agent liveness is now derived from SDK session state, not heartbeat files.
 */
export class Heartbeat {
  // ── Display helpers ────────────────────────────────────────────────

  /** Human-readable elapsed time: "30s ago", "5m ago", "2h 10m ago". */
  static formatAge(seconds: number | null): string {
    if (seconds === null) return '';
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m ago`;
  }

  /** Full label for a role, falls back to 'Kanban Lead' for that role. */
  static roleLabel(role: AgentRole | 'kanban-lead'): string {
    return role === 'kanban-lead' ? 'KL' : ROLE_LABELS[role as AgentRole];
  }

  static roleFullName(role: AgentRole | 'kanban-lead'): string {
    return role === 'kanban-lead' ? 'Kanban Lead' : ROLE_FULL[role as AgentRole];
  }

  /** Build the tooltip string shown on an agent avatar. */
  static avatarTooltip(
    role: AgentRole | 'kanban-lead',
    index: number,
    state: 'idle' | 'working' | 'inactive',
    lastActivitySec: number | null,
    note?: string | null,
  ): string {
    const fullName = Heartbeat.roleFullName(role);
    const stateLabel = state === 'inactive' ? 'no session' : state;
    const agePart = lastActivitySec != null ? ` (${Heartbeat.formatAge(lastActivitySec)})` : '';
    const notePart = note ? `\n${note}` : '';
    return (
      fullName +
      (role !== 'kanban-lead' ? ' #' + (index + 1) : '') +
      ' \u2014 ' +
      stateLabel +
      agePart +
      notePart
    );
  }

  // ── Agent pool API ────────────────────────────────────────────────

  /** POST /api/board/team to increment or decrement a role's executor count. */
  static async adjustTeam(
    role: AgentRole,
    delta: number,
  ): Promise<KanbanBoardSnapshot | null> {
    const planningRoot = KanbanBoard.resolvePlanningRoot();
    const res = await fetch('/api/board/team', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ planningRoot, role, delta }),
    });
    if (!res.ok) return null;
    return res.json() as Promise<KanbanBoardSnapshot>;
  }

  /** POST /api/board/lead-scan to trigger a kanban lead tick. */
  static async leadScan(): Promise<{
    must_spawn?: boolean;
    spawns?: Array<{ role: string; instance: number }>;
    actions?: string[];
  } | null> {
    const planningRoot = KanbanBoard.resolvePlanningRoot();
    const res = await fetch('/api/board/lead-scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ planningRoot }),
    });
    if (!res.ok) return null;
    return res.json();
  }
}
