import type { CustomerLocation as CustomerLocationDto } from '../types';
import { CustomerLocation } from './customer-location';
import { DistanceToStore } from './distance-to-store';
import { SelectedStore } from './selected-store';
import { Store } from './store';
import type { StoreList } from './store-list';
import type { StoreMap } from './store-map';
import type { Stores } from './stores';

/** << Entity >> — anonymous customer discovering and selecting a store. */
export class Customer {
  readonly displayName: string;
  customerLocation: CustomerLocation;
  selectedStore: SelectedStore;
  private readonly distanceToStore = new DistanceToStore();

  constructor(displayName: string, selectedStore: SelectedStore = SelectedStore.unset()) {
    this.displayName = displayName;
    this.customerLocation = CustomerLocation.empty();
    this.selectedStore = selectedStore;
  }

  openStoreMap(stores: Stores, storeMap: StoreMap) {
    return storeMap.showEveryStoreAsSelectableLocation(this);
  }

  openStoreList(stores: Stores, storeList: StoreList) {
    return storeList.presentReadableComparisonRows(this);
  }

  selectStoreFromMap(
    store: Store,
    storeMap: StoreMap,
    selectedStore: SelectedStore,
  ): SelectedStore {
    const chosen = storeMap.supportStoreSelection(this, store, selectedStore);
    this.selectedStore = chosen;
    return chosen;
  }

  selectStoreFromList(
    store: Store,
    storeList: StoreList,
    selectedStore: SelectedStore,
  ): SelectedStore {
    const chosen = storeList.supportStoreSelection(this, store, selectedStore);
    this.selectedStore = chosen;
    return chosen;
  }

  shareLocation(
    location: CustomerLocationDto,
    distanceToStore: DistanceToStore,
    stores: Stores,
  ): Store[] {
    this.customerLocation = CustomerLocation.fromDto(location);
    return distanceToStore.recalculateRankingOnLocationChange(
      this,
      stores,
      location,
    );
  }

  switchBetweenMapAndListViews(storeMap: StoreMap, storeList: StoreList): void {
    storeList.preserveDiscoveryContextOnMapSwitch(this, storeMap);
  }

  hasNotSharedLocation(): boolean {
    return this.customerLocation.isEmpty();
  }
}
