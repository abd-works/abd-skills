/**
 * domainName.routes.ts — Express router factory.
 *
 * Maps URL paths to controller methods. Compose into the main app
 * with: app.use('/api/domainNames', createDomainNamesRouter(controller));
 *
 * IMPORTANT: Every route defined here must have a corresponding API function
 * in the client's domainName.api.ts AND a UI control that calls it.
 * If a POST/PUT route exists but no client form or button triggers it,
 * users cannot reach that functionality through the UI.
 */
import { Router } from 'express';
import { DomainNamesController } from './domainName.controller';

export function createDomainNamesRouter(controller: DomainNamesController): Router {
  const router = Router();
  router.get('/', (req, res) => controller.list(req, res));
  router.get('/:id', (req, res) => controller.getById(req, res));
  router.post('/', (req, res) => controller.create(req, res));
  return router;
}
