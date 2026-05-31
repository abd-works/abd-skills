import type { GuestCheckout } from './guest-checkout';

/** Pickup store commitment for checkout (distinct from browse Selected Store). */
export class PickupStore {
  readonly storeIdentity: string;
  readonly storeAddress: string;

  constructor(storeIdentity: string, storeAddress: string) {
    this.storeIdentity = storeIdentity;
    this.storeAddress = storeAddress;
  }

  bindToCheckoutSessionOnSelection(guestCheckout: GuestCheckout): PickupStore {
    guestCheckout.clickAndCollectStore = this;
    return this;
  }

  showStoreIdentityAndAddress(): string {
    return `${this.storeIdentity} — ${this.storeAddress}`;
  }

  attachToPlacedOrderOnSuccess(order: { clickAndCollectStore: PickupStore | null }): void {
    order.clickAndCollectStore = this;
  }

  static blockPaymentUntilStoreChosen(guestCheckout: GuestCheckout): boolean {
    return guestCheckout.clickAndCollectStore != null;
  }
}
