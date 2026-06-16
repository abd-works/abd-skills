import type { AgentDefinition } from './AgentDefinition';
import type { BootstrapPrompt } from '@deliveryforge/kanban-shared';
import { SkillProgress } from '@deliveryforge/kanban-shared';
import type { Ticket } from '@deliveryforge/kanban-shared';
import { AgentSession } from './AgentSession';

/**
 * domain model: KanbanLead — orchestrates agent lifecycle via the Cursor SDK.
 *      Receives workspace path from the board configuration and injects it
 *      into every BootstrapPrompt it assembles.
 *
 * Responsibilities:
 *   - Create, start, stop, and restart AgentSessions for each role slot
 *   - Inject workspace into bootstrap prompts (invariant: workspace comes from board)
 *   - Track pool avatar state for each role
 *   - Detect stale/completed sessions and restart with eligible work
 *   - Record skill completion and ticket sub-column transitions
 */

export interface KanbanLeadOptions {
  workspace?: string;
}

export interface HandleSkillCompletionResult {
  updatedProgress: SkillProgress;
  session: AgentSession;
}

export class KanbanLead {
  readonly workspace: string;
  private readonly _sessions = new Map<string, AgentSession>();
  private readonly _ticketSubColumns = new Map<string, string>();

  constructor(opts: KanbanLeadOptions = {}) {
    this.workspace = opts.workspace ?? '';
  }

  // ─── Session Lifecycle ────────────────────────────────────────────────────

  createAgentSession(
    definition: AgentDefinition,
    workspace: string,
    opts?: { mcpServers?: Record<string, string[]> },
  ): AgentSession {
    if (AgentSession.isConnectionErrorSimulated()) {
      throw new Error(`Agent session creation failed for role: ${definition.role}`);
    }

    const bootstrapPrompt: BootstrapPrompt = {
      workspace,
      role: definition.role,
      agentDefinition: definition.path,
    };

    const mcpServers = opts?.mcpServers
      ? Object.values(opts.mcpServers).flat()
      : [];

    const session = new AgentSession(definition.role, {
      status: 'running',
      bootstrapPrompt,
      mcpServers,
    });

    this._sessions.set(definition.role, session);
    return session;
  }

  startTeamMember(role: string, tickets: Ticket[]): AgentSession {
    const first = tickets[0]!;
    const skill = first.activeSkillId ?? '';
    const session = new AgentSession(role, { status: 'running' }).setExecuting(
      skill,
      first.ticketId,
    );
    this._sessions.set(role, session);
    return session;
  }

  stopTeamMember(session: AgentSession): AgentSession {
    const terminated = session.terminate();
    this._sessions.set(session.role, terminated);
    return terminated;
  }

  detectStaleAndRestart(staleSession: AgentSession): AgentSession {
    const skill = staleSession.currentSkill ?? '';
    const ticketId = staleSession.currentTicketId ?? '';
    const fresh = new AgentSession(staleSession.role, { status: 'running' }).setExecuting(
      skill,
      ticketId,
    );
    this._sessions.set(staleSession.role, fresh);
    return fresh;
  }

  detectCompletedAndRestart(
    completedSession: AgentSession,
    eligibleTicket: Ticket,
  ): AgentSession {
    const skill = eligibleTicket.activeSkillId ?? '';
    const fresh = new AgentSession(completedSession.role, { status: 'running' }).setExecuting(
      skill,
      eligibleTicket.ticketId,
    );
    this._sessions.set(completedSession.role, fresh);
    return fresh;
  }

  handleSkillCompletion(session: AgentSession): HandleSkillCompletionResult {
    const updatedProgress = SkillProgress.create(
      session.currentTicketId ?? '',
      session.currentSkill ?? '',
      'done',
    );
    this._ticketSubColumns.set(session.currentTicketId ?? '', 'Done');
    return { updatedProgress, session };
  }

  // ─── Queries ──────────────────────────────────────────────────────────────

  getSessionForRole(role: string): AgentSession | undefined {
    return this._sessions.get(role);
  }

  getPoolAvatarState(role: string): 'working' | 'idle' | 'inactive' {
    const session = this._sessions.get(role);
    if (!session || session.status !== 'running') return 'idle';
    return session.currentSkill ? 'working' : 'idle';
  }

  getTicketSubColumn(ticketId: string, _stage: string): string {
    return this._ticketSubColumns.get(ticketId) ?? 'In Progress';
  }

  // ─── Factories ────────────────────────────────────────────────────────────

  static create(opts: KanbanLeadOptions): KanbanLead {
    return new KanbanLead(opts);
  }

  static createForScanCycle(): KanbanLead {
    return new KanbanLead();
  }
}
