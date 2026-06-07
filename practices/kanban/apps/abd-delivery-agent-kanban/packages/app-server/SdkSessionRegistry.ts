import { CursorSdkAdapter } from './CursorSdkAdapter';
import { KanbanBoard } from '@deliveryforge/kanban-server';
import type { AgentRole } from '@deliveryforge/kanban-shared';

/**
 * SdkSessionRegistry — module-level store of running CursorSdkAdapter instances.
 *
 * Responsibilities:
 *   - Start, stop, and retrieve SDK sessions by role
 *   - Build an agent-sessions status map for the board snapshot
 *   - Derive the bootstrap prompt from the agent definition path and workspace
 */

const _sessions = new Map<string, CursorSdkAdapter>();

export const SdkSessionRegistry = {
  get(role: string): CursorSdkAdapter | undefined {
    return _sessions.get(role);
  },

  all(): Map<string, CursorSdkAdapter> {
    return _sessions;
  },

  async start(role: AgentRole, planningRoot: string): Promise<CursorSdkAdapter> {
    const existing = _sessions.get(role);
    if (existing && existing.state === 'running') return existing;

    const workspace = KanbanBoard.engagementWorkspaceFromPlanningRoot(planningRoot);
    const adapter = new CursorSdkAdapter(role, workspace);
    _sessions.set(role, adapter);

    const prompt = [
      `You are the ${role} agent for this delivery workspace.`,
      `Workspace: ${workspace}`,
      `Role: ${role}`,
      `Read your agent definition at practices/kanban/agents/${role}/AGENT.md and begin your work.`,
    ].join('\n');

    // Fire-and-forget — streaming events flow to listeners
    void adapter.start(prompt).catch(() => {/* errors captured inside adapter */});
    return adapter;
  },

  stop(role: string): void {
    const adapter = _sessions.get(role);
    if (adapter) adapter.stop();
  },

  statusMap(): Record<string, { state: string; messageCount: number; lastActivitySec: number; finalMessage?: string; errorDetail?: string }> {
    const out: Record<string, ReturnType<CursorSdkAdapter['getStatus']>> = {};
    for (const [role, adapter] of _sessions) {
      out[role] = adapter.getStatus();
    }
    return out;
  },
};
