/**
 * domainName.routes.ts — Express router factory.
 *
 * Maps URL paths to controller methods. Compose into the main app
 * with: app.use('/api/domainNames', createDomainNamesRouter(controller));
 */
import { Router } from 'express';
import { DomainNamesController } from './domainName.controller';

export function createDomainNamesRouter(controller: DomainNamesController): Router {
  const router = Router();
  router.get('/', (req, res) => controller.list(req, res));
  return router;
}
