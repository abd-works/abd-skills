import type { ClickAndCollectOrder } from './click-and-collect-order';

export class PreparationIncompleteException extends Error {
  constructor(readonly clickAndCollectOrder: ClickAndCollectOrder) {
    super(
      `preparation is incomplete for click-and-collect order ${clickAndCollectOrder.orderId}`,
    );
    this.name = 'PreparationIncompleteException';
  }
}

export class RepeatPickupBlockedException extends Error {
  constructor(readonly orderId: string) {
    super(`repeat fulfill blocked for click-and-collect order ${orderId}`);
    this.name = 'RepeatPickupBlockedException';
  }
}
