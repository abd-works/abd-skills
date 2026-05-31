import type { Request, Response } from 'express';
import {
  addProductToCartBodySchema,
  updateCartQuantityBodySchema,
} from '../shared/src/cart.schema';
import { CartService } from './cart.service';

export class CartApi {
  constructor(private readonly service: CartService) {}

  createSession(req: Request, res: Response): void {
    const displayName = String(req.body?.displayName ?? 'Guest');
    const selectedStoreIdentity = String(req.body?.selectedStoreIdentity ?? '');
    const sessionId = String(req.headers['x-session-id'] ?? crypto.randomUUID());
    const cart = this.service.createGuestSession(
      sessionId,
      displayName,
      selectedStoreIdentity,
    );
    res.status(201).json({ sessionId, cart });
  }

  getCart(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    res.json(this.service.getShoppingCart(sessionId));
  }

  addLine(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const parsed = addProductToCartBodySchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: parsed.error.issues[0]?.message ?? 'invalid body' });
      return;
    }
    try {
      const cart = this.service.addProductToCart(
        sessionId,
        parsed.data.catalogItemIdentity,
      );
      res.status(201).json(cart);
    } catch (error) {
      this.sendDomainError(res, error);
    }
  }

  updateLine(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    const parsed = updateCartQuantityBodySchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: parsed.error.issues[0]?.message ?? 'invalid body' });
      return;
    }
    try {
      const cart = this.service.updateCartQuantity(
        sessionId,
        String(req.params.catalogItemIdentity),
        parsed.data.cartQuantity,
      );
      res.json(cart);
    } catch (error) {
      this.sendDomainError(res, error);
    }
  }

  removeLine(req: Request, res: Response): void {
    const sessionId = this.requireSessionId(req, res);
    if (!sessionId) return;
    try {
      const cart = this.service.removeProductFromCart(
        sessionId,
        String(req.params.catalogItemIdentity),
      );
      res.json(cart);
    } catch (error) {
      this.sendDomainError(res, error);
    }
  }

  listCatalog(req: Request, res: Response): void {
    const storeIdentity = String(req.query.store ?? '');
    res.json({ products: this.service.listCatalogForStore(storeIdentity) });
  }

  private requireSessionId(req: Request, res: Response): string | undefined {
    const sessionId = req.headers['x-session-id'];
    if (!sessionId || Array.isArray(sessionId)) {
      res.status(401).json({ error: 'x-session-id required' });
      return undefined;
    }
    return sessionId;
  }

  private sendDomainError(res: Response, error: unknown): void {
    if (error instanceof Error) {
      res.status(422).json({ error: error.message });
      return;
    }
    res.status(500).json({ error: 'unexpected error' });
  }
}
