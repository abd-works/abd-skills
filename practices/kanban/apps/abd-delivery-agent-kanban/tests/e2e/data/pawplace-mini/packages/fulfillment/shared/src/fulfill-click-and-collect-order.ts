import { ClickAndCollectOrder } from './click-and-collect-order';
import { ClickAndCollectStore } from './click-and-collect-store';
import { CustomerFulfillment } from './customer-fulfillment';
import { PreparationIncompleteException } from './fulfillment-exceptions';
import { FulfillmentQueue, StoreEmployee } from './fulfillment-queue';
import { OrderFulfillment } from './order-fulfillment';
import { PrepareClickAndCollectOrdersForPickup } from './prepare-click-and-collect-orders-for-pickup';

/** << Service >> — store employee handoff at click-and-collect pickup. */
export class FulfillClickAndCollectOrder {
  openPreparedOrderFromQueue(
    fulfillmentQueue: FulfillmentQueue,
    clickAndCollectOrder: ClickAndCollectOrder,
    storeEmployee: StoreEmployee,
  ): ClickAndCollectOrder {
    return fulfillmentQueue.openOrderDetailForHandoffPrep(
      this,
      storeEmployee,
      clickAndCollectOrder,
    );
  }

  showLinesStoreAndFulfillmentStatus(
    clickAndCollectOrder: ClickAndCollectOrder,
    _clickAndCollectStore: ClickAndCollectStore,
    _orderFulfillment: OrderFulfillment,
  ): ClickAndCollectOrder {
    return clickAndCollectOrder;
  }

  enableHandoffWhenPreparationComplete(orderFulfillment: OrderFulfillment): boolean {
    return orderFulfillment.isReadyForCollection();
  }

  blockHandoffWhenPreparationIncomplete(
    orderFulfillment: OrderFulfillment,
    _prepareClickAndCollectOrdersForPickup: PrepareClickAndCollectOrdersForPickup,
  ): boolean {
    return orderFulfillment.blockPrematureCompletionBeforePrepare();
  }

  markOrderFulfillmentCompleteOnConfirm(
    orderFulfillment: OrderFulfillment,
    clickAndCollectOrder: ClickAndCollectOrder,
  ): OrderFulfillment {
    if (clickAndCollectOrder.blockHandoffUntilPreparationComplete(this)) {
      throw new PreparationIncompleteException(clickAndCollectOrder);
    }
    return clickAndCollectOrder.markCollectedOrClosedAfterHandoff(this);
  }

  removeOrderFromActivePreparationQueue(
    fulfillmentQueue: FulfillmentQueue,
    clickAndCollectOrder: ClickAndCollectOrder,
  ): void {
    fulfillmentQueue.removeOrderFromActiveQueueOnFulfill(this, clickAndCollectOrder);
  }

  closeOrderAgainstRepeatPickupActions(clickAndCollectOrder: ClickAndCollectOrder): boolean {
    return clickAndCollectOrder.isFulfillmentComplete();
  }

  confirmHandoffAtPickup(
    clickAndCollectOrder: ClickAndCollectOrder,
    orderFulfillment: OrderFulfillment,
    fulfillmentQueue: FulfillmentQueue,
    storeEmployee: StoreEmployee,
    customer: CustomerFulfillment,
  ): OrderFulfillment {
    if (
      this.blockHandoffWhenPreparationIncomplete(
        orderFulfillment,
        new PrepareClickAndCollectOrdersForPickup(),
      )
    ) {
      throw new PreparationIncompleteException(clickAndCollectOrder);
    }
    const completedFulfillment = this.markOrderFulfillmentCompleteOnConfirm(
      orderFulfillment,
      clickAndCollectOrder,
    );
    this.removeOrderFromActivePreparationQueue(fulfillmentQueue, clickAndCollectOrder);
    customer.collectClickAndCollectOrderAtStore(
      clickAndCollectOrder,
      clickAndCollectOrder.clickAndCollectStore,
    );
    return completedFulfillment;
  }

  verifyOrderProofMatchesCustomer(
    clickAndCollectOrder: ClickAndCollectOrder,
    presentedOrderId: string,
    _customer: CustomerFulfillment,
  ): boolean {
    return clickAndCollectOrder.matchesOrderProof(presentedOrderId);
  }
}
