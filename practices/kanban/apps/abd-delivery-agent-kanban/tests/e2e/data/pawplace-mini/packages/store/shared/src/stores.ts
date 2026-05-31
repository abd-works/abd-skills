import { ALL_STORES } from '../mockStores';
import type { CustomerLocation as CustomerLocationDto } from '../types';
import { CustomerLocation } from './customer-location';
import { DistanceToStore } from './distance-to-store';
import { Store } from './store';
import { StoreList } from './store-list';
import { StoreMap } from './store-map';

/** << Entity >> — discovery inventory of every retail location. */
export class Stores {
  readonly everyRetailLocation: readonly Store[];
  readonly storeMap: StoreMap;
  readonly storeList: StoreList;
  readonly distanceToStore: DistanceToStore;

  constructor(
    everyRetailLocation: readonly Store[],
    distanceToStore: DistanceToStore = new DistanceToStore(),
  ) {
    this.everyRetailLocation = everyRetailLocation;
    this.distanceToStore = distanceToStore;
    this.storeMap = new StoreMap(this);
    this.storeList = new StoreList(this);
  }

  static supplyDiscoveryInventory(): Stores {
    const stores = ALL_STORES.map((record) => Store.fromRecord(record));
    return new Stores(stores);
  }

  sortNearestFirst(
    customerLocation: CustomerLocationDto | CustomerLocation,
  ): Store[] {
    return this.distanceToStore.sortStoresNearestFirst(
      this.everyRetailLocation,
      customerLocation,
    );
  }

  presentAllLocationsTogether(): Store[] {
    return [...this.everyRetailLocation];
  }
}
