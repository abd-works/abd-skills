import { Router } from 'express';
import { StoreApi } from './store.api';

export function createStoreRouter(api: StoreApi): Router {
  const router = Router();
  router.post('/store-discovery/sessions', (req, res) => api.createDiscoverySession(req, res));
  router.get('/stores/map', (req, res) => api.getMap(req, res));
  router.get('/stores/list', (req, res) => api.getList(req, res));
  router.post('/stores/map/select', (req, res) => api.selectFromMap(req, res));
  router.post('/stores/list/select', (req, res) => api.selectFromList(req, res));
  router.post('/stores/location', (req, res) => api.shareLocation(req, res));
  router.get('/stores/map/switch', (req, res) => api.switchToMap(req, res));
  return router;
}
