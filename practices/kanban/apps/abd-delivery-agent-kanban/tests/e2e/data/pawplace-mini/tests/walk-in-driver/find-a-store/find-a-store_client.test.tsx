/**
 * Find a store — client acceptance tests (Increment 1 Sprint 1).
 *
 * Story path: Walk-in driver → Find a store → [Story]
 * File: tests/walk-in-driver/find-a-store/find-a-store_client.test.tsx
 *
 * Source: docs/increments/1-walk-in-driver/specification/specification-by-example.md
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import { FindAStoreClientHelper } from './helpers/find-a-store.client';
import { FindAStoreBaseHelper } from './helpers/find-a-store.base';

describe('View Store Map', () => {
  const helper = new FindAStoreClientHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: every store appears as a selectable location on the store map', async () => {
    await helper.whenCustomerOpensStoreMap();
    helper.thenEveryStoreVisibleOnMap();
    helper.thenStoresPresentedWithoutSearchOrFilter();
  });

  it('Scenario 2: store selection on the map sets the selected store', async () => {
    const store = FindAStoreBaseHelper.STORE_WESTSIDE;
    await helper.whenCustomerOpensStoreMap();
    await helper.whenCustomerSelectsStoreOnMap(store.retailLocationIdentity);
    helper.thenSelectedStoreDetailVisible(
      store.retailLocationIdentity,
      store.geographicPlacement,
    );
  });

  it('Scenario 3: store map omits stock availability before a selected store exists', async () => {
    await helper.whenCustomerOpensStoreMap();
    helper.thenNoStockAvailabilityOnMap();
  });

  it('Scenario 4: multiple stores require no prior search or filter', async () => {
    await helper.whenCustomerOpensStoreMap();
    helper.thenEveryStoreVisibleOnMap();
    helper.thenNoSearchOrFilterAffordance();
  });
});

describe('View Store List', () => {
  const helper = new FindAStoreClientHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: store list offers an alternative to the store map', async () => {
    await helper.whenCustomerOpensStoreList();
    helper.thenStoreListShowsAllStores();
    helper.thenListRowShowsStoreDetails(
      FindAStoreBaseHelper.STORE_DOWNTOWN.retailLocationIdentity,
      FindAStoreBaseHelper.STORE_DOWNTOWN.geographicPlacement,
    );
  });

  it('Scenario 2: store selection from the list sets the selected store', async () => {
    const store = FindAStoreBaseHelper.STORE_DOWNTOWN;
    await helper.whenCustomerOpensStoreList();
    await helper.whenCustomerSelectsStoreOnList(store.retailLocationIdentity);
    await helper.whenCustomerClicksSelectStore();
    helper.thenNavigatedToCatalogScopedTo(store);
  });

  it('Scenario 3: store list rows are readable and map switch preserves discovery context', async () => {
    await helper.whenCustomerOpensStoreList();
    helper.thenStoreListShowsAllStores();
    await helper.whenCustomerSwitchesToMapTab();
    helper.thenMapTabPreservesStoreSet();
    await helper.whenCustomerSwitchesToListTab();
    helper.thenStoreListShowsAllStores();
  });

  it('Scenario 4: store list hides stock availability until a selected store is set', async () => {
    await helper.whenCustomerOpensStoreList();
    helper.thenStoreListOmitsStockAvailability();
  });
});

describe('Calculate Distance to Store', () => {
  const helper = new FindAStoreClientHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: shared location ranks stores nearest first on map and list', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerOpensStoreList();
    await helper.whenCustomerClicksUseMyLocation();
    helper.thenStoresRankedNearestFirst([
      'Downtown PawPlace',
      'Westside PawPlace',
      'Uptown PawPlace',
    ]);
    helper.thenDistanceShownForStore('Downtown PawPlace', 2.1);
    helper.thenDistanceShownForStore('Westside PawPlace', 4.8);
  });

  it('Scenario 2: stores remain visible without distance values when location is not shared', async () => {
    await helper.whenCustomerOpensStoreMap();
    helper.thenNoDistanceValuesShown();
    await helper.whenCustomerSwitchesToListTab();
    helper.thenNoDistanceValuesShown();
  });

  it('Scenario 3: nearest store is easy to spot when ranking is active', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerOpensStoreListWithLocation();
    helper.thenFirstListRowIs('Downtown PawPlace', 2.1);
  });

  it('Scenario 4: changed location recalculates distance and resort order', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerOpensStoreListWithLocation();
    helper.thenFirstListRowIs('Downtown PawPlace', 2.1);
    await helper.whenCustomerSharesAlternateLocation();
    helper.thenFirstListRowIs('Westside PawPlace', 1.4);
    helper.thenDistanceShownForStore('Downtown PawPlace', 3.2);
  });
});
