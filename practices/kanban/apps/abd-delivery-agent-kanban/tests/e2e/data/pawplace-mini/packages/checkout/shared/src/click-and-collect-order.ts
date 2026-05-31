import type { CartLine, Money } from '@pawplace-mini/cart-shared';
import type { BillingAddress } from './billing-address';
import type { PaymentMethod } from './payment-method';
import type { GuestCheckout } from './guest-checkout';
import type { PickupStore } from './pickup-store';

const FIXTURE_ORDER_ID = 'CNC-1042';

/** << Entity >> — paid click-and-collect order. */
export class ClickAndCollectOrder {
  readonly orderId: string;
  readonly customerContact: string;
  clickAndCollectStore: PickupStore | null;
  readonly cartLines: readonly CartLine[];
  billingAddress: BillingAddress | null;
  paymentMethod: PaymentMethod | null;
  readonly orderTotal: Money;
  paymentConfirmed = false;
  guestOnly = false;

  constructor(
    orderId: string,
    customerContact: string,
    clickAndCollectStore: PickupStore | null,
    cartLines: readonly CartLine[],
    billingAddress: BillingAddress | null,
    paymentMethod: PaymentMethod | null,
    orderTotal: Money,
  ) {
    this.orderId = orderId;
    this.customerContact = customerContact;
    this.clickAndCollectStore = clickAndCollectStore;
    this.cartLines = cartLines;
    this.billingAddress = billingAddress;
    this.paymentMethod = paymentMethod;
    this.orderTotal = orderTotal;
  }

  static originateFromCompletedGuestCheckout(
    guestCheckout: GuestCheckout,
    shoppingCart: { handOffLinesToGuestCheckout(): readonly CartLine[]; calculateOrderTotal(): Money },
  ): ClickAndCollectOrder {
    const placedOrder = new ClickAndCollectOrder(
      FIXTURE_ORDER_ID,
      guestCheckout.email,
      guestCheckout.clickAndCollectStore,
      shoppingCart.handOffLinesToGuestCheckout(),
      guestCheckout.billingAddress,
      guestCheckout.paymentMethod,
      shoppingCart.calculateOrderTotal(),
    );
    placedOrder.paymentConfirmed = true;
    placedOrder.guestOnly = true;
    return placedOrder;
  }

  referenceExactlyOnePickupStore(clickAndCollectStore: PickupStore): void {
    this.clickAndCollectStore = clickAndCollectStore;
  }
}
