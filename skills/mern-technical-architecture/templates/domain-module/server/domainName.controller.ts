/**
 * domainName.controller.ts — HTTP parsing and response formatting.
 *
 * Extracts request data, delegates to the service, formats the response.
 * No business logic here — that lives in shared/ domain classes.
 */
import { Request, Response } from 'express';
import { DomainNamesService } from './domainName.service';

export class DomainNamesController {
  constructor(private service: DomainNamesService) {}

  async list(req: Request, res: Response): Promise<void> {
    const enterpriseId = req.user!.enterpriseId;
    const activeOnly = req.query.activeOnly === 'true';
    const items = await this.service.getDomainNames(enterpriseId, { activeOnly });
    res.json({ items, total: items.length });
  }
}
