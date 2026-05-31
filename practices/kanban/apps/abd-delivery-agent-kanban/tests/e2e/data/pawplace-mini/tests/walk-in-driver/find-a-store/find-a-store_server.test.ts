/**
 * Find a store — server acceptance tests (Increment 1 Sprint 1).
 *
 * Story path: Walk-in driver → Find a store → [Story]
 * File: tests/walk-in-driver/find-a-store/find-a-store_server.test.ts
 *
 * Source: docs/increments/1-walk-in-driver/specification/specification-by-example.md
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import { FindAStoreServerHelper } from './helpers/find-a-store.server';
import { FindAStoreBaseHelper } from './helpers/find-a-store.base';

describe('View Store Map', () => {
  const helper = new FindAStoreServerHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: every store appears as a selectable location on the store map', async () => {
    await helper.whenCustomerOpensStoreMapViaApi();
    helper.thenStoreMapShowsEveryStoreAsSelectable();
    helper.thenStoresPresentedWithoutSearchOrFilter();
  });

  it('Scenario 2: store selection on the map sets the selected store', async () => {
    const store = FindAStoreBaseHelper.STORE_WESTSIDE;
    await helper.whenCustomerOpensStoreMapViaApi();
    await helper.whenCustomerSelectsStoreOnMapViaApi(store);
    helper.thenSelectedStoreIs(store);
  });

  it('Scenario 3: store map omits stock availability before a selected store exists', async () => {
    await helper.whenCustomerOpensStoreMapViaApi();
    helper.thenStoreMapOmitsStockAvailability();
  });

  it('Scenario 4: multiple stores require no prior search or filter', async () => {
    await helper.whenCustomerOpensStoreMapViaApi();
    helper.thenStoresPresentedWithoutSearchOrFilter();
  });
});

describe('View Store List', () => {
  const helper = new FindAStoreServerHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: store list offers an alternative to the store map', async () => {
    await helper.whenCustomerOpensStoreListViaApi();
    helper.thenStoreListShowsAlternativeToMap();
  });

  it('Scenario 2: store selection from the list sets the selected store', async () => {
    const store = FindAStoreBaseHelper.STORE_DOWNTOWN;
    await helper.whenCustomerOpensStoreListViaApi();
    await helper.whenCustomerSelectsStoreOnListViaApi(store);
    helper.thenSelectedStoreIs(store);
    helper.thenCustomerCanProceedToCatalogScopedTo(store);
  });

  it('Scenario 3: store list rows are readable and map switch preserves discovery context', async () => {
    await helper.whenCustomerOpensStoreListViaApi();
    helper.thenStoreListShowsAlternativeToMap();
    await helper.whenCustomerSwitchesToMapViewViaApi();
    helper.thenMapSwitchPreservesDiscoveryContext();
  });

  it('Scenario 4: store list hides stock availability until a selected store is set', async () => {
    await helper.whenCustomerOpensStoreListViaApi();
    helper.thenStoreListOmitsStockAvailability();
  });
});

describe('Calculate Distance to Store', () => {
  const helper = new FindAStoreServerHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: shared location ranks stores nearest first on map and list', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerOpensStoreListViaApi();
    helper.thenStoresRankedNearestFirst(
      ['Downtown PawPlace', 'Westside PawPlace', 'Uptown PawPlace'],
      [2.1, 4.8, 6.3],
    );
  });

  it('Scenario 2: stores remain visible without distance values when location is not shared', async () => {
    await helper.whenCustomerOpensStoreMapViaApi();
    helper.thenNoDistanceValuesOnMapOrList();
    await helper.whenCustomerOpensStoreListViaApi();
    helper.thenNoDistanceValuesOnMapOrList();
  });

  it('Scenario 3: nearest store is easy to spot when ranking is active', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerOpensStoreListViaApi();
    helper.thenFirstStoreRowIs('Downtown PawPlace', 2.1);
  });

  it('Scenario 4: changed location recalculates distance and resort order', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerOpensStoreListViaApi();
    helper.thenFirstStoreRowIs('Downtown PawPlace', 2.1);
    await helper.whenCustomerSharesLocationViaApi(43.7, -79.4);
    helper.thenDistanceRankingRecalculatedForAlternateLocation();
    helper.thenFirstStoreRowIs('Westside PawPlace', 1.4);
    helper.thenStoresRankedNearestFirst(
      ['Westside PawPlace', 'Downtown PawPlace', 'Uptown PawPlace'],
      [1.4, 3.2, 5.6],
    );
  });
});
