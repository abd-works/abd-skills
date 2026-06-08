import { Router } from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  AGENT_ROLES,
  type AgentRole,
  type StageId,
  type AgentStartResult,
  type AgentStopResult,
  type ActionIntentResult,
} from '@deliveryforge/kanban-shared';
import { KanbanBoard } from '@deliveryforge/kanban-server';
import { PlanningFolderRepository } from '@deliveryforge/kanban-server';
import { SdkSessionRegistry } from './SdkSessionRegistry';
import { FixtureAutomationService } from './FixtureAutomationService';
import { KanbanLeadService } from './KanbanLeadService';

const _dirname = path.dirname(fileURLToPath(import.meta.url));
const LEAD_TICK_SCRIPT = path.resolve(
  _dirname,
  '../../../../skills/abd-kanban/scripts/run_kanban_lead_tick.py',
);
const KANBAN_CLI_SCRIPT = path.resolve(
  _dirname,
  '../../../../skills/abd-kanban/scripts/kanban_cli.py',
);

const fixtureAutomation = new FixtureAutomationService(KANBAN_CLI_SCRIPT);
const leadService = new KanbanLeadService(LEAD_TICK_SCRIPT);

export function createKanbanBoardRouter(repo: PlanningFolderRepository): Router {
  const router = Router();

  let board: KanbanBoard | null = null;

  async function ensureBoard(planningRoot: string): Promise<KanbanBoard> {
    if (board && board.getPlanningRoot() === planningRoot) return board;
    board = await KanbanBoard.load(planningRoot, repo);
    return board;
  }

  // ── Health ───────────────────────────────────────────────────────────────

  router.get('/health', (_req, res) => {
    res.json({ ok: true });
  });

  // ── Board config ─────────────────────────────────────────────────────────

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

  // ── Board snapshot ───────────────────────────────────────────────────────

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

  // ── Team ─────────────────────────────────────────────────────────────────

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

  // ── Board mode ───────────────────────────────────────────────────────────

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

  // ── Ticket moves ─────────────────────────────────────────────────────────

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
      const status = message.includes('not found') ? 404
        : message.includes('Cannot move') || message.includes('scatter') ? 400
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
      const status = message.includes('not found') ? 404
        : message.includes('Cannot move') || message.includes('scatter')
            || message.includes('thin-slicing') || message.includes('duplicate IDs') ? 400
        : 500;
      res.status(status).json({ error: message });
    }
  });

  // ── Action intent ────────────────────────────────────────────────────────

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
      const engagementRoot = KanbanBoard.engagementWorkspaceFromPlanningRoot(planningRoot);
      const isFixture = await fixtureAutomation.isFixtureWorkspace(engagementRoot);

      await b.writeActionIntent(
        { ticket_id: ticketId, skill, agent_role: agentRole, created_at: new Date().toISOString() },
        planningRoot,
      );
      void fixtureAutomation.schedule(planningRoot, agentRole as AgentRole, engagementRoot);

      const leadScan = await leadService.maybeRunLeadScan(engagementRoot, isFixture, b);
      const result: ActionIntentResult = { ok: true, leadScan };
      res.json(result);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Action intent write failed' });
    }
  });

  // ── Lead scan ────────────────────────────────────────────────────────────

  router.post('/api/board/lead-scan', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? board?.getPlanningRoot() ?? '').trim();
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    try {
      const engagementRoot = KanbanBoard.engagementWorkspaceFromPlanningRoot(planningRoot);
      const result = await leadService.runLeadScan(engagementRoot);
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
      const result: AgentStartResult = { ok: true, role: role as AgentRole, state: adapter.state };
      res.json(result);
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
    const result: AgentStopResult = { ok: true, role: role as AgentRole };
    res.json(result);
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
    req.on('close', () => adapter.removeListener(listener));
  });

  return router;
}
