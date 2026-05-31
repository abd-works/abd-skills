/**
 * Find a store — domain acceptance tests (packages/store/shared).
 * Increment 1 Sprint 1 — typed domain surface from object-model.md.
 */
import { describe, it } from 'vitest';
import assert from 'node:assert/strict';
import {
  ALTERNATE_CUSTOMER_LOCATION,
  PRIMARY_CUSTOMER_LOCATION,
} from '../mockStores';
import {
  Customer,
  DistanceToStore,
  SelectedStore,
  Stores,
} from '../src/index';

describe('View Store Map (domain)', () => {
  it('Scenario 2: store selection on the map sets the selected store', () => {
    const stores = Stores.supplyDiscoveryInventory();
    const customer = new Customer('Alex Rivera');

    customer.selectStoreFromMap(
      stores.everyRetailLocation[1]!,
      stores.storeMap,
      customer.selectedStore,
    );

    assert.equal(customer.selectedStore.retailLocationIdentity, 'Westside PawPlace');
    assert.equal(customer.selectedStore.isUnset(), false);
  });

  it('Scenario 3: store map omits stock availability before a selected store exists', () => {
    const stores = Stores.supplyDiscoveryInventory();
    const customer = new Customer('Alex Rivera');
    const selectedStore = SelectedStore.unset();

    stores.storeMap.omitStockAvailabilityBeforeSelectedStore(selectedStore);
    const entries = stores.storeMap.showEveryStoreAsSelectableLocation(customer);

    assert.ok(entries.every((entry) => entry.stockAvailabilityShown === false));
  });
});

describe('View Store List (domain)', () => {
  it('Scenario 2: store selection from the list sets the selected store', () => {
    const stores = Stores.supplyDiscoveryInventory();
    const customer = new Customer('Alex Rivera');

    customer.selectStoreFromList(
      stores.everyRetailLocation[0]!,
      stores.storeList,
      customer.selectedStore,
    );

    assert.equal(customer.selectedStore.retailLocationIdentity, 'Downtown PawPlace');
  });

  it('Scenario 4: store list hides stock availability until a selected store is set', () => {
    const stores = Stores.supplyDiscoveryInventory();
    const customer = new Customer('Alex Rivera');
    const selectedStore = SelectedStore.unset();

    stores.storeList.omitStockAvailabilityBeforeSelectedStore(selectedStore);
    const rows = stores.storeList.presentReadableComparisonRows(customer);

    assert.ok(rows.every((row) => row.stockAvailabilityShown === false));
  });
});

describe('Calculate Distance to Store (domain)', () => {
  it('Scenario 1: shared location ranks stores nearest first on map and list', () => {
    const stores = Stores.supplyDiscoveryInventory();
    const distanceToStore = new DistanceToStore();

    const ranked = distanceToStore.sortStoresNearestFirst(
      stores.everyRetailLocation,
      PRIMARY_CUSTOMER_LOCATION,
    );

    assert.deepEqual(
      ranked.map((store) => store.retailLocationIdentity),
      ['Downtown PawPlace', 'Westside PawPlace', 'Uptown PawPlace'],
    );
    assert.equal(
      distanceToStore.distanceKmForStore(ranked[0]!.id, PRIMARY_CUSTOMER_LOCATION),
      2.1,
    );
  });

  it('Scenario 2: stores remain visible without distance values when location is not shared', () => {
    const stores = Stores.supplyDiscoveryInventory();
    const distanceToStore = new DistanceToStore();
    const customer = new Customer('Alex Rivera');

    distanceToStore.omitDistanceValuesUntilLocationShared(customer);
    const rows = stores.storeList.presentReadableComparisonRows(customer);

    assert.equal(rows.length, 3);
    assert.ok(distanceToStore.distanceKmForStore(rows[0]!.store.id, null) == null);
  });

  it('Scenario 4: changed location recalculates distance and resort order', () => {
    const stores = Stores.supplyDiscoveryInventory();
    const distanceToStore = new DistanceToStore();
    const customer = new Customer('Alex Rivera');

    const primaryRank = distanceToStore.recalculateRankingOnLocationChange(
      customer,
      stores,
      PRIMARY_CUSTOMER_LOCATION,
    );
    const alternateRank = distanceToStore.recalculateRankingOnLocationChange(
      customer,
      stores,
      ALTERNATE_CUSTOMER_LOCATION,
    );

    assert.equal(primaryRank[0]!.retailLocationIdentity, 'Downtown PawPlace');
    assert.equal(alternateRank[0]!.retailLocationIdentity, 'Westside PawPlace');
    assert.equal(
      distanceToStore.distanceKmForStore(alternateRank[0]!.id, ALTERNATE_CUSTOMER_LOCATION),
      1.4,
    );
  });
});
