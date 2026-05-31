/**
 * Store pickup — E2E-tier helper (Playwright).
 */
import {
  FulfillmentBaseHelper,
  type ClickAndCollectOrderTestData,
  type ClickAndCollectStoreTestData,
} from './fulfillment.base';

export class FulfillmentE2EHelper extends FulfillmentBaseHelper {
  async cleanup(): Promise<void> {
    this.notImplemented('e2e cleanup');
  }

  protected async seedEmployeeSessionAtStore(
    _store: ClickAndCollectStoreTestData,
  ): Promise<void> {
    this.notImplemented('browser employee session at click-and-collect store');
  }

  protected async seedPaidOrder(_order: ClickAndCollectOrderTestData): Promise<void> {
    this.notImplemented('browser seed paid click-and-collect order');
  }

  protected async seedUnpaidOrder(_order: ClickAndCollectOrderTestData): Promise<void> {
    this.notImplemented('browser seed unpaid checkout session');
  }

  protected async seedCustomerSession(_displayName: string): Promise<void> {
    this.notImplemented(`browser customer session ${displayName}`);
  }

  async whenStoreEmployeeOpensFulfillmentQueueInBrowser(): Promise<void> {
    this.notImplemented('browser navigate to fulfillment queue');
  }

  async whenStoreEmployeeMarksOrderPreparingInBrowser(orderId: string): Promise<void> {
    this.notImplemented(`browser mark preparing ${orderId}`);
  }

  thenBrowserShowsOrderInFulfillmentQueue(orderId: string): void {
    this.notImplemented(`browser queue lists ${orderId}`);
  }
}
