import { DistanceToStore } from '../shared/src/distance-to-store';
import { Stores } from '../shared/src/stores';
import type {
  DiscoverySessionDto,
  SelectStoreResponseDto,
  StoreListViewDto,
  StoreMapViewDto,
} from '../shared/src/store.schema';
import type { CustomerLocation as CustomerLocationDto } from '../shared/types';
import {
  toDiscoverySessionDto,
  toSelectStoreResponseDto,
  toStoreListViewDto,
  toStoreMapViewDto,
} from './store.mapper';
import { StoreRepository } from './store.repository';

export class StoreService {
  constructor(private readonly repository: StoreRepository) {}

  resetFixture(): void {
    this.repository.reset();
  }

  createDiscoverySession(
    sessionId: string,
    displayName: string,
    customerLocation?: CustomerLocationDto,
  ): DiscoverySessionDto {
    const record = this.repository.createDiscoverySession(
      sessionId,
      displayName,
      customerLocation,
    );
    return toDiscoverySessionDto(record.customer, record.activeView);
  }

  getStoreMap(sessionId: string): StoreMapViewDto {
    const record = this.requireSession(sessionId);
    record.activeView = 'map';
    const stores = Stores.supplyDiscoveryInventory();
    stores.storeMap.omitStockAvailabilityBeforeSelectedStore(record.customer.selectedStore);
    const entries = record.customer.openStoreMap(stores, stores.storeMap);
    return toStoreMapViewDto(entries);
  }

  getStoreList(sessionId: string): StoreListViewDto {
    const record = this.requireSession(sessionId);
    record.activeView = 'list';
    const stores = Stores.supplyDiscoveryInventory();
    stores.storeList.omitStockAvailabilityBeforeSelectedStore(record.customer.selectedStore);
    const rows = record.customer.openStoreList(stores, stores.storeList);
    return toStoreListViewDto(rows);
  }

  selectStoreFromMap(sessionId: string, storeId: string): SelectStoreResponseDto {
    const record = this.requireSession(sessionId);
    const stores = Stores.supplyDiscoveryInventory();
    const store = this.requireStore(stores, storeId);
    record.customer.selectStoreFromMap(store, stores.storeMap, record.customer.selectedStore);
    return toSelectStoreResponseDto(record.customer);
  }

  selectStoreFromList(sessionId: string, storeId: string): SelectStoreResponseDto {
    const record = this.requireSession(sessionId);
    const stores = Stores.supplyDiscoveryInventory();
    const store = this.requireStore(stores, storeId);
    record.customer.selectStoreFromList(store, stores.storeList, record.customer.selectedStore);
    return toSelectStoreResponseDto(record.customer);
  }

  shareLocation(
    sessionId: string,
    latitude: number,
    longitude: number,
  ): StoreListViewDto {
    const record = this.requireSession(sessionId);
    const stores = Stores.supplyDiscoveryInventory();
    const distanceToStore = new DistanceToStore();
    record.customer.shareLocation({ latitude, longitude }, distanceToStore, stores);
    return this.getStoreList(sessionId);
  }

  switchToMapView(sessionId: string): StoreMapViewDto {
    const record = this.requireSession(sessionId);
    const stores = Stores.supplyDiscoveryInventory();
    record.customer.switchBetweenMapAndListViews(stores.storeMap, stores.storeList);
    return this.getStoreMap(sessionId);
  }

  getDiscoverySession(sessionId: string): DiscoverySessionDto {
    const record = this.requireSession(sessionId);
    return toDiscoverySessionDto(record.customer, record.activeView);
  }

  private requireSession(sessionId: string) {
    const record = this.repository.findSession(sessionId);
    if (!record) {
      throw new Error(`store session not found: ${sessionId}`);
    }
    return record;
  }

  private requireStore(stores: Stores, storeId: string) {
    const store = stores.everyRetailLocation.find(
      (candidate) =>
        candidate.id === storeId ||
        candidate.retailLocationIdentity === storeId,
    );
    if (!store) {
      throw new Error(`store not found: ${storeId}`);
    }
    return store;
  }
}
