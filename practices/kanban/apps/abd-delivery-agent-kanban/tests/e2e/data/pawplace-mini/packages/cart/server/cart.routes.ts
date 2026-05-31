import { Router } from 'express';
import { CartApi } from './cart.api';

export function createCartRouter(api: CartApi): Router {
  const router = Router();
  router.post('/sessions', (req, res) => api.createSession(req, res));
  router.get('/cart', (req, res) => api.getCart(req, res));
  router.post('/cart/lines', (req, res) => api.addLine(req, res));
  router.patch('/cart/lines/:catalogItemIdentity', (req, res) => api.updateLine(req, res));
  router.delete('/cart/lines/:catalogItemIdentity', (req, res) => api.removeLine(req, res));
  router.get('/cart/catalog', (req, res) => api.listCatalog(req, res));
  return router;
}
