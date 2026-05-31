import type { ProductStockLevels } from './product-stock-levels';
import type { RealTimeStock } from './real-time-stock';
import type { Product } from './product';
import { StockAvailabilityStatus } from './stock-availability-status';
import type { SelectedStoreContext } from './selected-store-context';

/** << Service >> — derives stock availability from real-time stock rules. */
export class CatalogStockAvailability {
  deriveFromRealTimeStockRules(
    realTimeStock: RealTimeStock,
    product: Product,
    selectedStore: SelectedStoreContext,
    productStockLevels: ProductStockLevels,
  ): StockAvailabilityStatus {
    const onHandQuantity = realTimeStock.showOnHandQuantityAtStore(
      product,
      selectedStore,
      productStockLevels,
    );
    if (onHandQuantity > 0) {
      return StockAvailabilityStatus.available();
    }
    return StockAvailabilityStatus.unavailable();
  }
}
