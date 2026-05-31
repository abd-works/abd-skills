/**
 * Find a store — E2E acceptance tests (Increment 1 Sprint 1).
 *
 * Story path: Walk-in driver → Find a store → [Story]
 * File: tests/walk-in-driver/find-a-store/find-a-store_e2e.spec.ts
 *
 * Source: docs/increments/1-walk-in-driver/specification/specification-by-example.md
 */
import { test } from '@playwright/test';
import { FindAStoreE2EHelper } from './helpers/find-a-store.e2e';
import { FindAStoreBaseHelper } from './helpers/find-a-store.base';

test.describe('View Store Map — E2E', () => {
  const helper = new FindAStoreE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 1: every store appears as a selectable location on the store map', async () => {
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
    await helper.whenCustomerCompletesStoreMapDiscoveryFlow();
    helper.thenBrowserShowsExpectedStoreDiscoveryState(
      'Store Map shows Downtown PawPlace, Westside PawPlace, and Uptown PawPlace without search or filter',
    );
  });

  test('Scenario 2: store selection on the map sets the selected store', async () => {
    const store = FindAStoreBaseHelper.STORE_WESTSIDE;
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
    await helper.whenCustomerCompletesStoreSelectionOnMapFlow(store);
    helper.thenBrowserShowsExpectedStoreDiscoveryState(
      'Selected Store is Westside PawPlace with geographic placement 456 Oak Ave',
    );
  });
});

test.describe('View Store List — E2E', () => {
  const helper = new FindAStoreE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 2: store selection from the list sets the selected store', async () => {
    const store = FindAStoreBaseHelper.STORE_DOWNTOWN;
    await helper.givenCustomerAlexRiveraHasNoSelectedStore();
    await helper.whenCustomerCompletesStoreSelectionOnListFlow(store);
    helper.thenBrowserShowsExpectedStoreDiscoveryState(
      'customer proceeds to catalog scoped to Downtown PawPlace',
    );
  });
});

test.describe('Calculate Distance to Store — E2E', () => {
  const helper = new FindAStoreE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 1: shared location ranks stores nearest first on map and list', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerCompletesStoreListDiscoveryFlow();
    helper.thenBrowserShowsExpectedStoreDiscoveryState(
      'Store List ranks Downtown PawPlace first at 2.1 km',
    );
  });

  test('Scenario 4: changed location recalculates distance and resort order', async () => {
    await helper.givenCustomerAlexRiveraSharesPrimaryLocation();
    await helper.whenCustomerCompletesShareLocationFlow(43.7, -79.4);
    helper.thenBrowserShowsExpectedStoreDiscoveryState(
      'Westside PawPlace ranks first at 1.4 km after location change',
    );
  });
});
