import { Catalog } from './catalog';
import { CatalogStockAvailability } from './catalog-stock-availability';
import { ProductStockLevels } from './product-stock-levels';
import { Products } from './products';
import { RealTimeStock } from './real-time-stock';
import type { Product } from './product';
import { SelectedStoreContext } from './selected-store-context';

/** << Entity >> — walk-in customer browsing catalog after store selection. */
export class WalkInCustomer {
  readonly displayName: string;
  selectedStore: SelectedStoreContext;
  chooseStorePromptReceived = false;

  constructor(displayName: string, selectedStore: SelectedStoreContext = SelectedStoreContext.unset()) {
    this.displayName = displayName;
    this.selectedStore = selectedStore;
  }

  browseCatalogAfterSelectedStore(
    catalog: Catalog,
    products: Products,
    productStockLevels: ProductStockLevels,
  ) {
    if (this.selectedStore.isUnset()) {
      this.chooseStorePromptReceived = true;
    }
    return catalog.presentProductsAfterSelectedStore(
      this.selectedStore,
      products,
      productStockLevels,
    );
  }

  openProductDetailFromCatalog(
    product: Product,
    catalog: Catalog,
    realTimeStock: RealTimeStock,
    stockAvailability: CatalogStockAvailability,
    productStockLevels: ProductStockLevels,
  ) {
    return catalog.connectProductIdentityToInventory(
      product,
      realTimeStock,
      stockAvailability,
      this.selectedStore,
      productStockLevels,
    );
  }
}

/** << Entity >> — store employee maintaining product stock levels. */
export class StoreEmployee {
  readonly displayName: string;
  readonly storeIdentity: string;

  constructor(displayName: string, storeIdentity: string) {
    this.displayName = displayName;
    this.storeIdentity = storeIdentity;
  }

  saveProductStockLevels(
    product: Product,
    store: SelectedStoreContext,
    proposedQuantity: number,
    productStockLevels: ProductStockLevels,
  ): number {
    productStockLevels.editQuantity(product, store, proposedQuantity);
    return productStockLevels.persistValidUpdate(product, store);
  }
}
