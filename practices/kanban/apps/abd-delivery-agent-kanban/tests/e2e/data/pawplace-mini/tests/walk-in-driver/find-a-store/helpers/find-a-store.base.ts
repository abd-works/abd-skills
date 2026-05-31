/**
 * Find a store — shared test data and abstract Given/When/Then steps.
 * Epic: Walk-in driver | Sub-epic: Find a store | Increment 1 — Sprint 1
 * Source: docs/increments/1-walk-in-driver/specification/specification-by-example.md
 */
import {
  ALL_STORES,
  ALTERNATE_CUSTOMER_LOCATION,
  PRIMARY_CUSTOMER_LOCATION,
  type StoreRecord,
} from '@pawplace-mini/store-shared';

export { PRIMARY_CUSTOMER_LOCATION, ALTERNATE_CUSTOMER_LOCATION };

export interface CustomerTestData {
  displayName: string;
}

export type StoreTestData = StoreRecord;

export class FindAStoreBaseHelper {
  static readonly CUSTOMER_ALEX_RIVERA: CustomerTestData = {
    displayName: 'Alex Rivera',
  };

  static readonly STORES = ALL_STORES;

  static readonly STORE_DOWNTOWN = ALL_STORES[0];
  static readonly STORE_WESTSIDE = ALL_STORES[1];
  static readonly STORE_UPTOWN = ALL_STORES[2];

  protected customer: CustomerTestData = FindAStoreBaseHelper.CUSTOMER_ALEX_RIVERA;
  protected selectedStore: StoreRecord | null = null;
  protected catalogNavigationCount = 0;

  abstract cleanup(): Promise<void>;

  protected notImplemented(step: string): never {
    throw new Error(`RED — ${step} not implemented (awaiting abd-clean-code)`);
  }

  getSelectedStore(): StoreRecord | null {
    return this.selectedStore;
  }

  getCatalogNavigationCount(): number {
    return this.catalogNavigationCount;
  }

  protected onSelectedStoreChange(store: StoreRecord | null): void {
    this.selectedStore = store;
  }

  protected onProceedToCatalog(): void {
    this.catalogNavigationCount += 1;
  }

  async givenCustomerAlexRiveraHasNoSelectedStore(): Promise<void> {
    this.customer = FindAStoreBaseHelper.CUSTOMER_ALEX_RIVERA;
    this.selectedStore = null;
    await this.seedDiscoverySessionWithoutSelectedStore();
  }

  async givenCustomerAlexRiveraSharesPrimaryLocation(): Promise<void> {
    this.customer = FindAStoreBaseHelper.CUSTOMER_ALEX_RIVERA;
    await this.seedDiscoverySessionWithSharedLocation(
      PRIMARY_CUSTOMER_LOCATION.latitude,
      PRIMARY_CUSTOMER_LOCATION.longitude,
    );
  }

  protected abstract seedDiscoverySessionWithoutSelectedStore(): Promise<void>;
  protected abstract seedDiscoverySessionWithSharedLocation(
    latitude: number,
    longitude: number,
  ): Promise<void>;
}
