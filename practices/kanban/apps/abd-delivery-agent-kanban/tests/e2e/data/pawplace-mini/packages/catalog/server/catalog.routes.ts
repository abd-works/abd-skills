import { Router } from 'express';
import { CatalogApi } from './catalog.api';

export function createCatalogRouter(api: CatalogApi): Router {
  const router = Router();
  router.get('/catalog', (req, res) => api.getCatalogBrowse(req, res));
  router.get('/catalog/products/:catalogItemIdentity', (req, res) => api.getProductDetail(req, res));
  router.get('/inventory/stock-maintenance', (req, res) => api.getStockMaintenance(req, res));
  router.post('/inventory/stock-levels', (req, res) => api.saveStockLevels(req, res));
  return router;
}
