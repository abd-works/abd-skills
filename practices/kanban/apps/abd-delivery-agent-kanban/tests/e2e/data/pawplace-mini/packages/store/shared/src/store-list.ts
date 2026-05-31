import type { CustomerLocation as CustomerLocationDto } from '../types';
import { DistanceToStore } from './distance-to-store';
import type { Customer } from './customer';
import { SelectedStore } from './selected-store';
import { Store } from './store';
import { StoreListRow } from './store-list-row';
import type { Stores } from './stores';
import type { StoreMap } from './store-map';

/** << Service >> — list-centric store discovery presentation. */
export class StoreList {
  private readonly distanceToStore = new DistanceToStore();

  constructor(readonly stores: Stores) {}

  showAsAlternativeToStoreMap(): StoreList {
    return this;
  }

  presentReadableComparisonRows(
    customer?: Customer,
    customerLocation: CustomerLocationDto | null = customer?.customerLocation.toDto() ?? null,
  ): StoreListRow[] {
    const ordered = customerLocation
      ? this.stores.sortNearestFirst(customerLocation)
      : this.stores.presentAllLocationsTogether();
    return ordered.map((store) =>
      StoreListRow.fromStore(
        store,
        this.distanceToStore.distanceKmForStore(store.id, customerLocation),
      ),
    );
  }

  preserveDiscoveryContextOnMapSwitch(_customer: Customer, storeMap: StoreMap): void {
    storeMap.presentAllLocationsTogether();
  }

  showEveryStoreBeforeSelection(): Store[] {
    return this.stores.everyRetailLocation.slice();
  }

  supportStoreSelection(
    customer: Customer,
    store: Store,
    selectedStore: SelectedStore,
  ): SelectedStore {
    const chosen = selectedStore.setFromStoreList(customer, store);
    customer.selectedStore = chosen;
    return chosen;
  }

  omitStockAvailabilityBeforeSelectedStore(selectedStore: SelectedStore): void {
    if (selectedStore.isUnset()) {
      return;
    }
  }
}
