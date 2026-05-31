import { Router } from 'express';
import { AGENT_ROLES, type AgentRole } from '@deliveryforge/delivery-board-shared';
import { KanbanBoardService } from './kanbanBoard.service';

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

  return router;
}
