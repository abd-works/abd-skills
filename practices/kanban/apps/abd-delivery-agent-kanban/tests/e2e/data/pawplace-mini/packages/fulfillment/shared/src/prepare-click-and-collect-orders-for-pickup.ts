import { ClickAndCollectOrder } from './click-and-collect-order';
import { ClickAndCollectStore } from './click-and-collect-store';
import { FulfillmentQueue, StoreEmployee } from './fulfillment-queue';
import { OrderFulfillment } from './order-fulfillment';
import type { FulfillmentQueueRowDto } from './fulfillment.types';

/** << Service >> — store employee preparation on the fulfillment queue. */
export class PrepareClickAndCollectOrdersForPickup {
  openQueueForClickAndCollectStore(
    fulfillmentQueue: FulfillmentQueue,
    _storeEmployee: StoreEmployee,
    clickAndCollectStore: ClickAndCollectStore,
  ): FulfillmentQueueRowDto[] {
    const scopedQueue =
      clickAndCollectStore.scopeFulfillmentQueueToOneLocation(fulfillmentQueue);
    return scopedQueue.listPaidOrdersAwaitingPreparation();
  }

  listPaidOrdersAwaitingPreparation(
    fulfillmentQueue: FulfillmentQueue,
  ): FulfillmentQueueRowDto[] {
    return fulfillmentQueue.listPaidOrdersAwaitingPreparation();
  }

  markOrderPreparingOrStagingEquivalent(
    clickAndCollectOrder: ClickAndCollectOrder,
    orderFulfillment: OrderFulfillment,
  ): OrderFulfillment {
    return clickAndCollectOrder.transitionToReadyForCollection(this);
  }

  updateStatusToReadyForCollection(
    clickAndCollectOrder: ClickAndCollectOrder,
    orderFulfillment: OrderFulfillment,
  ): OrderFulfillment {
    return this.markOrderPreparingOrStagingEquivalent(
      clickAndCollectOrder,
      orderFulfillment,
    );
  }

  keepOrderScopedToItsClickAndCollectStore(
    clickAndCollectStore: ClickAndCollectStore,
    clickAndCollectOrder: ClickAndCollectOrder,
  ): boolean {
    return clickAndCollectOrder.clickAndCollectStore.equals(clickAndCollectStore);
  }
}
