/**
 * domainName.controller.ts — HTTP parsing and response formatting.
 *
 * Method names match the domain model verb exactly: if the domain says
 * toggleMode(), this controller has toggleMode(req, res).
 * No business logic here — that lives in shared/ domain classes.
 *
 * IMPORTANT: Every route in domainName.routes.ts must have a corresponding
 * controller method with the SAME domain verb name.
 */
import { Request, Response } from 'express';
import { CreateDomainNameInputSchema } from '@appName/domainName-shared';
import { DomainNamesService } from './domainName.service';

export class DomainNamesController {
  constructor(private service: DomainNamesService) {}

  async listDomainNames(req: Request, res: Response): Promise<void> {
    const enterpriseId = req.user!.enterpriseId;
    const activeOnly = req.query.active_only === 'true';
    const snapshot = await this.service.listDomainNames(enterpriseId, { activeOnly });
    res.json(snapshot);
  }

  async getDomainName(req: Request, res: Response): Promise<void> {
    const snapshot = await this.service.getDomainName(req.params.id);
    if (!snapshot) {
      res.status(404).json({ error: 'Not found' });
      return;
    }
    res.json(snapshot);
  }

  async createDomainName(req: Request, res: Response): Promise<void> {
    const validation = CreateDomainNameInputSchema.safeParse(req.body);
    if (!validation.success) {
      res.status(400).json({ error: validation.error.issues[0].message });
      return;
    }
    const enterpriseId = req.user!.enterpriseId;
    const snapshot = await this.service.createDomainName(enterpriseId, validation.data);
    res.status(201).json(snapshot);
  }
}
