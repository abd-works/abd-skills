import { readFile } from 'node:fs/promises';
import path from 'node:path';
import type { AgentRole } from '@deliveryforge/kanban-shared';
import {
  LeadScanService,
  claimNextIntent,
  applySkillFixture,
  findInProgressClaim,
} from '@deliveryforge/kanban-server';

const WINDOW_MS = 30_000;
const INTERVAL_MS = 5_000;

type AutomationState = {
  timer: NodeJS.Timeout;
  expiresAtMs: number;
  busy: boolean;
  roles: Set<AgentRole>;
};

/**
 * Drives fixture-mode kanban automation — a repeating timer that runs lead
 * sync and member fixture ticks so the board evolves without a real agent.
 *
 * Previously shelled out to Python kanban_cli.py. Now calls the TypeScript
 * domain layer directly. Python scripts are kept but the app no longer depends
 * on them.
 */
export class FixtureAutomationService {
  private readonly byWorkspace = new Map<string, AutomationState>();

  /**
   * Start or extend fixture automation for a workspace/role.
   * No-ops when the workspace is not in fixture mode.
   */
  async schedule(planningRoot: string, role: AgentRole, engagementRoot: string): Promise<void> {
    if (!(await this.isFixtureWorkspace(engagementRoot))) return;

    const existing = this.byWorkspace.get(engagementRoot);
    const nextExpiry = Date.now() + WINDOW_MS;
    if (existing) {
      existing.roles = new Set<AgentRole>([role]);
      existing.expiresAtMs = nextExpiry;
      return;
    }

    const state: AutomationState = {
      timer: setInterval(async () => {
        const current = this.byWorkspace.get(engagementRoot);
        if (!current) return;
        if (Date.now() > current.expiresAtMs) {
          clearInterval(current.timer);
          this.byWorkspace.delete(engagementRoot);
          return;
        }
        if (current.busy) return;
        current.busy = true;
        try {
          await this.runTick(engagementRoot, planningRoot, current.roles);
          if (await this.hasOutstandingWork(engagementRoot, planningRoot, current.roles)) {
            current.expiresAtMs = Date.now() + WINDOW_MS;
          }
        } catch {
          // Best-effort; next interval will retry.
        } finally {
          const live = this.byWorkspace.get(engagementRoot);
          if (live) live.busy = false;
        }
      }, INTERVAL_MS),
      expiresAtMs: nextExpiry,
      busy: false,
      roles: new Set<AgentRole>([role]),
    };

    this.byWorkspace.set(engagementRoot, state);
  }

  async isFixtureWorkspace(engagementRoot: string): Promise<boolean> {
    const contextPath = path.join(engagementRoot, 'CONTEXT.md');
    try {
      const text = await readFile(contextPath, 'utf8');
      return /fixture_mode[\s\W]*true/i.test(text);
    } catch {
      return false;
    }
  }

  private async runTick(
    engagementRoot: string,
    planningRoot: string,
    roles: Set<AgentRole>,
  ): Promise<void> {
    const leadService = new LeadScanService(engagementRoot);
    const warRoom = await leadService.getWarRoomDir();

    // 1. Sync the board (advance complete tickets, flag scatter)
    await leadService.syncBoard().catch(() => null);

    // 2. For each role: claim next intent (manual mode), then apply fixture
    for (const role of roles) {
      await claimNextIntent(warRoom, role).catch(() => null);

      const claim = await findInProgressClaim(warRoom, role).catch(() => null);
      if (claim) {
        await applySkillFixture(
          warRoom,
          engagementRoot,
          role,
          claim.ticket_id,
          claim.skill,
        ).catch(() => null);
      }
    }
  }

  private async hasOutstandingWork(
    engagementRoot: string,
    planningRoot: string,
    roles: Set<AgentRole>,
  ): Promise<boolean> {
    if (roles.size === 0) return false;
    const kanbanDir = path.join(planningRoot, 'kanban');
    const boardPath = path.join(kanbanDir, 'board.json');
    const actionPath = path.join(kanbanDir, 'action-state.json');

    try {
      const actionRaw = await readFile(actionPath, 'utf8');
      const action = JSON.parse(actionRaw) as { intents?: Array<{ agent_role?: string }> };
      if (
        Array.isArray(action.intents) &&
        action.intents.some((i) => roles.has(i.agent_role as AgentRole))
      ) {
        return true;
      }
    } catch {
      // Missing/invalid action-state means no queued intents.
    }

    try {
      const boardRaw = await readFile(boardPath, 'utf8');
      const board = JSON.parse(boardRaw) as {
        active?: Array<{
          skill_progress?: Record<
            string,
            { execution_status?: string; review_status?: string | null; agent?: string }
          >;
        }>;
      };
      const active = Array.isArray(board.active) ? board.active : [];
      for (const ticket of active) {
        for (const skill of Object.values(ticket.skill_progress ?? {})) {
          const ticketRole = skill.agent as AgentRole | undefined;
          if (!ticketRole || !roles.has(ticketRole)) continue;
          if (skill.execution_status === 'in_progress' || skill.review_status === 'in_progress') {
            return true;
          }
        }
      }
    } catch {
      return true;
    }

    return false;
  }
}
