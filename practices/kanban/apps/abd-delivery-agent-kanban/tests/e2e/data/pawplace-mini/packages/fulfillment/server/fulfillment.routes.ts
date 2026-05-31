import { Router } from 'express';
import { FulfillmentApi } from './fulfillment.api';

export function createFulfillmentRouter(api: FulfillmentApi): Router {
  const router = Router();
  router.get('/fulfillment/queue', (req, res) => api.listQueue(req, res));
  router.get('/fulfillment/orders/:orderId', (req, res) => api.getOrder(req, res));
  router.post('/fulfillment/orders/:orderId/prepare', (req, res) =>
    api.markPreparing(req, res),
  );
  router.post('/fulfillment/orders/:orderId/fulfill', (req, res) =>
    api.fulfillOrder(req, res),
  );
  return router;
}
