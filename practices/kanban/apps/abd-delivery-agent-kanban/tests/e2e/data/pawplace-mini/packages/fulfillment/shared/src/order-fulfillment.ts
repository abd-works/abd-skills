import type { OrderFulfillmentStatus } from './fulfillment.types';
import type { PrepareClickAndCollectOrdersForPickup } from './prepare-click-and-collect-orders-for-pickup';
import type { FulfillClickAndCollectOrder } from './fulfill-click-and-collect-order';

/** << Entity >> — lifecycle status for a click-and-collect order at pickup. */
export class OrderFulfillment {
  constructor(private status: OrderFulfillmentStatus) {}

  get currentStatus(): OrderFulfillmentStatus {
    return this.status;
  }

  markAwaitingPreparation(): void {
    this.status = 'awaiting preparation';
  }

  markReadyForCollection(
    _prepareClickAndCollectOrdersForPickup: PrepareClickAndCollectOrdersForPickup,
  ): OrderFulfillment {
    this.status = 'ready for collection';
    return this;
  }

  markComplete(_fulfillClickAndCollectOrder: FulfillClickAndCollectOrder): OrderFulfillment {
    this.status = 'complete';
    return this;
  }

  markCollectedOrClosed(
    _fulfillClickAndCollectOrder: FulfillClickAndCollectOrder,
  ): OrderFulfillment {
    this.status = 'complete';
    return this;
  }

  blockPrematureCompletionBeforePrepare(): boolean {
    return this.status === 'awaiting preparation';
  }

  isAwaitingPreparation(): boolean {
    return this.status === 'awaiting preparation';
  }

  isReadyForCollection(): boolean {
    return this.status === 'ready for collection';
  }

  isComplete(): boolean {
    return (
      this.status === 'complete' ||
      this.status === 'collected' ||
      this.status === 'closed'
    );
  }

  isClosedAgainstRepeatPickup(): boolean {
    return this.isComplete();
  }
}
