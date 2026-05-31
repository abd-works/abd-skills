import type { Request, Response } from 'express';
import { CheckoutService } from './checkout.service';

export class CheckoutApi {
  constructor(private readonly service: CheckoutService) {}

  startGuestCheckout(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.status(201).json(this.service.startGuestCheckout(sessionId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  getSession(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(this.service.getCheckoutSession(sessionId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  selectStore(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const storeIdentity = String(req.body?.storeIdentity ?? '');
    const storeAddress = String(req.body?.storeAddress ?? '');
    try {
      res.json(
        this.service.selectClickAndCollectStore(sessionId, storeIdentity, storeAddress),
      );
    } catch (error) {
      this.sendError(res, error);
    }
  }

  enterBilling(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(
        this.service.enterBillingAddress(sessionId, {
          name: String(req.body?.name ?? ''),
          street: String(req.body?.street ?? ''),
          city: String(req.body?.city ?? ''),
          postalCode: String(req.body?.postalCode ?? ''),
          country: String(req.body?.country ?? ''),
        }),
      );
    } catch (error) {
      this.sendError(res, error);
    }
  }

  selectPaymentMethod(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const method = String(req.body?.method ?? 'card');
    try {
      res.json(this.service.selectPaymentMethod(sessionId, method));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  configureStripeWave(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const outcome = String(req.body?.outcome ?? 'success');
    this.service.configureStripeWaveOutcome(sessionId, outcome);
    res.status(204).send();
  }

  processPayment(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      res.json(this.service.processCardPayment(sessionId));
    } catch (error) {
      this.sendError(res, error);
    }
  }

  getConfirmation(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      const confirmation = this.service.getOrderConfirmation(sessionId);
      if (!confirmation) {
        res.status(404).json({ error: 'order confirmation not available' });
        return;
      }
      res.json(confirmation);
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
