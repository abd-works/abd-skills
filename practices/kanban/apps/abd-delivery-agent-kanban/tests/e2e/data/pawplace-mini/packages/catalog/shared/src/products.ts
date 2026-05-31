import { Money } from './money';
import { Product } from './product';
import type { ProductStockLevels } from './product-stock-levels';
import type { SelectedStoreContext } from './selected-store-context';

/** << Entity >> — global product assortment with store-scoped browse. */
export class Products {
  readonly everyCatalogProduct: readonly Product[];

  constructor(everyCatalogProduct: readonly Product[]) {
    this.everyCatalogProduct = everyCatalogProduct;
  }

  static supplyDefaultAssortment(): Products {
    return new Products([
      new Product(
        'Premium Salmon Kibble',
        'grain-free salmon recipe for adult dogs',
        new Money(24.99),
      ),
      new Product(
        'Reflective Dog Leash',
        'high-visibility leash for evening walks',
        new Money(18.5),
      ),
      new Product(
        'Limited Edition Cat Tree',
        'multi-level climbing tower',
        new Money(199.99),
      ),
    ]);
  }

  supplyBrowseInventory(
    selectedStore: SelectedStoreContext,
    productStockLevels: ProductStockLevels,
  ): Product[] {
    if (selectedStore.isUnset()) {
      return [];
    }
    return this.everyCatalogProduct.filter((product) =>
      productStockLevels.hasLevelFor(product, selectedStore),
    );
  }
}
