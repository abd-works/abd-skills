import {
  Catalog,
  CatalogStockAvailability,
  ProductStockLevels,
  Products,
  RealTimeStock,
  SelectedStoreContext,
} from '../shared/src/index';

/** In-memory catalog persistence for stock levels and browse context. */
export class CatalogRepository {
  readonly productStockLevels = ProductStockLevels.withDefaultFixture();
  readonly products = Products.supplyDefaultAssortment();
  readonly catalog = new Catalog();
  readonly realTimeStock = new RealTimeStock();
  readonly stockAvailability = new CatalogStockAvailability();

  reset(): void {
    this.productStockLevels.resetFixture();
  }

  selectedStoreFromIdentity(storeIdentity: string): SelectedStoreContext {
    if (!storeIdentity) {
      return SelectedStoreContext.unset();
    }
    const streetAddress =
      storeIdentity === 'Westside PawPlace' ? '42 Oak Avenue' : '100 Main Street';
    return SelectedStoreContext.fromStore(storeIdentity, streetAddress);
  }
}
