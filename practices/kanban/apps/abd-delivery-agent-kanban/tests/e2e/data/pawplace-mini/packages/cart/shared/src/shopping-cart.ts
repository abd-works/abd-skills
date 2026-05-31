import type { Customer } from './customer';
import { CartLines } from './cart-lines';
import type { CartLine } from './cart-line';
import { Money } from './money';

/** << Entity >> — session-scoped shopping cart container. */
export class ShoppingCart {
  readonly cartLines: CartLines;
  readonly customer: Customer;

  constructor(customer: Customer) {
    this.customer = customer;
    this.cartLines = new CartLines();
  }

  showEachLineWithProductIdentity(): readonly CartLine[] {
    return this.cartLines.allLines();
  }

  showEditableCartQuantityPerLine(): readonly CartLine[] {
    return this.cartLines.allLines();
  }

  persistUpdatedCountsWhileBrowsing(): void {
    this.cartLines.persistCurrentState();
  }

  blockCheckoutEntryWhenEmpty(): boolean {
    return this.cartLines.isEmpty();
  }

  isEmpty(): boolean {
    return this.cartLines.isEmpty();
  }

  hasAtLeastOneLine(): boolean {
    return this.cartLines.lineCount() >= 1;
  }

  calculateOrderTotal(): Money {
    let total = Money.zero();
    for (const line of this.cartLines.allLines()) {
      total = total.add(line.lineTotalFromQuantity(line.product.unitPrice));
    }
    return total;
  }

  handOffLinesToGuestCheckout(): readonly CartLine[] {
    return this.cartLines.allLines();
  }

  clearAllLinesAfterPayment(): void {
    this.cartLines.clearAll();
  }
}
