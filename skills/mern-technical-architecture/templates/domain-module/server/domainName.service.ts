/**
 * domainName.service.ts — Application service (use-case orchestration).
 *
 * Coordinates repository + shared domain collection class.
 * No HTTP concerns — that's the controller's job.
 */
import { DomainName, DomainNames } from '@project/domainName/shared';
import { DomainNamesRepository } from './domainName.repository';

export class DomainNamesService {
  constructor(private repo: DomainNamesRepository) {}

  async getDomainNames(
    enterpriseId: string,
    filters?: { activeOnly?: boolean }
  ): Promise<DomainName[]> {
    const all = await this.repo.findByEnterprise(enterpriseId);
    let collection = new DomainNames(all);
    if (filters?.activeOnly) {
      collection = collection.filterByStatus('Active');
    }
    return collection.toArray();
  }

  async findByIds(ids: string[]): Promise<DomainName[]> {
    return this.repo.findByIds(ids);
  }
}
