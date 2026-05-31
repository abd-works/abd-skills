import { CatalogStockAvailability } from './catalog-stock-availability';
import type { CatalogStockAvailability as StockAvailabilityService } from './catalog-stock-availability';
import type { ProductStockLevels } from './product-stock-levels';
import type { Products } from './products';
import type { RealTimeStock } from './real-time-stock';
import type { Product } from './product';
import type { SelectedStoreContext } from './selected-store-context';
import { StockAvailabilityStatus } from './stock-availability-status';

export interface ProductCatalogRow {
  catalogItemIdentity: string;
}

export interface ProductDetailView {
  catalogItemIdentity: string;
  description: string;
  unitPrice: number;
  realTimeStock: number;
  stockAvailability: 'available' | 'unavailable';
  selectedStoreIdentity: string;
  cartCheckoutPaymentActionsOffered: boolean;
}

export interface ChooseStorePromptView {
  chooseStorePromptShown: true;
  productRows: ProductCatalogRow[];
}

export type CatalogBrowseView = ProductCatalogRow[] | ChooseStorePromptView;

/** << Service >> — catalog browse and product detail orchestration. */
export class Catalog {
  presentProductsAfterSelectedStore(
    selectedStore: SelectedStoreContext,
    products: Products,
    productStockLevels: ProductStockLevels,
  ): CatalogBrowseView {
    if (selectedStore.isUnset()) {
      return { chooseStorePromptShown: true, productRows: [] };
    }
    const scopedProducts = products.supplyBrowseInventory(selectedStore, productStockLevels);
    return scopedProducts.map((product) => ({
      catalogItemIdentity: product.catalogItemIdentity,
    }));
  }

  connectProductIdentityToInventory(
    product: Product,
    realTimeStock: RealTimeStock,
    stockAvailability: StockAvailabilityService,
    selectedStore: SelectedStoreContext,
    productStockLevels: ProductStockLevels,
  ): ProductDetailView {
    const onHandQuantity = realTimeStock.showOnHandQuantityAtStore(
      product,
      selectedStore,
      productStockLevels,
    );
    const availability = stockAvailability.deriveFromRealTimeStockRules(
      realTimeStock,
      product,
      selectedStore,
      productStockLevels,
    );
    return {
      catalogItemIdentity: product.catalogItemIdentity,
      description: product.description,
      unitPrice: product.unitPrice.amount,
      realTimeStock: onHandQuantity,
      stockAvailability: availability.label,
      selectedStoreIdentity: selectedStore.storeIdentity,
      cartCheckoutPaymentActionsOffered: false,
    };
  }
}

export { StockAvailabilityStatus };
