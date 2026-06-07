import type { AgentDefinition } from './AgentDefinition';
import { AgentSession } from './AgentSession';

/**
 * domain model: TeamMember — a delivery agent (executor or reviewer) identified by role.
 *      Extends the shared Agent concept with server-side Cursor SDK session management.
 *
 * Responsibilities:
 *   - Hold a reference to the active AgentSession for this slot
 *   - Delegate session lifecycle to KanbanLead
 *   - Report slot identity (role, slot type)
 */

export type SlotType = 'executor' | 'reviewer';

export class TeamMember {
  readonly role: string;
  readonly slotType: SlotType;
  readonly definition: AgentDefinition;
  private _session: AgentSession | null;

  constructor(role: string, slotType: SlotType, definition: AgentDefinition) {
    this.role = role;
    this.slotType = slotType;
    this.definition = definition;
    this._session = null;
  }

  get session(): AgentSession | null {
    return this._session;
  }

  get isActive(): boolean {
    return this._session?.status === 'running';
  }

  attachSession(session: AgentSession): void {
    this._session = session;
  }

  detachSession(): void {
    this._session = null;
  }

  static create(role: string, slotType: SlotType, definition: AgentDefinition): TeamMember {
    return new TeamMember(role, slotType, definition);
  }
}
