import { ALL_STORES, rankStoresForLocation } from '../mockStores';
import type { CustomerLocation as CustomerLocationDto } from '../types';
import { CustomerLocation } from './customer-location';
import { Store } from './store';
import type { Customer } from './customer';
import type { Stores } from './stores';

function toLocationDto(
  location: CustomerLocationDto | CustomerLocation | null,
): CustomerLocationDto | null {
  if (location instanceof CustomerLocation) {
    return location.toDto();
  }
  return location;
}

/** << Service >> — proximity ranking when customer shares location. */
export class DistanceToStore {
  sortStoresNearestFirst(
    stores: readonly Store[],
    customerLocation: CustomerLocationDto | CustomerLocation,
  ): Store[] {
    const location = toLocationDto(customerLocation);
    if (!location) {
      return [...stores];
    }
    const ranked = rankStoresForLocation(location);
    const order = ranked.map((record) => record.id);
    return [...stores].sort((a, b) => order.indexOf(a.id) - order.indexOf(b.id));
  }

  omitDistanceValuesUntilLocationShared(
    customerOrLocation: Customer | CustomerLocation,
  ): void {
    const notShared =
      customerOrLocation instanceof CustomerLocation
        ? customerOrLocation.isEmpty()
        : customerOrLocation.hasNotSharedLocation();
    if (notShared) {
      return;
    }
  }

  recalculateRankingOnLocationChange(
    storesOrCustomer: readonly Store[] | Customer,
    locationOrStores?: CustomerLocation | CustomerLocationDto | Stores,
    newLocation?: CustomerLocationDto,
  ): Store[] {
    if (Array.isArray(storesOrCustomer) && locationOrStores instanceof CustomerLocation) {
      return this.sortStoresNearestFirst(storesOrCustomer, locationOrStores);
    }
    const customer = storesOrCustomer as Customer;
    const stores = locationOrStores as Stores;
    const location = newLocation!;
    customer.customerLocation = CustomerLocation.fromDto(location);
    return this.sortStoresNearestFirst(stores.everyRetailLocation, location);
  }

  distanceKmForStore(
    storeOrId: Store | string,
    location: CustomerLocationDto | CustomerLocation | null,
  ): number | undefined {
    const dto = toLocationDto(location);
    if (!dto) {
      return undefined;
    }
    const storeId = typeof storeOrId === 'string' ? storeOrId : storeOrId.id;
    const ranked = rankStoresForLocation(dto);
    return ranked.find((store) => store.id === storeId)?.distanceToStoreKm;
  }

  loadFixtureStores(): Store[] {
    return ALL_STORES.map((record) => Store.fromRecord(record));
  }
}
