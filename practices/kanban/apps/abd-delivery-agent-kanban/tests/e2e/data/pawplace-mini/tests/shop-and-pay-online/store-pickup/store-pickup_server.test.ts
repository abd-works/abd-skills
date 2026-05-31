/**
 * Store pickup — server acceptance tests (Increment 2 Sprint 3).
 *
 * Story path: Shop & Pay Online → Store pickup → [Story]
 * File: tests/shop-and-pay-online/store-pickup/store-pickup_server.test.ts
 *
 * Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import { FulfillmentServerHelper } from './helpers/fulfillment.server';
import { FulfillmentBaseHelper } from './helpers/fulfillment.base';

describe('Prepare Click-and-Collect Orders for Pickup', () => {
  const helper = new FulfillmentServerHelper();

  beforeEach(async () => {
    await helper.givenStoreEmployeeJordanKimBoundToDowntownPawPlace();
    await helper.givenSprint3BackgroundOrdersSeeded();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: fulfillment queue lists paid click-and-collect orders awaiting preparation', async () => {
    await helper.whenStoreEmployeeOpensFulfillmentQueueViaApi();
    helper.thenFulfillmentQueueListsOrder(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenFulfillmentQueueRowShowsContactStatusAndStore(
      FulfillmentBaseHelper.ORDER_CNC_1042,
      FulfillmentBaseHelper.CONTACT_ALEX,
      'awaiting preparation',
      FulfillmentBaseHelper.STORE_DOWNTOWN,
    );
    helper.thenStoreEmployeeCanOpenOrderFromQueue(FulfillmentBaseHelper.ORDER_CNC_1042);
  });

  it('Scenario 2: mark preparing updates click-and-collect order to ready for collection', async () => {
    await helper.whenStoreEmployeeMarksOrderPreparingViaApi(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenOrderFulfillmentStatusIs(
      FulfillmentBaseHelper.ORDER_CNC_1042,
      'ready for collection',
    );
    helper.thenOrderRemainsScopedToStore(
      FulfillmentBaseHelper.ORDER_CNC_1042,
      FulfillmentBaseHelper.STORE_DOWNTOWN,
    );
  });

  it('Scenario 3: unpaid orders without order confirmation are excluded from preparation queue', async () => {
    await helper.whenStoreEmployeeOpensFulfillmentQueueViaApi();
    helper.thenFulfillmentQueueDoesNotListOrder(FulfillmentBaseHelper.ORDER_CNC_1044);
  });

  it('Scenario 4: fulfillment queue shows only orders for employee click-and-collect store', async () => {
    await helper.whenStoreEmployeeOpensFulfillmentQueueViaApi();
    helper.thenFulfillmentQueueListsOrder(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenFulfillmentQueueDoesNotListOrder(FulfillmentBaseHelper.ORDER_CNC_1043);
  });

  it('Scenario 5: customer cannot access fulfillment queue or preparation actions', async () => {
    await helper.givenCustomerAlexRiveraSession();
    await helper.whenCustomerAttemptsFulfillmentQueueViaApi();
    helper.thenFulfillmentQueueAndPreparationActionsUnavailableToCustomer();
  });
});

describe('Fulfill Click-and-Collect Order', () => {
  const helper = new FulfillmentServerHelper();

  beforeEach(async () => {
    await helper.givenStoreEmployeeJordanKimBoundToDowntownPawPlace();
    await helper.givenSprint3BackgroundOrdersSeeded();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: prepared order detail shows lines store and fulfillment status with handoff action', async () => {
    await helper.givenClickAndCollectOrderReadyForCollection(
      FulfillmentBaseHelper.ORDER_1042_PAID,
    );
    await helper.whenStoreEmployeeOpensOrderDetailViaApi(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenOrderDetailShowsCartLinesAndStore(
      FulfillmentBaseHelper.ORDER_CNC_1042,
      FulfillmentBaseHelper.STORE_DOWNTOWN,
      'ready for collection',
    );
    helper.thenFulfillClickAndCollectOrderOfferedWhenPreparationComplete();
  });

  it('Scenario 2: confirming fulfill marks order fulfillment complete and removes order from queue', async () => {
    await helper.givenClickAndCollectOrderReadyForCollection(
      FulfillmentBaseHelper.ORDER_1042_PAID,
    );
    await helper.whenStoreEmployeeAttemptsFulfillOrderViaApi(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenOrderFulfillmentStatusIs(
      FulfillmentBaseHelper.ORDER_CNC_1042,
      'complete',
    );
    helper.thenFulfillmentQueueRemovesOrder(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenCustomerReceivesOrderLines();
  });

  it('Scenario 3: store employee matches order proof and completes handoff at click-and-collect store', async () => {
    await helper.givenClickAndCollectOrderReadyForCollection(
      FulfillmentBaseHelper.ORDER_1042_PAID,
    );
    await helper.whenStoreEmployeeAttemptsFulfillOrderViaApi(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenOrderFulfillmentStatusIs(
      FulfillmentBaseHelper.ORDER_CNC_1042,
      'complete',
    );
    helper.thenCustomerReceivesOrderLines();
  });

  it('Scenario 4: handoff blocked when click-and-collect order is not yet prepared', async () => {
    await helper.givenClickAndCollectOrderAwaitingPreparation(
      FulfillmentBaseHelper.ORDER_1042_PAID,
    );
    await helper.whenStoreEmployeeOpensOrderDetailViaApi(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    await helper.whenStoreEmployeeAttemptsFulfillOrderViaApi(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenFulfillBlocksHandoffWithPreparationWarning(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenOrderFulfillmentNotMarkedComplete(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenFulfillmentQueueStillListsOrder(FulfillmentBaseHelper.ORDER_CNC_1042);
  });

  it('Scenario 5: completed fulfill closes order against repeat pickup actions', async () => {
    await helper.givenClickAndCollectOrderFulfillmentComplete(
      FulfillmentBaseHelper.ORDER_1042_PAID,
    );
    await helper.whenStoreEmployeeOrCustomerAttemptsRepeatFulfillViaApi(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    helper.thenOrderShowsCollectedOrClosed(FulfillmentBaseHelper.ORDER_CNC_1042);
    helper.thenFulfillDoesNotCompleteOrderFulfillmentAgain(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
  });
});
