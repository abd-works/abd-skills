import type { ProductStockLevels } from './product-stock-levels';
import type { Product } from './product';
import type { SelectedStoreContext } from './selected-store-context';

/** << Entity >> — customer-visible on-hand quantity at one store. */
export class RealTimeStock {
  showOnHandQuantityAtStore(
    product: Product,
    selectedStore: SelectedStoreContext,
    productStockLevels: ProductStockLevels,
  ): number {
    return productStockLevels.onHandCountFor(product, selectedStore);
  }

  reflectLatestProductStockLevels(
    productStockLevels: ProductStockLevels,
    product: Product,
    store: SelectedStoreContext,
  ): number {
    return this.showOnHandQuantityAtStore(product, store, productStockLevels);
  }
}
