/**
 * Store pickup — E2E acceptance tests (Increment 2 Sprint 3).
 *
 * Story path: Shop & Pay Online → Store pickup → [Story]
 * File: tests/shop-and-pay-online/store-pickup/store-pickup_e2e.spec.ts
 */
import { test } from '@playwright/test';
import { FulfillmentE2EHelper } from './helpers/fulfillment.e2e';
import { FulfillmentBaseHelper } from './helpers/fulfillment.base';

test.describe('Prepare Click-and-Collect Orders for Pickup — E2E', () => {
  const helper = new FulfillmentE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 1: employee fulfillment queue lists paid order', async () => {
    await helper.givenStoreEmployeeJordanKimBoundToDowntownPawPlace();
    await helper.givenSprint3BackgroundOrdersSeeded();
    await helper.whenStoreEmployeeOpensFulfillmentQueueInBrowser();
    helper.thenBrowserShowsOrderInFulfillmentQueue(FulfillmentBaseHelper.ORDER_CNC_1042);
  });

  test('Scenario 2: mark preparing updates queue status', async () => {
    await helper.givenStoreEmployeeJordanKimBoundToDowntownPawPlace();
    await helper.givenSprint3BackgroundOrdersSeeded();
    await helper.whenStoreEmployeeMarksOrderPreparingInBrowser(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenBrowserShowsOrderInFulfillmentQueue(FulfillmentBaseHelper.ORDER_CNC_1042);
  });
});
