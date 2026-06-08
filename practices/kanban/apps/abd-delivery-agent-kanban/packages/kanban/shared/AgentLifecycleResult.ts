import type { AgentRole } from './TeamMembership';
import type { AgentSessionInfo } from './KanbanBoard';

/** Returned by POST /api/board/agent/start */
export interface AgentStartResult {
  ok: true;
  role: AgentRole;
  state: AgentSessionInfo['state'];
}

/** Returned by POST /api/board/agent/stop */
export interface AgentStopResult {
  ok: true;
  role: AgentRole;
}

/** Returned by POST /api/board/action-intent */
export interface ActionIntentResult {
  ok: true;
  leadScan: Record<string, unknown> | null;
}
