import type { CustomerLocation as CustomerLocationDto } from '../types';
import { DistanceToStore } from './distance-to-store';
import type { Customer } from './customer';
import { SelectedStore } from './selected-store';
import { Store } from './store';
import { StoreMapEntry } from './store-map-entry';
import type { Stores } from './stores';

/** << Service >> — map-centric store discovery presentation. */
export class StoreMap {
  private readonly distanceToStore = new DistanceToStore();

  constructor(readonly stores: Stores) {}

  showEveryStoreAsSelectableLocation(
    customer?: Customer,
    customerLocation: CustomerLocationDto | null = customer?.customerLocation.toDto() ?? null,
  ): StoreMapEntry[] {
    const ordered = customerLocation
      ? this.stores.sortNearestFirst(customerLocation)
      : this.stores.presentAllLocationsTogether();
    return ordered.map((store) =>
      StoreMapEntry.fromStore(
        store,
        this.distanceToStore.distanceKmForStore(store.id, customerLocation),
      ),
    );
  }

  presentAllLocationsTogether(): Store[] {
    return this.stores.presentAllLocationsTogether();
  }

  supportStoreSelection(
    customer: Customer,
    store: Store,
    selectedStore: SelectedStore,
  ): SelectedStore {
    const chosen = selectedStore.setFromStoreMap(customer, store);
    customer.selectedStore = chosen;
    return chosen;
  }

  omitStockAvailabilityBeforeSelectedStore(selectedStore: SelectedStore): void {
    if (selectedStore.isUnset()) {
      return;
    }
  }
}
