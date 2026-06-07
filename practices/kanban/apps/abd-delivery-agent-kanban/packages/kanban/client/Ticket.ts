import {
  Ticket as DomainTicket,
  Stage,
  AGENT_ROLES,
  type AgentRole,
  type KanbanColumn,
  type KanbanBoardSnapshot,
  type StageSkill,
  type StageSubColumn,
  type StageId,
} from '@deliveryforge/kanban-shared';
import type { RawTicket } from '@deliveryforge/kanban-shared';
import { KanbanBoard } from './KanbanBoard';

export const TICKET_DRAG_ID = 'application/ticket-id';
export const TICKET_DRAG_STAGE = 'application/ticket-stage';
export const AGENT_ROLE_DRAG_ID = 'application/agent-role';

const TICKET_API_BASE: string =
  (import.meta as unknown as { env: Record<string, string> }).env.VITE_API_BASE ?? '';

// ── Lead scan result type ─────────────────────────────────────────────────

export type LeadScanResult = {
  must_spawn?: boolean;
  spawns?: Array<{ role: string; instance: number }>;
  actions?: string[];
};

// ── Ticket drag/drop types ─────────────────────────────────────────────────

export type TicketDragPayload = { id: string; stage: StageId };

export type TicketDropPlacement = 'in_progress' | 'stage_done';

export type TicketDropTarget = {
  stage: StageId;
  placement: TicketDropPlacement;
};

/** Callback invoked when a dragged ticket is committed to a drop zone. */
export type TicketStageDropHandler = (
  ticketId: string,
  targetStage: StageId,
  placement: TicketDropPlacement,
) => void;

/**
 * Presentation-layer Ticket — extends domain Ticket with drag/drop behavior,
 * CSS class derivation, skill assignment logic, and drop-target resolution.
 */
export class Ticket extends DomainTicket {
  constructor(raw: RawTicket, column: KanbanColumn) {
    super(raw, column);
  }

  static fromDomain(ticket: DomainTicket): Ticket {
    return new Ticket(ticket.toRaw(), ticket.column);
  }

  // ── Presentation: CSS state class ─────────────────────────────────

  /** CSS modifier for blocked or scatter-parent tickets. */
  statusCssClass(): string {
    if (this.isScatterParent()) return 'kb-ticket--scatter-parent';
    if (this.notes.toLowerCase().includes('blocked')) return 'kb-ticket--blocked';
    return '';
  }

  /** Whether the in-progress sub-column should show the active-work pulse. */
  isInProgressActive(stageSubColumn: StageSubColumn): boolean {
    return (
      stageSubColumn === 'ip' &&
      ((this.executingSkillIds?.length ?? 0) > 0 ||
        this.activeSkillId !== null ||
        (this.reviewingSkillIds?.length ?? 0) > 0 ||
        this.reviewSkillId !== null)
    );
  }

  // ── Presentation: agent skill assignment ───────────────────────────

  /**
   * Find the next skill this agent role can pick up on this ticket.
   * Skips done, in-progress, under-review, pending-intent, and wrong-role skills.
   */
  findNextEligibleSkill(stageSkills: StageSkill[], agentRole?: string): string | null {
    const doneSet = new Set(this.doneSkillIds);
    const pendingSet = new Set(this.pendingIntentSkillIds ?? []);
    const executingSet = new Set(this.executingSkillIds ?? []);
    for (const s of stageSkills) {
      if (agentRole && s.role !== agentRole) continue;
      if (doneSet.has(s.skillId)) continue;
      if (executingSet.has(s.skillId)) continue;
      if ((this.reviewingSkillIds ?? []).includes(s.skillId)) continue;
      if (this.reviewSkillId === s.skillId) continue;
      if (pendingSet.has(s.skillId)) continue;
      return s.skillId;
    }
    return null;
  }

  // ── Presentation: drag — DataTransfer I/O ────────────────────────

  /** Whether this ticket is draggable for cross-stage moves in manual mode. */
  isDraggableForStageMove(boardMode: string, stageSubColumn?: StageSubColumn): boolean {
    return (
      boardMode === 'manual' &&
      (stageSubColumn === 'ip' || stageSubColumn === 'done' || stageSubColumn === 'feeds-next')
    );
  }

  /** Write this ticket's drag payload into a DataTransfer. */
  setDragData(dt: DataTransfer): void {
    if (!this.stage) return;
    dt.setData(TICKET_DRAG_ID, this.ticketId);
    dt.setData(TICKET_DRAG_STAGE, this.stage);
    dt.setData('text/plain', `ticket:${this.ticketId}`);
    dt.effectAllowed = 'move';
  }

  /** True if the DataTransfer carries ticket-drag data. */
  static isTicketStageDrag(dt: DataTransfer, activeDragId?: string | null): boolean {
    if (activeDragId) return true;
    return Ticket.hasExplicitTicketDragData(dt);
  }

  /** True only when the DataTransfer payload explicitly identifies a ticket drag. */
  static hasExplicitTicketDragData(dt: DataTransfer): boolean {
    const id = dt.getData(TICKET_DRAG_ID);
    if (id) return true;
    const plain = dt.getData('text/plain');
    return plain.startsWith('ticket:');
  }

  /** Read the ticket ID out of a drag DataTransfer, with optional ref fallback. */
  static readTicketIdFromDataTransfer(dt: DataTransfer, fallbackId?: string | null): string {
    const id = dt.getData(TICKET_DRAG_ID);
    if (id) return id;
    const plain = dt.getData('text/plain');
    if (plain.startsWith('ticket:')) return plain.slice('ticket:'.length);
    return fallbackId ?? '';
  }

  /** Read an agent role from drag DataTransfer. Supports custom + text fallbacks. */
  static readAgentRoleFromDataTransfer(dt: DataTransfer): AgentRole | null {
    const fromCustom = dt.getData(AGENT_ROLE_DRAG_ID).trim();
    if (AGENT_ROLES.includes(fromCustom as AgentRole)) {
      return fromCustom as AgentRole;
    }

    const plain = dt.getData('text/plain').trim();
    if (plain.startsWith('agent-role:')) {
      const role = plain.slice('agent-role:'.length).trim();
      if (AGENT_ROLES.includes(role as AgentRole)) {
        return role as AgentRole;
      }
      return null;
    }

    if (AGENT_ROLES.includes(plain as AgentRole)) {
      return plain as AgentRole;
    }

    return null;
  }

  // ── HTTP API: ticket operations ───────────────────────────────────

  /**
   * POST /api/board/ticket/move-to-stage or /resume-in-progress.
   * Returns the raw snapshot from the server — call KanbanBoard.fromSnapshot() to hydrate.
   */
  static async moveToStage(
    ticketId: string,
    targetStage: StageId | null,
    placement: 'in_progress' | 'stage_done' = 'in_progress',
  ): Promise<KanbanBoardSnapshot> {
    const planningRoot = KanbanBoard.resolvePlanningRoot();
    const url =
      targetStage === null
        ? TICKET_API_BASE + '/api/board/ticket/resume-in-progress'
        : TICKET_API_BASE + '/api/board/ticket/move-to-stage';
    const body =
      targetStage === null
        ? { planningRoot, ticket_id: ticketId }
        : { planningRoot, ticket_id: ticketId, target_stage: targetStage, placement };
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const payload = await res.json().catch(() => ({})) as { error?: string };
      throw new Error(payload.error ?? 'Move ticket failed');
    }
    return res.json() as Promise<KanbanBoardSnapshot>;
  }

  /** Resume a ticket in-progress (short-hand for moveToStage with null stage). */
  static async resume(ticketId: string): Promise<KanbanBoardSnapshot> {
    return Ticket.moveToStage(ticketId, null);
  }

  /** POST /api/board/action-intent — assign a skill to a ticket for an agent role. */
  static async postActionIntent(
    ticketId: string,
    skill: string,
    agentRole: string,
  ): Promise<{ ok: boolean; lead_scan: LeadScanResult | null }> {
    const planningRoot = KanbanBoard.resolvePlanningRoot();
    const res = await fetch(TICKET_API_BASE + '/api/board/action-intent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ planningRoot, ticket_id: ticketId, skill, agent_role: agentRole }),
    });
    if (!res.ok) {
      const payload = await res.json().catch(() => ({})) as { error?: string };
      throw new Error(payload.error ?? 'Action intent failed');
    }
    return res.json() as Promise<{ ok: boolean; lead_scan: LeadScanResult | null }>;
  }

  /** Stable DOM key for a ticket element. */
  static key(ticketId: string): string {
    return 'ticket-' + ticketId;
  }

  // ── Presentation: drag — drop-target resolution ───────────────────

  /**
   * Resolve a DOM drop hit target to the stage column + placement it belongs to.
   * Used by the board's native drop listener to commit a ticket move.
   */
  static resolveDropTarget(
    target: HTMLElement | null,
    stageOrder: readonly StageId[] = Stage.ORDER,
  ): TicketDropTarget | null {
    if (!target) return null;

    const stageEl = target.closest('[data-stage]');
    const stageAttr = stageEl?.getAttribute('data-stage');
    if (!stageAttr || !stageOrder.includes(stageAttr as StageId)) return null;

    const ipCol = target.closest('.kb-sub-col--ip');
    const doneCol = target.closest('.kb-sub-col--done');
    if (ipCol || doneCol) {
      const placement: TicketDropPlacement = doneCol && !ipCol ? 'stage_done' : 'in_progress';
      return { stage: stageAttr as StageId, placement };
    }

    // Drop on stage header / skill chips still targets that stage's In Progress.
    if (stageEl?.classList.contains('kb-stage-group')) {
      return { stage: stageAttr as StageId, placement: 'in_progress' };
    }

    return null;
  }
}
