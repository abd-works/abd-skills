/**
 * Find a store — E2E-tier helper (Playwright).
 * RED stubs — awaiting abd-clean-code browser flows.
 */
import {
  FindAStoreBaseHelper,
  type StoreTestData,
} from './find-a-store.base';

export class FindAStoreE2EHelper extends FindAStoreBaseHelper {
  async cleanup(): Promise<void> {
    this.notImplemented('e2e cleanup');
  }

  protected async seedDiscoverySessionWithoutSelectedStore(): Promise<void> {
    this.notImplemented('browser session without selected store');
  }

  protected async seedDiscoverySessionWithSharedLocation(
    _latitude: number,
    _longitude: number,
  ): Promise<void> {
    this.notImplemented('browser session with shared location');
  }

  async whenCustomerCompletesStoreMapDiscoveryFlow(): Promise<void> {
    this.notImplemented('E2E open store map and browse stores');
  }

  async whenCustomerCompletesStoreSelectionOnMapFlow(
    store: StoreTestData,
  ): Promise<void> {
    this.notImplemented(`E2E select ${store.retailLocationIdentity} on map`);
  }

  async whenCustomerCompletesStoreListDiscoveryFlow(): Promise<void> {
    this.notImplemented('E2E open store list');
  }

  async whenCustomerCompletesStoreSelectionOnListFlow(
    store: StoreTestData,
  ): Promise<void> {
    this.notImplemented(`E2E select ${store.retailLocationIdentity} from list`);
  }

  async whenCustomerCompletesShareLocationFlow(
    latitude: number,
    longitude: number,
  ): Promise<void> {
    this.notImplemented(`E2E share location ${latitude},${longitude}`);
  }

  thenBrowserShowsExpectedStoreDiscoveryState(message: string): void {
    this.notImplemented(`E2E assert: ${message}`);
  }
}
