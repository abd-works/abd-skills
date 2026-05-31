import { Money } from './money';

/** << Entity >> — catalog product referenced by cart lines. */
export class Product {
  readonly catalogItemIdentity: string;
  readonly unitPrice: Money;

  constructor(catalogItemIdentity: string, unitPrice: Money) {
    this.catalogItemIdentity = catalogItemIdentity;
    this.unitPrice = unitPrice;
  }

  equals(other: Product): boolean {
    return this.catalogItemIdentity === other.catalogItemIdentity;
  }
}
