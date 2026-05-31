import type {
  FulfillmentQueueRowDto,
  OrderFulfillmentStatus,
} from './fulfillment.types';
import { ClickAndCollectOrder } from './click-and-collect-order';
import { ClickAndCollectStore } from './click-and-collect-store';
import { OrderConfirmation } from './order-confirmation';
import type { FulfillClickAndCollectOrder } from './fulfill-click-and-collect-order';

/** << Entity >> — paid orders awaiting preparation at one click-and-collect store. */
export class FulfillmentQueue {
  constructor(
    readonly clickAndCollectStore: ClickAndCollectStore,
    private awaitingPreparationOrders: ClickAndCollectOrder[],
  ) {}

  listPaidOrdersAwaitingPreparation(): FulfillmentQueueRowDto[] {
    return this.awaitingPreparationOrders
      .filter((order) => order.excludeUnpaidOrdersFromFulfillmentQueue())
      .filter((order) => !order.isFulfillmentComplete())
      .map((order) => ({
        orderId: order.orderId,
        customerContact: order.customerContact,
        orderFulfillment: order.orderFulfillment.currentStatus as OrderFulfillmentStatus,
        clickAndCollectStore: order.clickAndCollectStore.storeIdentity,
        pickupTime: 'ASAP',
      }));
  }

  excludeUnpaidOrUnconfirmedSessions(
    orderConfirmation: OrderConfirmation,
    _clickAndCollectOrder: ClickAndCollectOrder,
  ): ClickAndCollectOrder[] {
    return this.awaitingPreparationOrders.filter((order) =>
      order.hasSuccessfulPaymentAndConfirmation(orderConfirmation),
    );
  }

  removeOrderFromActiveQueueOnFulfill(
    _fulfillClickAndCollectOrder: FulfillClickAndCollectOrder,
    clickAndCollectOrder: ClickAndCollectOrder,
  ): void {
    this.awaitingPreparationOrders = this.awaitingPreparationOrders.filter(
      (order) => order.orderId !== clickAndCollectOrder.orderId,
    );
  }

  openOrderDetailForHandoffPrep(
    _fulfillClickAndCollectOrder: FulfillClickAndCollectOrder,
    _storeEmployee: StoreEmployee,
    clickAndCollectOrder: ClickAndCollectOrder,
  ): ClickAndCollectOrder {
    return clickAndCollectOrder;
  }

  filterToStoreScope(clickAndCollectStore: ClickAndCollectStore): FulfillmentQueue {
    const scopedOrders = this.awaitingPreparationOrders.filter((order) =>
      order.clickAndCollectStore.equals(clickAndCollectStore),
    );
    return new FulfillmentQueue(clickAndCollectStore, scopedOrders);
  }

  containsOrder(clickAndCollectOrder: ClickAndCollectOrder): boolean {
    return this.awaitingPreparationOrders.some(
      (order) => order.orderId === clickAndCollectOrder.orderId,
    );
  }

  addConfirmedOrder(
    clickAndCollectOrder: ClickAndCollectOrder,
    orderConfirmation: OrderConfirmation,
  ): void {
    if (
      clickAndCollectOrder.hasSuccessfulPaymentAndConfirmation(orderConfirmation)
    ) {
      this.awaitingPreparationOrders.push(clickAndCollectOrder);
    }
  }
}

/** << Entity >> — store employee bound to one click-and-collect store. */
export class StoreEmployee {
  constructor(
    readonly displayName: string,
    private boundStore: ClickAndCollectStore | null = null,
  ) {}

  bindToClickAndCollectStore(clickAndCollectStore: ClickAndCollectStore): void {
    this.boundStore = clickAndCollectStore;
  }

  get clickAndCollectStore(): ClickAndCollectStore | null {
    return this.boundStore;
  }
}
