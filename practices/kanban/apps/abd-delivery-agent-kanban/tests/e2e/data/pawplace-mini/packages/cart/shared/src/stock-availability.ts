import type { Product } from './product';
import type { SelectedStore } from './selected-store';

export type AvailabilityStatus = 'available' | 'unavailable';

/** << Service >> — stock read at browsing context (Increment 1 boundary). */
export class StockAvailability {
  private readonly availabilityByProduct = new Map<string, AvailabilityStatus>();

  setAvailability(
    product: Product,
    selectedStore: SelectedStore,
    status: AvailabilityStatus,
  ): void {
    this.availabilityByProduct.set(this.key(product, selectedStore), status);
  }

  isUnavailable(product: Product, selectedStore: SelectedStore): boolean {
    return this.lookupAvailability(product, selectedStore) === 'unavailable';
  }

  warnBeforeAddingUnavailableProduct(_customerDisplayName: string, _product: Product): void {
    return;
  }

  blockOrWarnOnUnavailableAdd(
    product: Product,
    selectedStore: SelectedStore,
    customerDisplayName: string,
  ): void {
    if (this.isUnavailable(product, selectedStore)) {
      this.warnBeforeAddingUnavailableProduct(customerDisplayName, product);
    }
  }

  private lookupAvailability(product: Product, selectedStore: SelectedStore): AvailabilityStatus {
    return this.availabilityByProduct.get(this.key(product, selectedStore)) ?? 'available';
  }

  reset(): void {
    this.availabilityByProduct.clear();
  }

  private key(product: Product, selectedStore: SelectedStore): string {
    return `${selectedStore.storeIdentity}::${product.catalogItemIdentity}`;
  }
}
