import type { Request, Response } from 'express';
import { saveStockLevelsBodySchema } from '../shared/src/catalog.schema';
import { CatalogService } from './catalog.service';

export class CatalogApi {
  constructor(private readonly service: CatalogService) {}

  getCatalogBrowse(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(this.service.getCatalogBrowse(sessionId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  getProductDetail(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(
        this.service.getProductDetail(sessionId, String(req.params.catalogItemIdentity)),
      );
    } catch (error) {
      this.sendError(res, error);
    }
  }

  getStockMaintenance(req: Request, res: Response): void {
    try {
      const storeIdentity = String(req.query.store ?? '');
      res.json(
        this.service.getStockMaintenance(this.staffToken(req), storeIdentity),
      );
    } catch (error) {
      this.sendError(res, error, 403);
    }
  }

  saveStockLevels(req: Request, res: Response): void {
    const parsed = saveStockLevelsBodySchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({
        ok: false,
        message: parsed.error.issues[0]?.message ?? 'invalid body',
      });
      return;
    }
    try {
      res.json(
        this.service.saveStockLevels(
          this.staffToken(req),
          parsed.data.storeIdentity,
          parsed.data.updates,
        ),
      );
    } catch (error) {
      this.sendError(res, error, 403);
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

  private staffToken(req: Request): string | undefined {
    const token = req.headers['x-staff-token'];
    return Array.isArray(token) ? token[0] : token;
  }

  private sendError(res: Response, error: unknown, status = 422): void {
    if (error instanceof Error) {
      res.status(status).json({ error: error.message });
      return;
    }
    res.status(500).json({ error: 'unexpected error' });
  }
}
