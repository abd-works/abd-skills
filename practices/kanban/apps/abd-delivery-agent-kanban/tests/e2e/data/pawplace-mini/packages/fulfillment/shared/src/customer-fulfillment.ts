import type { ClickAndCollectCartLine } from './click-and-collect-order';
import { ClickAndCollectOrder } from './click-and-collect-order';
import { ClickAndCollectStore } from './click-and-collect-store';

/** << Entity >> — customer receiving products at pickup. */
export class CustomerFulfillment {
  readonly collectedLines: ClickAndCollectCartLine[] = [];

  collectClickAndCollectOrderAtStore(
    clickAndCollectOrder: ClickAndCollectOrder,
    _clickAndCollectStore: ClickAndCollectStore,
  ): void {
    this.collectedLines.push(...clickAndCollectOrder.showLinesForHandoffDetail());
  }
}
