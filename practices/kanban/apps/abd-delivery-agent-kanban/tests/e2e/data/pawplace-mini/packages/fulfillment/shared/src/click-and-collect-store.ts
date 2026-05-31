import { FulfillmentQueue } from './fulfillment-queue';

/** << Entity >> — pickup location bound at checkout; scopes fulfillment queue. */
export class ClickAndCollectStore {
  constructor(
    readonly storeIdentity: string,
    readonly displayName: string = storeIdentity,
  ) {}

  scopeFulfillmentQueueToOneLocation(fulfillmentQueue: FulfillmentQueue): FulfillmentQueue {
    return fulfillmentQueue.filterToStoreScope(this);
  }

  equals(other: ClickAndCollectStore): boolean {
    return this.storeIdentity === other.storeIdentity;
  }
}
