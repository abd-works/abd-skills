import {
  ClickAndCollectOrder,
  ClickAndCollectStore,
  CustomerFulfillment,
  FulfillmentQueue,
  OrderConfirmation,
  OrderFulfillment,
  StoreEmployee,
  type ClickAndCollectCartLine,
} from '../shared/src/index';

export interface FulfillmentOrderRecord {
  order: ClickAndCollectOrder;
  customer: CustomerFulfillment;
}

export interface FulfillmentSessionRecord {
  storeEmployee: StoreEmployee | null;
  isCustomer: boolean;
}

export interface SeedOrderInput {
  orderId: string;
  customerContact: string;
  clickAndCollectStore: string;
  orderFulfillment: 'awaiting preparation' | 'ready for collection' | 'complete';
  paid: boolean;
  cartLines: ClickAndCollectCartLine[];
}

/** In-memory fulfillment persistence for store pickup flows. */
export class FulfillmentRepository {
  private readonly orders = new Map<string, FulfillmentOrderRecord>();
  private readonly sessions = new Map<string, FulfillmentSessionRecord>();
  private queueStore = new ClickAndCollectStore('Downtown PawPlace');

  saveOrder(record: FulfillmentOrderRecord): void {
    this.orders.set(record.order.orderId, record);
  }

  findOrder(orderId: string): FulfillmentOrderRecord | undefined {
    return this.orders.get(orderId);
  }

  allOrders(): FulfillmentOrderRecord[] {
    return [...this.orders.values()];
  }

  saveSession(sessionId: string, record: FulfillmentSessionRecord): void {
    this.sessions.set(sessionId, record);
  }

  findSession(sessionId: string): FulfillmentSessionRecord | undefined {
    return this.sessions.get(sessionId);
  }

  buildQueueForStore(storeIdentity: string): FulfillmentQueue {
    const store = new ClickAndCollectStore(storeIdentity);
    const orders = this.allOrders()
      .map((record) => record.order)
      .filter((order) => order.clickAndCollectStore.storeIdentity === storeIdentity);
    return new FulfillmentQueue(store, orders);
  }

  replaceQueueOrders(storeIdentity: string, orders: ClickAndCollectOrder[]): void {
    const store = new ClickAndCollectStore(storeIdentity);
    this.queueStore = store;
    for (const order of orders) {
      const existing = this.orders.get(order.orderId);
      if (existing) {
        existing.order = order;
      }
    }
  }

  removeOrderFromQueue(orderId: string): void {
    this.orders.delete(orderId);
  }

  seedOrder(input: SeedOrderInput): void {
    const store = new ClickAndCollectStore(input.clickAndCollectStore);
    const orderFulfillment = new OrderFulfillment(input.orderFulfillment);
    const orderConfirmation = new OrderConfirmation(input.paid);
    const order = new ClickAndCollectOrder(
      input.orderId,
      input.customerContact,
      store,
      orderFulfillment,
      input.cartLines,
      orderConfirmation,
      input.paid,
    );
    this.saveOrder({ order, customer: new CustomerFulfillment() });
  }

  bindEmployeeSession(
    sessionId: string,
    displayName: string,
    storeIdentity: string,
  ): void {
    const storeEmployee = new StoreEmployee(displayName);
    storeEmployee.bindToClickAndCollectStore(new ClickAndCollectStore(storeIdentity));
    this.saveSession(sessionId, { storeEmployee, isCustomer: false });
  }

  bindCustomerSession(sessionId: string): void {
    this.saveSession(sessionId, { storeEmployee: null, isCustomer: true });
  }

  reset(): void {
    this.orders.clear();
    this.sessions.clear();
    this.queueStore = new ClickAndCollectStore('Downtown PawPlace');
  }
}
