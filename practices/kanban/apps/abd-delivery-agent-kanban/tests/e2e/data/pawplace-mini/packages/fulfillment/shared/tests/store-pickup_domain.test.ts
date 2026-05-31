/**
 * Store pickup — domain acceptance tests (packages/fulfillment/shared).
 * Increment 2 Sprint 3 — typed domain surface from object-model.md.
 */
import { describe, it } from 'vitest';
import assert from 'node:assert/strict';
import {
  ClickAndCollectOrder,
  ClickAndCollectStore,
  CustomerFulfillment,
  FulfillClickAndCollectOrder,
  FulfillmentQueue,
  OrderConfirmation,
  OrderFulfillment,
  PreparationIncompleteException,
  PrepareClickAndCollectOrdersForPickup,
  StoreEmployee,
} from '../src/index';

describe('Prepare Click-and-Collect Orders for Pickup (domain)', () => {
  it('mark preparing transitions order fulfillment to ready for collection', () => {
    const store = new ClickAndCollectStore('Downtown PawPlace');
    const orderFulfillment = new OrderFulfillment('awaiting preparation');
    const order = new ClickAndCollectOrder(
      'CNC-1042',
      'alex.rivera@example.com',
      store,
      orderFulfillment,
      [{ catalogItemIdentity: 'Premium Salmon Kibble', cartQuantity: 1 }],
      new OrderConfirmation(true),
      true,
    );
    const prepare = new PrepareClickAndCollectOrdersForPickup();
    order.transitionToReadyForCollection(prepare);
    assert.equal(orderFulfillment.currentStatus, 'ready for collection');
  });

  it('fulfillment queue excludes unpaid orders without order confirmation', () => {
    const store = new ClickAndCollectStore('Downtown PawPlace');
    const paidOrder = new ClickAndCollectOrder(
      'CNC-1042',
      'alex.rivera@example.com',
      store,
      new OrderFulfillment('awaiting preparation'),
      [],
      new OrderConfirmation(true),
      true,
    );
    const unpaidOrder = new ClickAndCollectOrder(
      'CNC-1044',
      'lee.chen@example.com',
      store,
      new OrderFulfillment('awaiting preparation'),
      [],
      new OrderConfirmation(false),
      false,
    );
    const queue = new FulfillmentQueue(store, [paidOrder, unpaidOrder]);
    const eligible = queue.excludeUnpaidOrUnconfirmedSessions(
      new OrderConfirmation(true),
      unpaidOrder,
    );
    assert.equal(eligible.length, 1);
    assert.equal(eligible[0]!.orderId, 'CNC-1042');
  });

  it('fulfillment queue filters to employee click-and-collect store only', () => {
    const downtown = new ClickAndCollectStore('Downtown PawPlace');
    const westside = new ClickAndCollectStore('Westside PawPlace');
    const downtownOrder = new ClickAndCollectOrder(
      'CNC-1042',
      'alex.rivera@example.com',
      downtown,
      new OrderFulfillment('awaiting preparation'),
      [],
      new OrderConfirmation(true),
      true,
    );
    const westsideOrder = new ClickAndCollectOrder(
      'CNC-1043',
      'sam.patel@example.com',
      westside,
      new OrderFulfillment('awaiting preparation'),
      [],
      new OrderConfirmation(true),
      true,
    );
    const queue = new FulfillmentQueue(downtown, [downtownOrder, westsideOrder]);
    const scoped = downtown.scopeFulfillmentQueueToOneLocation(queue);
    assert.equal(scoped.listPaidOrdersAwaitingPreparation().length, 1);
    assert.equal(scoped.listPaidOrdersAwaitingPreparation()[0]!.orderId, 'CNC-1042');
  });
});

describe('Fulfill Click-and-Collect Order (domain)', () => {
  it('blocks handoff when order fulfillment is awaiting preparation', () => {
    const store = new ClickAndCollectStore('Downtown PawPlace');
    const orderFulfillment = new OrderFulfillment('awaiting preparation');
    const order = new ClickAndCollectOrder(
      'CNC-1042',
      'alex.rivera@example.com',
      store,
      orderFulfillment,
      [],
      new OrderConfirmation(true),
      true,
    );
    const fulfill = new FulfillClickAndCollectOrder();
    assert.throws(
      () => fulfill.confirmHandoffAtPickup(
        order,
        orderFulfillment,
        new FulfillmentQueue(store, [order]),
        new StoreEmployee('Jordan Kim'),
        new CustomerFulfillment(),
      ),
      PreparationIncompleteException,
    );
  });

  it('confirm handoff marks order fulfillment complete and removes from queue', () => {
    const store = new ClickAndCollectStore('Downtown PawPlace');
    const orderFulfillment = new OrderFulfillment('ready for collection');
    const order = new ClickAndCollectOrder(
      'CNC-1042',
      'alex.rivera@example.com',
      store,
      orderFulfillment,
      [{ catalogItemIdentity: 'Premium Salmon Kibble', cartQuantity: 1 }],
      new OrderConfirmation(true),
      true,
    );
    const queue = new FulfillmentQueue(store, [order]);
    const fulfill = new FulfillClickAndCollectOrder();
    const customer = new CustomerFulfillment();
    fulfill.confirmHandoffAtPickup(
      order,
      orderFulfillment,
      queue,
      new StoreEmployee('Jordan Kim'),
      customer,
    );
    assert.equal(orderFulfillment.currentStatus, 'complete');
    assert.equal(queue.listPaidOrdersAwaitingPreparation().length, 0);
    assert.equal(customer.collectedLines.length, 1);
  });

  it('closed order rejects repeat fulfill click-and-collect order', () => {
    const orderFulfillment = new OrderFulfillment('complete');
    assert.equal(orderFulfillment.isClosedAgainstRepeatPickup(), true);
  });
});
