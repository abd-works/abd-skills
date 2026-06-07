import { Router } from 'express';
import { execFile } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import { AGENT_ROLES, type AgentRole, type StageId } from '@deliveryforge/kanban-shared';
import { KanbanBoard } from '@deliveryforge/kanban-server';
import { PlanningFolderRepository } from '@deliveryforge/kanban-server';
import { SdkSessionRegistry } from './SdkSessionRegistry';

const execFileAsync = promisify(execFile);
const _dirname = path.dirname(fileURLToPath(import.meta.url));
const LEAD_TICK_SCRIPT = path.resolve(
  _dirname,
  '../../../../skills/abd-kanban/scripts/run_kanban_lead_tick.py',
);
const KANBAN_CLI_SCRIPT = path.resolve(
  _dirname,
  '../../../../skills/abd-kanban/scripts/kanban_cli.py',
);
const FIXTURE_AUTOMATION_WINDOW_MS = 30_000;
const FIXTURE_AUTOMATION_INTERVAL_MS = 5_000;

type FixtureAutomationState = {
  timer: NodeJS.Timeout;
  expiresAtMs: number;
  busy: boolean;
  roles: Set<AgentRole>;
};

const fixtureAutomationByWorkspace = new Map<string, FixtureAutomationState>();

async function isFixtureWorkspace(workspace: string): Promise<boolean> {
  const contextPath = path.join(workspace, 'CONTEXT.md');
  try {
    const text = await readFile(contextPath, 'utf8');
    // Accept markdown variants like:
    //   fixture_mode: true
    //   **fixture_mode:** `true`
    return /fixture_mode[\s\W]*true/i.test(text);
  } catch {
    return false;
  }
}

async function isManualBoard(planningRoot: string): Promise<boolean> {
  const boardPath = path.join(planningRoot, 'kanban', 'board.json');
  try {
    const raw = await readFile(boardPath, 'utf8');
    const board = JSON.parse(raw) as { board_mode?: string };
    return board.board_mode === 'manual';
  } catch {
    return false;
  }
}

async function runFixtureAutomationTick(workspace: string, roles: Set<AgentRole>): Promise<void> {
  await execFileAsync(
    'python',
    [KANBAN_CLI_SCRIPT, '--json', 'lead', 'sync', '--workspace', workspace],
    { timeout: 30_000 },
  ).catch(() => null);

  for (const role of roles) {
    await execFileAsync(
      'python',
      [KANBAN_CLI_SCRIPT, '--json', 'member', 'intent', '--workspace', workspace, '--role', role],
      { timeout: 30_000 },
    ).catch(() => null);

    await execFileAsync(
      'python',
      [KANBAN_CLI_SCRIPT, '--json', 'member', 'fixture', '--workspace', workspace, '--role', role],
      { timeout: 30_000 },
    ).catch(() => null);
  }
}

async function hasOutstandingFixtureWork(workspace: string, roles: Set<AgentRole>): Promise<boolean> {
  if (roles.size === 0) return false;
  const kanbanDir = path.join(workspace, 'docs', 'planning', 'kanban');
  const boardPath = path.join(kanbanDir, 'board.json');
  const actionPath = path.join(kanbanDir, 'action-state.json');

  try {
    const actionRaw = await readFile(actionPath, 'utf8');
    const action = JSON.parse(actionRaw) as {
      intents?: Array<{ agent_role?: string }>;
    };
    if (Array.isArray(action.intents) && action.intents.some((i) => roles.has(i.agent_role as AgentRole))) {
      return true;
    }
  } catch {
    // Missing/invalid action-state means no queued intents.
  }

  try {
    const boardRaw = await readFile(boardPath, 'utf8');
    const board = JSON.parse(boardRaw) as {
      active?: Array<{ skill_progress?: Record<string, { execution_status?: string; review_status?: string | null }> }>;
    };
    const active = Array.isArray(board.active) ? board.active : [];
    for (const ticket of active) {
      const progress = ticket.skill_progress ?? {};
      for (const skill of Object.values(progress)) {
        const role = (skill as { agent?: string }).agent as AgentRole | undefined;
        if (!role || !roles.has(role)) continue;
        if (skill.execution_status === 'in_progress' || skill.review_status === 'in_progress') {
          return true;
        }
      }
    }
  } catch {
    // If board cannot be read, keep automation alive and retry.
    return true;
  }

  return false;
}

async function scheduleFixtureAutomation(planningRoot: string, role: AgentRole): Promise<void> {
  const workspace = KanbanBoard.engagementWorkspaceFromPlanningRoot(planningRoot);
  if (!(await isFixtureWorkspace(workspace))) return;

  const existing = fixtureAutomationByWorkspace.get(workspace);
  const nextExpiry = Date.now() + FIXTURE_AUTOMATION_WINDOW_MS;
  if (existing) {
    // Manual mode intent should drive only the dropped role.
    existing.roles = new Set<AgentRole>([role]);
    existing.expiresAtMs = nextExpiry;
    return;
  }

  const state: FixtureAutomationState = {
    timer: setInterval(async () => {
      const current = fixtureAutomationByWorkspace.get(workspace);
      if (!current) return;
      if (Date.now() > current.expiresAtMs) {
        clearInterval(current.timer);
        fixtureAutomationByWorkspace.delete(workspace);
        return;
      }
      if (current.busy) return;
      current.busy = true;
      try {
        await runFixtureAutomationTick(workspace, current.roles);
        if (await hasOutstandingFixtureWork(workspace, current.roles)) {
          current.expiresAtMs = Date.now() + FIXTURE_AUTOMATION_WINDOW_MS;
        }
      } catch {
        // Best-effort fixture automation; next interval will retry.
      } finally {
        const live = fixtureAutomationByWorkspace.get(workspace);
        if (live) live.busy = false;
      }
    }, FIXTURE_AUTOMATION_INTERVAL_MS),
    expiresAtMs: nextExpiry,
    busy: false,
    roles: new Set<AgentRole>([role]),
  };

  fixtureAutomationByWorkspace.set(workspace, state);

}

export function createKanbanBoardRouter(repo: PlanningFolderRepository): Router {
  const router = Router();

  let board: KanbanBoard | null = null;

  async function ensureBoard(planningRoot: string): Promise<KanbanBoard> {
    if (board && board.getPlanningRoot() === planningRoot) return board;
    board = await KanbanBoard.load(planningRoot, repo);
    return board;
  }

  router.get('/health', (_req, res) => {
    res.json({ ok: true });
  });

  router.get('/api/board/config', (_req, res) => {
    res.json({ planningRoot: board?.getPlanningRoot() ?? null });
  });

  router.post('/api/board/config', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? '').trim();
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    try {
      board = await KanbanBoard.load(planningRoot, repo);
      const snapshot = await board.loadSnapshot(planningRoot);
      res.json(snapshot);
    } catch (err) {
      res.status(400).json({ error: err instanceof Error ? err.message : 'Invalid planning root' });
    }
  });

  router.get('/api/board', async (req, res) => {
    const planningRoot = String(req.query.planningRoot ?? board?.getPlanningRoot() ?? '');
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot query param or config required' });
      return;
    }
    try {
      const b = await ensureBoard(planningRoot);
      const snapshot = await b.loadSnapshot(planningRoot);
      const ifNoneMatch = req.headers['if-none-match'];
      if (ifNoneMatch && ifNoneMatch === snapshot.etag) {
        res.status(304).end();
        return;
      }
      res.setHeader('ETag', snapshot.etag);
      res.json({ ...snapshot, agentSessions: SdkSessionRegistry.statusMap() });
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Board load failed' });
    }
  });

  router.post('/api/board/team', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    const role = req.body?.role as string;
    const delta = Number(req.body?.delta);

    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    if (!AGENT_ROLES.includes(role as AgentRole)) {
      res.status(400).json({ error: 'role must be one of: ' + AGENT_ROLES.join(', ') });
      return;
    }
    if (!Number.isFinite(delta) || (delta !== 1 && delta !== -1)) {
      res.status(400).json({ error: 'delta must be 1 or -1' });
      return;
    }

    try {
      const b = await ensureBoard(planningRoot);
      const snapshot = await b.updateTeamAndPersist(role as AgentRole, delta, planningRoot);
      res.json(snapshot);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Team update failed' });
    }
  });

  router.post('/api/board/mode', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    try {
      const b = await ensureBoard(planningRoot);
      const snapshot = await b.toggleModeAndPersist(planningRoot);
      res.json(snapshot);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Board mode toggle failed' });
    }
  });

  router.post('/api/board/ticket/resume-in-progress', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    const ticketId = String(req.body?.ticket_id ?? '').trim();
    const targetStage = req.body?.target_stage as string | undefined;

    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    if (!ticketId) {
      res.status(400).json({ error: 'ticket_id required' });
      return;
    }

    try {
      const b = await ensureBoard(planningRoot);
      const snapshot = await b.moveToStageAndPersist(
        ticketId,
        targetStage ? (targetStage as StageId) : null,
        planningRoot,
      );
      res.json(snapshot);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Move ticket failed';
      const status = message.includes('not found')
        ? 404
        : message.includes('Cannot move') || message.includes('scatter')
          ? 400
          : 500;
      res.status(status).json({ error: message });
    }
  });

  router.post('/api/board/ticket/move-to-stage', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    const ticketId = String(req.body?.ticket_id ?? '').trim();
    const targetStage = String(req.body?.target_stage ?? '').trim();

    if (!planningRoot || !ticketId || !targetStage) {
      res.status(400).json({ error: 'planningRoot, ticket_id, and target_stage required' });
      return;
    }

    const placement = req.body?.placement === 'stage_done' ? 'stage_done' : 'in_progress';

    try {
      const b = await ensureBoard(planningRoot);
      const snapshot = await b.moveToStageAndPersist(
        ticketId,
        targetStage as StageId,
        planningRoot,
        placement as 'in_progress' | 'stage_done',
      );
      res.json(snapshot);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Move ticket failed';
      const status = message.includes('not found')
        ? 404
        : message.includes('Cannot move') ||
            message.includes('scatter') ||
            message.includes('thin-slicing') ||
            message.includes('duplicate IDs')
          ? 400
          : 500;
      res.status(status).json({ error: message });
    }
  });

  router.post('/api/board/action-intent', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    const ticketId = req.body?.ticket_id as string;
    const skill = req.body?.skill as string;
    const agentRole = req.body?.agent_role as string;

    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    if (!ticketId || !skill || !agentRole) {
      res.status(400).json({ error: 'ticket_id, skill, and agent_role are required' });
      return;
    }

    try {
      const b = await ensureBoard(planningRoot);
      await b.writeActionIntent(
        { ticket_id: ticketId, skill, agent_role: agentRole, created_at: new Date().toISOString() },
        planningRoot,
      );
      void scheduleFixtureAutomation(planningRoot, agentRole as AgentRole);

      let scan: Record<string, unknown> | null = null;
      const engRoot = KanbanBoard.engagementWorkspaceFromPlanningRoot(planningRoot);
      const fixtureMode = await isFixtureWorkspace(engRoot);
      const manualMode = await isManualBoard(planningRoot);
      try {
        // In fixture+manual mode, do NOT run lead tick here. It can auto-claim other
        // roles (e.g. BE) and violates manual drop intent ownership.
        if (!(fixtureMode && manualMode)) {
          const { stdout } = await execFileAsync('python', [LEAD_TICK_SCRIPT, '--workspace', engRoot, '--json'], {
            timeout: 30_000,
          });
          scan = JSON.parse(stdout) as Record<string, unknown>;
        }
      } catch {
        scan = null;
      }
      res.json({ ok: true, lead_scan: scan });
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Action intent write failed' });
    }
  });

  router.post('/api/board/lead-scan', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    try {
      const engRoot = KanbanBoard.engagementWorkspaceFromPlanningRoot(planningRoot);
      const { stdout } = await execFileAsync('python', [LEAD_TICK_SCRIPT, '--workspace', engRoot, '--json'], {
        timeout: 30_000,
      });
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Lead scan failed' });
    }
  });

  // ── Agent lifecycle (Cursor SDK) ─────────────────────────────────────────

  router.post('/api/board/agent/start', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    const role = req.body?.role as string;

    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    if (!AGENT_ROLES.includes(role as AgentRole)) {
      res.status(400).json({ error: 'role must be one of: ' + AGENT_ROLES.join(', ') });
      return;
    }

    try {
      const adapter = await SdkSessionRegistry.start(role as AgentRole, planningRoot);
      res.json({ ok: true, role, state: adapter.state });
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Agent start failed' });
    }
  });

  router.post('/api/board/agent/stop', (req, res) => {
    const role = req.body?.role as string;
    if (!AGENT_ROLES.includes(role as AgentRole)) {
      res.status(400).json({ error: 'role must be one of: ' + AGENT_ROLES.join(', ') });
      return;
    }
    SdkSessionRegistry.stop(role);
    res.json({ ok: true, role });
  });

  router.get('/api/board/agent/:role/status', (req, res) => {
    const role = req.params['role'];
    const adapter = SdkSessionRegistry.get(role);
    if (!adapter) {
      res.json({ state: 'idle', messageCount: 0, lastActivitySec: 0 });
      return;
    }
    res.json(adapter.getStatus());
  });

  // SSE stream — clients connect and receive agent output events in real time
  router.get('/api/board/agent/:role/stream', (req, res) => {
    const role = req.params['role'];

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.flushHeaders();

    const sendEvent = (data: object) => {
      res.write(`data: ${JSON.stringify(data)}\n\n`);
    };

    const adapter = SdkSessionRegistry.get(role);
    if (!adapter) {
      sendEvent({ type: 'status', state: 'idle' });
      res.end();
      return;
    }

    sendEvent({ type: 'status', state: adapter.state });

    const listener = (event: { type: string; content?: string }) => {
      sendEvent(event);
      if (adapter.state !== 'running') {
        sendEvent({ type: 'status', state: adapter.state });
        res.end();
      }
    };

    adapter.addListener(listener);

    req.on('close', () => {
      adapter.removeListener(listener);
    });
  });

  return router;
}
