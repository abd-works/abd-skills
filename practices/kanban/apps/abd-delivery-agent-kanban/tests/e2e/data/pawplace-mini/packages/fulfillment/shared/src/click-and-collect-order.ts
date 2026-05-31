import type { FulfillClickAndCollectOrder } from './fulfill-click-and-collect-order';
import { ClickAndCollectStore } from './click-and-collect-store';
import { OrderConfirmation } from './order-confirmation';
import { OrderFulfillment } from './order-fulfillment';
import type { PrepareClickAndCollectOrdersForPickup } from './prepare-click-and-collect-orders-for-pickup';

export interface ClickAndCollectCartLine {
  catalogItemIdentity: string;
  cartQuantity: number;
}

/** << Entity >> — paid click-and-collect order awaiting store pickup. */
export class ClickAndCollectOrder {
  constructor(
    readonly orderId: string,
    readonly customerContact: string,
    readonly clickAndCollectStore: ClickAndCollectStore,
    readonly orderFulfillment: OrderFulfillment,
    readonly cartLines: ClickAndCollectCartLine[],
    readonly orderConfirmation: OrderConfirmation,
    readonly paymentConfirmed: boolean,
  ) {}

  awaitPreparationAfterConfirmation(orderFulfillment: OrderFulfillment): void {
    orderFulfillment.markAwaitingPreparation();
  }

  transitionToReadyForCollection(
    prepareClickAndCollectOrdersForPickup: PrepareClickAndCollectOrdersForPickup,
  ): OrderFulfillment {
    return this.orderFulfillment.markReadyForCollection(
      prepareClickAndCollectOrdersForPickup,
    );
  }

  blockHandoffUntilPreparationComplete(
    _fulfillClickAndCollectOrder: FulfillClickAndCollectOrder,
  ): boolean {
    return this.orderFulfillment.isAwaitingPreparation();
  }

  markCollectedOrClosedAfterHandoff(
    fulfillClickAndCollectOrder: FulfillClickAndCollectOrder,
  ): OrderFulfillment {
    return this.orderFulfillment.markCollectedOrClosed(fulfillClickAndCollectOrder);
  }

  excludeUnpaidOrdersFromFulfillmentQueue(): boolean {
    return this.paymentConfirmed && this.orderConfirmation.isComplete();
  }

  hasSuccessfulPaymentAndConfirmation(orderConfirmation: OrderConfirmation): boolean {
    return this.paymentConfirmed && orderConfirmation.isComplete();
  }

  isReadyForCollection(): boolean {
    return this.orderFulfillment.isReadyForCollection();
  }

  isAwaitingPreparation(): boolean {
    return this.orderFulfillment.isAwaitingPreparation();
  }

  isFulfillmentComplete(): boolean {
    return this.orderFulfillment.isComplete();
  }

  matchesOrderProof(presentedOrderId: string): boolean {
    return this.orderId === presentedOrderId;
  }

  showLinesForHandoffDetail(): ClickAndCollectCartLine[] {
    return [...this.cartLines];
  }
}
