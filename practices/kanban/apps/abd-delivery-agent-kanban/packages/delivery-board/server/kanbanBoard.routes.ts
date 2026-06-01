import { Router } from 'express';
import { execFile } from 'node:child_process';
import path from 'node:path';
import { promisify } from 'node:util';
import { AGENT_ROLES, type AgentRole } from '@deliveryforge/delivery-board-shared';
import type { StageId } from '@deliveryforge/delivery-board-shared';
import { KanbanBoardService } from './kanbanBoard.service';

const execFileAsync = promisify(execFile);
const LEAD_TICK_SCRIPT = path.resolve(
  __dirname,
  '../../../../skills/abd-kanban/scripts/run_kanban_lead_tick.py',
);

export function createKanbanBoardRouter(service: KanbanBoardService): Router {
  const router = Router();

  router.get('/health', (_req, res) => {
    res.json({ ok: true });
  });

  router.get('/api/board/config', (_req, res) => {
    res.json({ planningRoot: service.getPlanningRoot() });
  });

  router.post('/api/board/config', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? '').trim();
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    try {
      await service.setPlanningRoot(planningRoot);
      const snapshot = await service.loadSnapshot(planningRoot);
      res.json(snapshot);
    } catch (err) {
      res.status(400).json({ error: err instanceof Error ? err.message : 'Invalid planning root' });
    }
  });

  router.get('/api/board', async (req, res) => {
    const planningRoot = String(req.query.planningRoot ?? service.getPlanningRoot() ?? '');
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot query param or config required' });
      return;
    }
    try {
      const snapshot = await service.loadSnapshot(planningRoot);
      const ifNoneMatch = req.headers['if-none-match'];
      if (ifNoneMatch && ifNoneMatch === snapshot.etag) {
        res.status(304).end();
        return;
      }
      res.setHeader('ETag', snapshot.etag);
      res.json(snapshot);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Board load failed' });
    }
  });

  router.post('/api/board/team', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? service.getPlanningRoot() ?? '').trim();
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
      const snapshot = await service.updateTeam(role as AgentRole, delta, planningRoot);
      res.json(snapshot);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Team update failed' });
    }
  });

  router.post('/api/board/mode', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? service.getPlanningRoot() ?? '').trim();
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    try {
      const snapshot = await service.toggleBoardMode(planningRoot);
      res.json(snapshot);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Board mode toggle failed' });
    }
  });

  router.post('/api/board/ticket/resume-in-progress', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? service.getPlanningRoot() ?? '').trim();
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
      const snapshot = await service.moveTicketToStage(
        planningRoot,
        ticketId,
        targetStage ? (targetStage as StageId) : null,
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
    const planningRoot = String(req.body?.planningRoot ?? service.getPlanningRoot() ?? '').trim();
    const ticketId = String(req.body?.ticket_id ?? '').trim();
    const targetStage = String(req.body?.target_stage ?? '').trim();

    if (!planningRoot || !ticketId || !targetStage) {
      res.status(400).json({ error: 'planningRoot, ticket_id, and target_stage required' });
      return;
    }

    const placement =
      req.body?.placement === 'stage_done' ? 'stage_done' : 'in_progress';

    try {
      const snapshot = await service.moveTicketToStage(
        planningRoot,
        ticketId,
        targetStage as StageId,
        placement,
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
    const planningRoot = String(req.body?.planningRoot ?? service.getPlanningRoot() ?? '').trim();
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
      await service.writeActionIntent(planningRoot, {
        ticket_id: ticketId,
        skill,
        agent_role: agentRole,
        created_at: new Date().toISOString(),
      });
      // Delegate on disk immediately; Cursor spawn still requires live kanban-lead session.
      let scan: Record<string, unknown> | null = null;
      try {
        const { stdout } = await execFileAsync('python', [LEAD_TICK_SCRIPT, '--workspace', planningRoot, '--json'], {
          timeout: 30_000,
        });
        scan = JSON.parse(stdout) as Record<string, unknown>;
      } catch {
        scan = null;
      }
      res.json({ ok: true, lead_scan: scan });
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Action intent write failed' });
    }
  });

  router.post('/api/board/lead-scan', async (req, res) => {
    const planningRoot = String(req.body?.planningRoot ?? service.getPlanningRoot() ?? '').trim();
    if (!planningRoot) {
      res.status(400).json({ error: 'planningRoot required' });
      return;
    }
    try {
      const { stdout } = await execFileAsync('python', [LEAD_TICK_SCRIPT, '--workspace', planningRoot, '--json'], {
        timeout: 30_000,
      });
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (err) {
      res.status(500).json({ error: err instanceof Error ? err.message : 'Lead scan failed' });
    }
  });

  return router;
}
