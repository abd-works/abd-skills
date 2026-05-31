import { Money } from './money';

/** << Entity >> — catalog product for walk-in browse and stock visibility. */
export class Product {
  readonly catalogItemIdentity: string;
  readonly description: string;
  readonly unitPrice: Money;

  constructor(catalogItemIdentity: string, description: string, unitPrice: Money) {
    this.catalogItemIdentity = catalogItemIdentity;
    this.description = description;
    this.unitPrice = unitPrice;
  }
}
