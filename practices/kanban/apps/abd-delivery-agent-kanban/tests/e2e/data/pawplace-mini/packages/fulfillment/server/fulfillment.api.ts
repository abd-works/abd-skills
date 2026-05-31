import type { Request, Response } from 'express';
import { FulfillmentService } from './fulfillment.service';

export class FulfillmentApi {
  constructor(private readonly service: FulfillmentService) {}

  listQueue(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      const storeIdentity = String(req.query.store ?? '');
      res.json({
        queue: this.service.listQueue(
          this.staffToken(req),
          sessionId,
          storeIdentity,
        ),
      });
    } catch (error) {
      this.sendError(res, error, this.statusFor(error));
    }
  }

  getOrder(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(
        this.service.getOrderDetail(
          this.staffToken(req),
          sessionId,
          String(req.params.orderId),
        ),
      );
    } catch (error) {
      this.sendError(res, error, this.statusFor(error));
    }
  }

  markPreparing(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      const storeIdentity = String(req.body.storeIdentity ?? req.query.store ?? '');
      res.json({
        order: this.service.markPreparing(
          this.staffToken(req),
          sessionId,
          String(req.params.orderId),
          storeIdentity,
        ),
      });
    } catch (error) {
      this.sendError(res, error, this.statusFor(error));
    }
  }

  fulfillOrder(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(
        this.service.fulfillOrder(
          this.staffToken(req),
          sessionId,
          String(req.params.orderId),
        ),
      );
    } catch (error) {
      this.sendError(res, error, this.statusFor(error));
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

  private statusFor(error: unknown): number {
    if (error instanceof Error) {
      if (error.message.includes('customer role')) return 403;
      if (error.message.includes('employee access denied')) return 403;
    }
    return 422;
  }

  private sendError(res: Response, error: unknown, status = 422): void {
    if (error instanceof Error) {
      res.status(status).json({ error: error.message });
      return;
    }
    res.status(500).json({ error: 'unexpected error' });
  }
}
