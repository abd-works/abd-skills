/**
 * domainName.controller.ts — HTTP parsing and response formatting.
 *
 * Extracts request data, delegates to the service, formats the response.
 * No business logic here — that lives in shared/ domain classes.
 *
 * IMPORTANT: Every route in domainName.routes.ts must have a corresponding
 * controller method. If the router defines GET /:id and POST /, this
 * controller must have getById() and create() methods.
 */
import { Request, Response } from 'express';
import { CreateDomainNameInputSchema } from '@appName/domainName-shared';
import { DomainNamesService } from './domainName.service';

export class DomainNamesController {
  constructor(private service: DomainNamesService) {}

  async list(req: Request, res: Response): Promise<void> {
    const enterpriseId = req.user!.enterpriseId;
    const activeOnly = req.query.activeOnly === 'true';
    const items = await this.service.getDomainNames(enterpriseId, { activeOnly });
    res.json({ items, total: items.length });
  }

  async getById(req: Request, res: Response): Promise<void> {
    const item = await this.service.getById(req.params.id);
    if (!item) {
      res.status(404).json({ error: 'Not found' });
      return;
    }
    res.json(item);
  }

  async create(req: Request, res: Response): Promise<void> {
    const validation = CreateDomainNameInputSchema.safeParse(req.body);
    if (!validation.success) {
      res.status(400).json({ error: validation.error.issues[0].message });
      return;
    }
    const enterpriseId = req.user!.enterpriseId;
    const created = await this.service.create(enterpriseId, validation.data);
    res.status(201).json(created);
  }
}
