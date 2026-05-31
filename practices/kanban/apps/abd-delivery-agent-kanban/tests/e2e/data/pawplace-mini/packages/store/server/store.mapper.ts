import type { Customer } from '../shared/src/customer';
import type { StoreListRow } from '../shared/src/store-list-row';
import type { StoreMapEntry } from '../shared/src/store-map-entry';
import type { Store } from '../shared/src/store';
import type {
  DiscoverySessionDto,
  SelectStoreResponseDto,
  StoreListViewDto,
  StoreMapViewDto,
} from '../shared/src/store.schema';
import type { StoreRecord } from '../shared/types';

export function toStoreRecordDto(store: Store): StoreRecord {
  return {
    id: store.id,
    retailLocationIdentity: store.retailLocationIdentity,
    geographicPlacement: store.geographicPlacement.streetAddress,
  };
}

export function toStoreWithDistanceDto(
  entry: StoreMapEntry | StoreListRow,
): StoreRecord & { distanceToStoreKm?: number; stockAvailabilityShown: boolean } {
  return {
    ...toStoreRecordDto(entry.store),
    distanceToStoreKm: entry.distanceToStoreKm,
    stockAvailabilityShown: entry.stockAvailabilityShown,
  };
}

export function toStoreMapViewDto(entries: StoreMapEntry[]): StoreMapViewDto {
  return {
    entries: entries.map(toStoreWithDistanceDto),
    allStoresPresentedWithoutSearchOrFilter: entries.length >= 3,
    stockAvailabilityShown: entries.some((entry) => entry.stockAvailabilityShown),
  };
}

export function toStoreListViewDto(rows: StoreListRow[]): StoreListViewDto {
  return {
    rows: rows.map(toStoreWithDistanceDto),
    alternativeToMap: true,
    stockAvailabilityShown: rows.some((row) => row.stockAvailabilityShown),
  };
}

export function toDiscoverySessionDto(
  customer: Customer,
  activeView: 'map' | 'list' | null,
): DiscoverySessionDto {
  return {
    displayName: customer.displayName,
    selectedStore: customer.selectedStore.isUnset()
      ? null
      : toStoreRecordDto(customer.selectedStore),
    customerLocation: customer.customerLocation.toDto(),
    activeView,
    catalogScope: customer.selectedStore.isUnset()
      ? null
      : customer.selectedStore.scopesCatalogBrowse(),
  };
}

export function toSelectStoreResponseDto(customer: Customer): SelectStoreResponseDto {
  return {
    selectedStore: toStoreRecordDto(customer.selectedStore),
    catalogScope: customer.selectedStore.scopesCatalogBrowse(),
  };
}
