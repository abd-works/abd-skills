import type { BootstrapPrompt } from '@deliveryforge/kanban-shared';
import { AgentOutputStream, type AgentOutputEvent } from './AgentOutputStream';

/**
 * domain model: AgentSession — represents a running Cursor SDK session for one agent slot.
 *      Invariant: one active session per agent slot (executor or reviewer instance).
 *
 * Responsibilities:
 *   - Track session state (running / completed / failed)
 *   - Track current skill and ticket being worked
 *   - Emit streamed output events to the server relay
 *   - Report status (state, message count, last activity, final message / error)
 */

export type SessionStatus = 'running' | 'completed' | 'failed';

export interface AgentSessionOptions {
  status?: SessionStatus;
  messageCount?: number;
  lastActivityTs?: number;
  bootstrapPrompt?: BootstrapPrompt;
  mcpServers?: string[];
  currentSkill?: string | null;
  currentTicketId?: string | null;
  finalMessage?: string | null;
  errorDetail?: string | null;
}

export interface SessionStatusReport {
  state: SessionStatus;
  message_count: number;
  last_activity_sec: number;
  final_message?: string;
  error_detail?: string;
}

// One-shot connection error flag — set by simulateConnectionError, consumed on first use
let _simulateConnectionError = false;

// Module-level registry for clearForRole (guards duplicate sessions)
const _sessionsByRole = new Map<string, AgentSession>();

export class AgentSession {
  readonly role: string;
  readonly status: SessionStatus;
  readonly messageCount: number;
  lastActivityTs: number;
  readonly bootstrapPrompt: BootstrapPrompt;
  readonly mcpServers: string[];
  readonly currentSkill: string | null;
  readonly currentTicketId: string | null;
  private readonly _finalMessage: string | null;
  private readonly _errorDetail: string | null;

  constructor(role: string, opts: AgentSessionOptions = {}) {
    this.role = role;
    this.status = opts.status ?? 'running';
    this.messageCount = opts.messageCount ?? 0;
    this.lastActivityTs = opts.lastActivityTs ?? Date.now();
    this.bootstrapPrompt = opts.bootstrapPrompt ?? { workspace: '', role, agentDefinition: '' };
    this.mcpServers = opts.mcpServers ?? [];
    this.currentSkill = opts.currentSkill ?? null;
    this.currentTicketId = opts.currentTicketId ?? null;
    this._finalMessage = opts.finalMessage ?? null;
    this._errorDetail = opts.errorDetail ?? null;
  }

  get state(): SessionStatus {
    return this.status;
  }

  // ─── State Transitions ────────────────────────────────────────────────────

  setExecuting(skill: string, ticketId: string): AgentSession {
    return new AgentSession(this.role, {
      status: this.status,
      messageCount: this.messageCount,
      lastActivityTs: this.lastActivityTs,
      bootstrapPrompt: this.bootstrapPrompt,
      mcpServers: this.mcpServers,
      currentSkill: skill,
      currentTicketId: ticketId,
    });
  }

  setIdle(): AgentSession {
    return new AgentSession(this.role, {
      status: this.status,
      messageCount: this.messageCount,
      lastActivityTs: this.lastActivityTs,
      bootstrapPrompt: this.bootstrapPrompt,
      mcpServers: this.mcpServers,
      currentSkill: null,
      currentTicketId: null,
    });
  }

  terminate(): AgentSession {
    return new AgentSession(this.role, {
      status: 'completed',
      messageCount: this.messageCount,
      lastActivityTs: this.lastActivityTs,
      bootstrapPrompt: this.bootstrapPrompt,
      mcpServers: this.mcpServers,
    });
  }

  // ─── Output Streaming ─────────────────────────────────────────────────────

  emit(event: AgentOutputEvent): AgentOutputStream {
    this.lastActivityTs = Date.now();
    return new AgentOutputStream(event);
  }

  // ─── Status Query ─────────────────────────────────────────────────────────

  queryStatus(): SessionStatusReport {
    const report: SessionStatusReport = {
      state: this.status,
      message_count: this.messageCount,
      last_activity_sec: Math.round((Date.now() - this.lastActivityTs) / 1000),
    };
    if (this._finalMessage) report.final_message = this._finalMessage;
    if (this._errorDetail) report.error_detail = this._errorDetail;
    return report;
  }

  // ─── Static Factories ─────────────────────────────────────────────────────

  static createActive(role: string): AgentSession {
    return new AgentSession(role, { status: 'running' });
  }

  static createWithMessages(
    role: string,
    messageCount: number,
    lastActivitySec: number,
  ): AgentSession {
    return new AgentSession(role, {
      status: 'running',
      messageCount,
      lastActivityTs: Date.now() - lastActivitySec * 1000,
    });
  }

  static createCompleted(role: string, finalMessage: string): AgentSession {
    return new AgentSession(role, {
      status: 'completed',
      finalMessage,
    });
  }

  static createFailed(role: string, errorDetail: string): AgentSession {
    return new AgentSession(role, {
      status: 'failed',
      errorDetail,
    });
  }

  static createStale(
    role: string,
    noOutputSeconds: number,
    skill: string,
    ticketId: string,
  ): AgentSession {
    return new AgentSession(role, {
      status: 'running',
      lastActivityTs: Date.now() - noOutputSeconds * 1000,
      currentSkill: skill,
      currentTicketId: ticketId,
    });
  }

  // ─── Global Fixture Helpers ───────────────────────────────────────────────

  static simulateConnectionError(): void {
    _simulateConnectionError = true;
  }

  static isConnectionErrorSimulated(): boolean {
    if (_simulateConnectionError) {
      _simulateConnectionError = false;
      return true;
    }
    return false;
  }

  static clearForRole(role: string): void {
    _sessionsByRole.delete(role);
  }
}
