import { PickupStore } from './pickup-store';
import type { GuestCheckout } from './guest-checkout';

/** << Service >> — select click-and-collect pickup store. */
export class SelectClickAndCollectStore {
  presentEligibleStoresAtCheckoutStart(
    stores: { storeIdentity: string; storeAddress: string }[],
  ): PickupStore[] {
    return stores.map(
      (store) => new PickupStore(store.storeIdentity, store.storeAddress),
    );
  }

  updateBindingWhenCustomerChangesStore(
    guestCheckout: GuestCheckout,
    store: { storeIdentity: string; storeAddress: string },
  ): PickupStore {
    const replacement = new PickupStore(store.storeIdentity, store.storeAddress);
    guestCheckout.clickAndCollectStore = replacement;
    return replacement;
  }
}
