import type { Request, Response } from 'express';
import {
  createDiscoverySessionBodySchema,
  customerLocationSchema,
  selectStoreBodySchema,
} from '../shared/src/store.schema';
import { StoreService } from './store.service';

export class StoreApi {
  constructor(private readonly service: StoreService) {}

  createDiscoverySession(req: Request, res: Response): void {
    const parsed = createDiscoverySessionBodySchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: parsed.error.issues[0]?.message ?? 'invalid body' });
      return;
    }
    const sessionId = String(req.headers['x-session-id'] ?? crypto.randomUUID());
    const session = this.service.createDiscoverySession(
      sessionId,
      parsed.data.displayName,
      parsed.data.customerLocation,
    );
    res.status(201).json({ sessionId, session });
  }

  getMap(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(this.service.getStoreMap(sessionId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  getList(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(this.service.getStoreList(sessionId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  selectFromMap(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const parsed = selectStoreBodySchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: parsed.error.issues[0]?.message ?? 'invalid body' });
      return;
    }
    try {
      res.json(this.service.selectStoreFromMap(sessionId, parsed.data.storeId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  selectFromList(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const parsed = selectStoreBodySchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: parsed.error.issues[0]?.message ?? 'invalid body' });
      return;
    }
    try {
      res.json(this.service.selectStoreFromList(sessionId, parsed.data.storeId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  shareLocation(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const parsed = customerLocationSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: parsed.error.issues[0]?.message ?? 'invalid body' });
      return;
    }
    try {
      res.json(
        this.service.shareLocation(
          sessionId,
          parsed.data.latitude,
          parsed.data.longitude,
        ),
      );
    } catch (error) {
      this.sendError(res, error);
    }
  }

  switchToMap(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(this.service.switchToMapView(sessionId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  private requireSessionId(req: Request, res: Response): string | undefined {
    const sessionId = req.headers['x-session-id'];
    if (!sessionId || Array.isArray(sessionId)) {
      res.status(401).json({ error: 'x-session-id required' });
      return undefined;
    }
    return sessionId;
  }

  private sendError(res: Response, error: unknown): void {
    if (error instanceof Error) {
      res.status(422).json({ error: error.message });
      return;
    }
    res.status(500).json({ error: 'unexpected error' });
  }
}
