/**
 * DomainName.ts — Entity and Value Objects for the domain module.
 *
 * Replace 'DomainName' with your entity (PascalCase): Recipient, Payment, Invoice.
 * This file lives in packages/{domainName}/shared/ and has ZERO framework imports.
 */

// ============================================================================
// VALUE OBJECT: DomainNameStatus
// ============================================================================

export type DomainNameStatusType = 'Active' | 'Pending' | 'Inactive';

export class DomainNameStatus {
  constructor(
    public readonly status: DomainNameStatusType,
    public readonly createdAt: Date
  ) {}

  isEligibleForPayment(): boolean {
    return this.status === 'Active';
  }

  isPending(): boolean {
    return this.status === 'Pending';
  }
}

// ============================================================================
// ENTITY: DomainName
// ============================================================================

export interface DomainName {
  id: string;
  enterpriseId: string;
  name: string;
  status: DomainNameStatus;
  createdAt: Date;
}
