/**
 * domainName.routes.ts — Express router factory.
 *
 * Route paths use kebab-case of the domain verb:
 *   listDomainNames  → GET  /
 *   getDomainName    → GET  /:id
 *   createDomainName → POST /
 *
 * For domain-specific mutations, the verb becomes the path:
 *   toggleMode       → POST /toggle-mode
 *   moveToStage      → POST /move-to-stage
 *
 * IMPORTANT: Every route defined here must have a corresponding API function
 * in the client's domainName.api.ts with the SAME domain verb name.
 */
import { Router } from 'express';
import { DomainNamesController } from './domainName.controller';

export function createDomainNamesRouter(controller: DomainNamesController): Router {
  const router = Router();
  router.get('/', (req, res) => controller.listDomainNames(req, res));
  router.get('/:id', (req, res) => controller.getDomainName(req, res));
  router.post('/', (req, res) => controller.createDomainName(req, res));
  return router;
}
