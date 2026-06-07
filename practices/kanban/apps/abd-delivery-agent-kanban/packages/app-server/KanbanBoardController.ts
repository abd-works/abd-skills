import { execFile } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import type { AgentRole, StageId, KanbanBoardSnapshot } from '@deliveryforge/kanban-shared';
import { AGENT_ROLES } from '@deliveryforge/kanban-shared';
import { KanbanBoard } from '@deliveryforge/kanban-server';

const execFileAsync = promisify(execFile);
const _dirname = path.dirname(fileURLToPath(import.meta.url));
const KANBAN_CLI_SCRIPT = path.resolve(
  _dirname,
  '../../../../skills/abd-kanban/scripts/kanban_cli.py',
);

export interface ConfigBody {
  planningRoot?: string;
}

export interface TeamBody {
  planningRoot?: string;
  role?: string;
  delta?: number;
}

export interface ModeBody {
  planningRoot?: string;
}

export interface TicketMoveBody {
  planningRoot?: string;
  ticket_id?: string;
  target_stage?: string;
  placement?: string;
}

export interface ActionIntentBody {
  planningRoot?: string;
  ticket_id?: string;
  skill?: string;
  agent_role?: string;
}

export interface LeadScanBody {
  planningRoot?: string;
}

function errorStatus(message: string): number {
  if (message.includes('not found')) return 404;
  if (
    message.includes('Cannot move') ||
    message.includes('scatter') ||
    message.includes('thin-slicing') ||
    message.includes('duplicate IDs')
  ) {
    return 400;
  }
  return 500;
}

export class KanbanBoardController {
  constructor(private readonly board: KanbanBoard) {}

  getConfig(): { planningRoot: string | null } {
    return { planningRoot: this.board.getPlanningRoot() };
  }

  async setConfig(body: ConfigBody): Promise<KanbanBoardSnapshot> {
    const planningRoot = String(body.planningRoot ?? '').trim();
    if (!planningRoot) throw new ValidationError('planningRoot required');
    this.board.setPlanningRoot(planningRoot);
    return this.board.loadSnapshot(planningRoot);
  }

  async getSnapshot(
    planningRoot: string | undefined,
    ifNoneMatch: string | undefined,
  ): Promise<{ snapshot: KanbanBoardSnapshot; notModified: boolean }> {
    const root = planningRoot ?? this.board.getPlanningRoot() ?? '';
    if (!root) throw new ValidationError('planningRoot query param or config required');
    const snapshot = await this.board.loadSnapshot(root);
    if (ifNoneMatch && ifNoneMatch === snapshot.etag) {
      return { snapshot, notModified: true };
    }
    return { snapshot, notModified: false };
  }

  async updateTeam(body: TeamBody): Promise<KanbanBoardSnapshot> {
    const planningRoot = String(body.planningRoot ?? this.board.getPlanningRoot() ?? '').trim();
    const role = body.role as string;
    const delta = Number(body.delta);

    if (!planningRoot) throw new ValidationError('planningRoot required');
    if (!AGENT_ROLES.includes(role as AgentRole)) {
      throw new ValidationError('role must be one of: ' + AGENT_ROLES.join(', '));
    }
    if (!Number.isFinite(delta) || (delta !== 1 && delta !== -1)) {
      throw new ValidationError('delta must be 1 or -1');
    }

    return this.board.updateTeamAndPersist(role as AgentRole, delta, planningRoot);
  }

  async toggleMode(body: ModeBody): Promise<KanbanBoardSnapshot> {
    const planningRoot = String(body.planningRoot ?? this.board.getPlanningRoot() ?? '').trim();
    if (!planningRoot) throw new ValidationError('planningRoot required');
    return this.board.toggleModeAndPersist(planningRoot);
  }

  async moveTicket(body: TicketMoveBody): Promise<KanbanBoardSnapshot> {
    const planningRoot = String(body.planningRoot ?? this.board.getPlanningRoot() ?? '').trim();
    const ticketId = String(body.ticket_id ?? '').trim();
    const targetStage = String(body.target_stage ?? '').trim();

    if (!planningRoot || !ticketId || !targetStage) {
      throw new ValidationError('planningRoot, ticket_id, and target_stage required');
    }
    const placement = body.placement === 'stage_done' ? 'stage_done' : 'in_progress';

    try {
      return await this.board.moveToStageAndPersist(
        ticketId,
        targetStage as StageId,
        planningRoot,
        placement as 'in_progress' | 'stage_done',
      );
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Move ticket failed';
      throw new DomainError(message, errorStatus(message));
    }
  }

  async resumeTicket(body: TicketMoveBody): Promise<KanbanBoardSnapshot> {
    const planningRoot = String(body.planningRoot ?? this.board.getPlanningRoot() ?? '').trim();
    const ticketId = String(body.ticket_id ?? '').trim();
    const targetStage = body.target_stage as string | undefined;

    if (!planningRoot) throw new ValidationError('planningRoot required');
    if (!ticketId) throw new ValidationError('ticket_id required');

    try {
      return await this.board.moveToStageAndPersist(
        ticketId,
        targetStage ? (targetStage as StageId) : null,
        planningRoot,
      );
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Move ticket failed';
      throw new DomainError(message, errorStatus(message));
    }
  }

  async writeActionIntent(body: ActionIntentBody): Promise<{ ok: true }> {
    const planningRoot = String(body.planningRoot ?? this.board.getPlanningRoot() ?? '').trim();
    const ticketId = body.ticket_id as string;
    const skill = body.skill as string;
    const agentRole = body.agent_role as string;

    if (!planningRoot) throw new ValidationError('planningRoot required');
    if (!ticketId || !skill || !agentRole) {
      throw new ValidationError('ticket_id, skill, and agent_role are required');
    }

    await this.board.writeActionIntent(
      { ticket_id: ticketId, skill, agent_role: agentRole, created_at: new Date().toISOString() },
      planningRoot,
    );
    return { ok: true };
  }

  async leadScan(body: LeadScanBody): Promise<unknown> {
    const planningRoot = String(body.planningRoot ?? this.board.getPlanningRoot() ?? '').trim();
    if (!planningRoot) throw new ValidationError('planningRoot required');

    const engagementRoot = KanbanBoard.engagementWorkspaceFromPlanningRoot(planningRoot);
    const { stdout } = await execFileAsync(
      'python',
      [KANBAN_CLI_SCRIPT, 'lead', 'tick', '--workspace', engagementRoot, '--json'],
      { timeout: 30_000 },
    );
    return JSON.parse(stdout);
  }
}

export class ValidationError extends Error {
  readonly status = 400;
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class DomainError extends Error {
  readonly status: number;
  constructor(message: string, status = 500) {
    super(message);
    this.name = 'DomainError';
    this.status = status;
  }
}
