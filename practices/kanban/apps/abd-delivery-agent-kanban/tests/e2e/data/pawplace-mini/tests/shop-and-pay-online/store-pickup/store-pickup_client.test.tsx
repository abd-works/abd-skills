/**
 * Store pickup — client acceptance tests (Increment 2 Sprint 3).
 *
 * Story path: Shop & Pay Online → Store pickup → [Story]
 * File: tests/shop-and-pay-online/store-pickup/store-pickup_client.test.tsx
 *
 * Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
 * Priors: abd-interface-design implementation (8/8 GREEN)
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import { FulfillmentClientHelper } from './helpers/fulfillment.client';
import { FulfillmentBaseHelper } from './helpers/fulfillment.base';

describe('Prepare Click-and-Collect Orders for Pickup — client', () => {
  const helper = new FulfillmentClientHelper();

  beforeEach(async () => {
    await helper.givenStoreEmployeeAtDowntown();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Prepare Click-and-Collect Orders for Pickup — AC 1: queue lists paid orders', async () => {
    await helper.whenEmployeeOpensFulfillmentQueue();
    helper.thenUiListsOrderInQueue(FulfillmentBaseHelper.ORDER_CNC_1042);
  });

  it('Prepare Click-and-Collect Orders for Pickup — AC 2: mark preparing ready for collection', async () => {
    await helper.whenEmployeeMarksOrderPreparing(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenUiShowsStatus(
      FulfillmentBaseHelper.ORDER_CNC_1042,
      'ready for collection',
    );
  });

  it('Prepare Click-and-Collect Orders for Pickup — AC 3: unpaid excluded', async () => {
    await helper.whenEmployeeOpensFulfillmentQueue();
    helper.thenUiDoesNotListOrder(FulfillmentBaseHelper.ORDER_CNC_1044);
  });

  it('Prepare Click-and-Collect Orders for Pickup — AC 4: store scoped queue', async () => {
    await helper.whenEmployeeOpensFulfillmentQueue();
    helper.thenUiListsOrderInQueue(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenUiDoesNotListOrder(FulfillmentBaseHelper.ORDER_CNC_1043);
  });

  it('Prepare Click-and-Collect Orders for Pickup — AC 5: customer blocked', async () => {
    await helper.givenCustomerSession();
    await helper.whenCustomerAttemptsFulfillmentQueue();
    helper.thenUiBlocksCustomerAccess();
  });
});

describe('Fulfill Click-and-Collect Order — client', () => {
  const helper = new FulfillmentClientHelper();

  beforeEach(async () => {
    await helper.givenStoreEmployeeAtDowntown();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Fulfill Click-and-Collect Order — AC 1: detail shows lines and fulfill offer', async () => {
    await helper.whenEmployeeMarksOrderPreparing(FulfillmentBaseHelper.ORDER_CNC_1042);
    await helper.whenEmployeeOpensOrderDetail(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenUiShowsOrderLines();
  });

  it('Fulfill Click-and-Collect Order — AC 4: unprepared blocked', async () => {
    await helper.whenEmployeeOpensOrderDetail(FulfillmentBaseHelper.ORDER_CNC_1042);
    await helper.whenEmployeeAttemptsFulfill(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenUiShowsPreparationWarning();
  });

  it('Fulfill Click-and-Collect Order — AC 2: fulfill complete removes queue', async () => {
    await helper.whenEmployeeMarksOrderPreparing(FulfillmentBaseHelper.ORDER_CNC_1042);
    await helper.whenEmployeeOpensOrderDetail(FulfillmentBaseHelper.ORDER_CNC_1042);
    await helper.whenEmployeeAttemptsFulfill(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenUiShowsOrderComplete();
  });
});
