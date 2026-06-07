/**
 * DomainNames.ts — Collection class with domain-oriented query methods.
 *
 * Wraps a DomainName[] array with fluent, chainable methods for filtering
 * and searching. Used identically on both client (in-memory filtering) and
 * server (post-repository filtering) — same logic, zero duplication.
 */
import { DomainName, DomainNameStatusType } from './DomainName';

export class DomainNames {
  constructor(private readonly items: DomainName[]) {}

  filterByStatus(status: DomainNameStatusType): DomainNames {
    return new DomainNames(this.items.filter(r => r.status.status === status));
  }

  search(query: string): DomainNames {
    const lower = query.toLowerCase();
    return new DomainNames(
      this.items.filter(r => r.name.toLowerCase().includes(lower))
    );
  }

  toArray(): DomainName[] {
    return [...this.items];
  }

  get length(): number {
    return this.items.length;
  }
}
