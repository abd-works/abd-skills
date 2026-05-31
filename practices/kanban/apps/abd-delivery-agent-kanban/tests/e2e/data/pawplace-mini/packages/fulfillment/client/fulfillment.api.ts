import type {
  FulfillmentOrderDetailDto,
  FulfillmentQueueRowDto,
  OrderFulfillmentStatus,
} from '../shared/src/fulfillment.types';

export interface FulfillmentApi {
  listQueue(employeeStoreIdentity: string): FulfillmentQueueRowDto[];
  getOrder(orderId: string): FulfillmentOrderDetailDto | null;
  markPreparing(orderId: string): FulfillmentOrderDetailDto | null;
  fulfillOrder(orderId: string): FulfillmentOrderDetailDto | null;
  seedOrders(orders: FulfillmentOrderDetailDto[]): void;
  reset(): void;
}

interface StoredOrder extends FulfillmentOrderDetailDto {
  paid: boolean;
}

const EMPLOYEE_ACCENT = '#2E6B4A';

export { EMPLOYEE_ACCENT };

export class InMemoryFulfillmentApi implements FulfillmentApi {
  private orders: StoredOrder[] = [];

  reset(): void {
    this.orders = [];
  }

  seedOrders(orders: FulfillmentOrderDetailDto[]): void {
    this.orders = orders.map((o) => ({ ...o, paid: true }));
  }

  seedUnpaidOrder(order: FulfillmentOrderDetailDto): void {
    this.orders.push({ ...order, paid: false });
  }

  listQueue(employeeStoreIdentity: string): FulfillmentQueueRowDto[] {
    return this.orders
      .filter(
        (o) =>
          o.paid &&
          o.clickAndCollectStore === employeeStoreIdentity &&
          o.orderFulfillment !== 'complete' &&
          o.orderFulfillment !== 'collected' &&
          o.orderFulfillment !== 'closed',
      )
      .map((o) => ({
        orderId: o.orderId,
        customerContact: o.customerContact,
        orderFulfillment: o.orderFulfillment,
        clickAndCollectStore: o.clickAndCollectStore,
        pickupTime: 'ASAP',
      }));
  }

  getOrder(orderId: string): FulfillmentOrderDetailDto | null {
    const order = this.orders.find((o) => o.orderId === orderId && o.paid);
    return order ? { ...order } : null;
  }

  markPreparing(orderId: string): FulfillmentOrderDetailDto | null {
    const order = this.orders.find((o) => o.orderId === orderId && o.paid);
    if (!order) return null;
    order.orderFulfillment = 'ready for collection';
    return { ...order };
  }

  fulfillOrder(orderId: string): FulfillmentOrderDetailDto | null {
    const order = this.orders.find((o) => o.orderId === orderId && o.paid);
    if (!order) return null;
    if (order.orderFulfillment === 'awaiting preparation') {
      return null;
    }
    if (
      order.orderFulfillment === 'complete' ||
      order.orderFulfillment === 'collected' ||
      order.orderFulfillment === 'closed'
    ) {
      return { ...order };
    }
    order.orderFulfillment = 'complete';
    return { ...order };
  }
}
