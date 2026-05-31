/**
 * Store pickup — server-tier helper (Supertest + FulfillmentService / FulfillmentApi).
 */
import assert from 'node:assert/strict';
import type { Express } from 'express';
import request from 'supertest';
import { createAppServer } from '@pawplace-mini/app-server';
import type { FulfillmentService } from '@pawplace-mini/fulfillment-server';
import type {
  FulfillmentOrderDetailDto,
  FulfillmentQueueRowDto,
} from '@pawplace-mini/fulfillment-shared';
import {
  FulfillmentBaseHelper,
  type ClickAndCollectOrderTestData,
  type ClickAndCollectStoreTestData,
} from './fulfillment.base';

export class FulfillmentServerHelper extends FulfillmentBaseHelper {
  private readonly app: Express;
  private readonly fulfillmentService: FulfillmentService;
  private readonly employeeSessionId = 'fulfillment-employee-session';
  private readonly customerSessionId = 'fulfillment-customer-session';
  private lastQueue: FulfillmentQueueRowDto[] = [];
  private lastOrder: FulfillmentOrderDetailDto | null = null;
  private lastFulfillResponse: {
    blocked?: boolean;
    warning?: string;
    customerReceivedLines?: boolean;
  } | null = null;
  private lastQueueStatus = 200;
  private lastCustomerQueueStatus = 200;

  constructor() {
    super();
    const server = createAppServer();
    this.app = server.app;
    this.fulfillmentService = server.fulfillmentService;
  }

  async cleanup(): Promise<void> {
    this.fulfillmentService.resetFixture();
    this.lastQueue = [];
    this.lastOrder = null;
    this.lastFulfillResponse = null;
    this.lastQueueStatus = 200;
    this.lastCustomerQueueStatus = 200;
  }

  protected async seedEmployeeSessionAtStore(
    store: ClickAndCollectStoreTestData,
  ): Promise<void> {
    this.fulfillmentService.bindEmployeeSession(
      this.employeeSessionId,
      this.storeEmployee.displayName,
      store.storeIdentity,
    );
  }

  protected async seedPaidOrder(order: ClickAndCollectOrderTestData): Promise<void> {
    this.fulfillmentService.seedPaidOrder({
      orderId: order.orderId,
      customerContact: order.customerContact,
      clickAndCollectStore: order.clickAndCollectStore,
      orderFulfillment: order.orderFulfillment,
      paid: true,
      cartLines: order.cartLines,
    });
  }

  protected async seedUnpaidOrder(order: ClickAndCollectOrderTestData): Promise<void> {
    this.fulfillmentService.seedUnpaidOrder({
      orderId: order.orderId,
      customerContact: order.customerContact,
      clickAndCollectStore: order.clickAndCollectStore,
      orderFulfillment: order.orderFulfillment,
      paid: false,
      cartLines: order.cartLines,
    });
  }

  protected async seedCustomerSession(_displayName: string): Promise<void> {
    this.fulfillmentService.bindCustomerSession(this.customerSessionId);
  }

  async whenStoreEmployeeOpensFulfillmentQueueViaApi(): Promise<void> {
    const response = await request(this.app)
      .get('/api/v1/fulfillment/queue')
      .query({ store: this.employeeStore.storeIdentity })
      .set('x-session-id', this.employeeSessionId)
      .set('x-staff-token', 'store-employee');
    this.lastQueueStatus = response.status;
    this.lastQueue = response.body.queue ?? [];
  }

  async whenStoreEmployeeMarksOrderPreparingViaApi(orderId: string): Promise<void> {
    const response = await request(this.app)
      .post(`/api/v1/fulfillment/orders/${orderId}/prepare`)
      .set('x-session-id', this.employeeSessionId)
      .set('x-staff-token', 'store-employee')
      .send({ storeIdentity: this.employeeStore.storeIdentity });
    assert.equal(response.status, 200);
    this.lastOrder = response.body.order;
  }

  async whenStoreEmployeeOpensOrderDetailViaApi(orderId: string): Promise<void> {
    const response = await request(this.app)
      .get(`/api/v1/fulfillment/orders/${orderId}`)
      .set('x-session-id', this.employeeSessionId)
      .set('x-staff-token', 'store-employee');
    assert.equal(response.status, 200);
    this.lastOrder = response.body.order;
  }

  async whenStoreEmployeeAttemptsFulfillOrderViaApi(orderId: string): Promise<void> {
    const response = await request(this.app)
      .post(`/api/v1/fulfillment/orders/${orderId}/fulfill`)
      .set('x-session-id', this.employeeSessionId)
      .set('x-staff-token', 'store-employee');
    assert.equal(response.status, 200);
    this.lastOrder = response.body.order;
    this.lastFulfillResponse = response.body;
  }

  async whenCustomerAttemptsFulfillmentQueueViaApi(): Promise<void> {
    const response = await request(this.app)
      .get('/api/v1/fulfillment/queue')
      .query({ store: this.employeeStore.storeIdentity })
      .set('x-session-id', this.customerSessionId);
    this.lastCustomerQueueStatus = response.status;
  }

  async whenStoreEmployeeOrCustomerAttemptsRepeatFulfillViaApi(
    orderId: string,
  ): Promise<void> {
    await this.whenStoreEmployeeAttemptsFulfillOrderViaApi(orderId);
  }

  thenFulfillmentQueueListsOrder(orderId: string): void {
    assert.ok(
      this.lastQueue.some((row) => row.orderId === orderId),
      `fulfillment queue should list ${orderId}`,
    );
  }

  thenFulfillmentQueueRowShowsContactStatusAndStore(
    orderId: string,
    customerContact: string,
    orderFulfillment: string,
    clickAndCollectStore: string,
  ): void {
    const row = this.lastQueue.find((entry) => entry.orderId === orderId);
    assert.ok(row, `expected queue row for ${orderId}`);
    assert.equal(row!.customerContact, customerContact);
    assert.equal(row!.orderFulfillment, orderFulfillment);
    assert.equal(row!.clickAndCollectStore, clickAndCollectStore);
  }

  thenStoreEmployeeCanOpenOrderFromQueue(orderId: string): void {
    assert.ok(this.lastQueue.some((row) => row.orderId === orderId));
  }

  thenOrderFulfillmentStatusIs(orderId: string, status: string): void {
    assert.ok(this.lastOrder, 'expected order detail from last API call');
    assert.equal(this.lastOrder!.orderId, orderId);
    assert.equal(this.lastOrder!.orderFulfillment, status);
  }

  thenOrderRemainsScopedToStore(orderId: string, storeIdentity: string): void {
    assert.ok(this.lastOrder);
    assert.equal(this.lastOrder!.orderId, orderId);
    assert.equal(this.lastOrder!.clickAndCollectStore, storeIdentity);
  }

  thenFulfillmentQueueDoesNotListOrder(orderId: string): void {
    assert.equal(
      this.lastQueue.some((row) => row.orderId === orderId),
      false,
      `fulfillment queue should not list ${orderId}`,
    );
  }

  thenFulfillmentQueueAndPreparationActionsUnavailableToCustomer(): void {
    assert.equal(this.lastCustomerQueueStatus, 403);
  }

  thenOrderDetailShowsCartLinesAndStore(
    orderId: string,
    storeIdentity: string,
    status: string,
  ): void {
    assert.ok(this.lastOrder);
    assert.equal(this.lastOrder!.orderId, orderId);
    assert.equal(this.lastOrder!.clickAndCollectStore, storeIdentity);
    assert.equal(this.lastOrder!.orderFulfillment, status);
    assert.ok(this.lastOrder!.cartLines.length > 0);
  }

  thenFulfillClickAndCollectOrderOfferedWhenPreparationComplete(): void {
    assert.equal(this.lastOrder?.orderFulfillment, 'ready for collection');
  }

  thenFulfillBlocksHandoffWithPreparationWarning(orderId: string): void {
    assert.equal(this.lastFulfillResponse?.blocked, true);
    assert.match(String(this.lastFulfillResponse?.warning), /preparation is incomplete/i);
    assert.equal(this.lastOrder?.orderId, orderId);
  }

  thenOrderFulfillmentNotMarkedComplete(orderId: string): void {
    assert.notEqual(this.lastOrder?.orderFulfillment, 'complete');
    assert.equal(this.lastOrder?.orderId, orderId);
  }

  thenFulfillmentQueueStillListsOrder(orderId: string): void {
    const queue = this.fulfillmentService.listQueue(
      'store-employee',
      this.employeeSessionId,
      this.employeeStore.storeIdentity,
    );
    assert.ok(queue.some((row) => row.orderId === orderId));
  }

  thenFulfillmentQueueRemovesOrder(orderId: string): void {
    const queue = this.fulfillmentService.listQueue(
      'store-employee',
      this.employeeSessionId,
      this.employeeStore.storeIdentity,
    );
    assert.equal(
      queue.some((row) => row.orderId === orderId),
      false,
    );
  }

  thenCustomerReceivesOrderLines(): void {
    const lines = this.fulfillmentService.getDeliveredLines(
      FulfillmentBaseHelper.ORDER_CNC_1042,
    );
    assert.ok(lines.length > 0);
  }

  thenOrderShowsCollectedOrClosed(orderId: string): void {
    assert.ok(this.lastOrder);
    assert.equal(this.lastOrder!.orderId, orderId);
    assert.ok(
      ['complete', 'collected', 'closed'].includes(this.lastOrder!.orderFulfillment),
    );
  }

  thenFulfillDoesNotCompleteOrderFulfillmentAgain(orderId: string): void {
    assert.equal(this.lastFulfillResponse?.blocked, true);
    assert.equal(this.lastOrder?.orderId, orderId);
    assert.ok(
      ['complete', 'collected', 'closed'].includes(
        this.lastOrder?.orderFulfillment ?? '',
      ),
    );
  }
}
