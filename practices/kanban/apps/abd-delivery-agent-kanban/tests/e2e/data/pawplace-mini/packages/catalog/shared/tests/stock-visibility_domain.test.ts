/**
 * Stock visibility — domain acceptance tests (packages/catalog/shared).
 * Increment 1 Sprint 2 — typed domain surface from object-model.md.
 */
import { describe, it, beforeEach } from 'vitest';
import assert from 'node:assert/strict';
import {
  Catalog,
  CatalogStockAvailability,
  Product,
  ProductStockLevels,
  Products,
  RealTimeStock,
  SelectedStoreContext,
  StoreEmployee,
  WalkInCustomer,
} from '../src/index';

describe('View Product Details (domain)', () => {
  let products: Products;
  let productStockLevels: ProductStockLevels;
  let downtown: SelectedStoreContext;

  beforeEach(() => {
    products = Products.supplyDefaultAssortment();
    productStockLevels = ProductStockLevels.withDefaultFixture();
    downtown = SelectedStoreContext.fromStore('Downtown PawPlace', '100 Main Street');
  });

  it('Scenario 1: catalog lists products scoped to the selected store', () => {
    const customer = new WalkInCustomer('Alex Rivera', downtown);
    const catalog = new Catalog();

    const rows = customer.browseCatalogAfterSelectedStore(catalog, products, productStockLevels);

    assert.ok(Array.isArray(rows));
    assert.equal((rows as { catalogItemIdentity: string }[]).length, 3);
  });

  it('Scenario 4: catalog browse without selected store prompts store choice first', () => {
    const customer = new WalkInCustomer('Alex Rivera');
    const catalog = new Catalog();

    const view = customer.browseCatalogAfterSelectedStore(catalog, products, productStockLevels);

    assert.equal(customer.chooseStorePromptReceived, true);
    assert.equal((view as { chooseStorePromptShown: boolean }).chooseStorePromptShown, true);
  });
});

describe('Display Real-Time Stock Availability (domain)', () => {
  let products: Products;
  let productStockLevels: ProductStockLevels;
  let downtown: SelectedStoreContext;
  let westside: SelectedStoreContext;
  let catalog: Catalog;
  let realTimeStock: RealTimeStock;
  let stockAvailability: CatalogStockAvailability;

  beforeEach(() => {
    products = Products.supplyDefaultAssortment();
    productStockLevels = ProductStockLevels.withDefaultFixture();
    downtown = SelectedStoreContext.fromStore('Downtown PawPlace', '100 Main Street');
    westside = SelectedStoreContext.fromStore('Westside PawPlace', '42 Oak Avenue');
    catalog = new Catalog();
    realTimeStock = new RealTimeStock();
    stockAvailability = new CatalogStockAvailability();
  });

  it('Scenario 1: product detail shows real-time stock at the selected store', () => {
    const customer = new WalkInCustomer('Alex Rivera', downtown);
    const salmon = products.everyCatalogProduct[0]!;

    const detail = customer.openProductDetailFromCatalog(
      salmon,
      catalog,
      realTimeStock,
      stockAvailability,
      productStockLevels,
    );

    assert.equal(detail.realTimeStock, 12);
  });

  it('Scenario 3: zero on-hand shows unavailable without cart actions', () => {
    const customer = new WalkInCustomer('Alex Rivera', downtown);
    const catTree = products.everyCatalogProduct[2]!;

    const detail = customer.openProductDetailFromCatalog(
      catTree,
      catalog,
      realTimeStock,
      stockAvailability,
      productStockLevels,
    );

    assert.equal(detail.stockAvailability, 'unavailable');
    assert.equal(detail.cartCheckoutPaymentActionsOffered, false);
  });

  it('Scenario 5: stock counts apply only to selected store never aggregate all stores', () => {
    const customer = new WalkInCustomer('Alex Rivera', downtown);
    const salmon = products.everyCatalogProduct[0]!;

    const detail = customer.openProductDetailFromCatalog(
      salmon,
      catalog,
      realTimeStock,
      stockAvailability,
      productStockLevels,
    );

    assert.equal(detail.realTimeStock, 12);
    assert.notEqual(
      detail.realTimeStock,
      productStockLevels.onHandCountFor(salmon, downtown) +
        productStockLevels.onHandCountFor(salmon, westside),
    );
  });
});

describe('Update Product Stock Levels (domain)', () => {
  let products: Products;
  let productStockLevels: ProductStockLevels;
  let downtown: SelectedStoreContext;
  let westside: SelectedStoreContext;
  let employee: StoreEmployee;
  let salmon: Product;

  beforeEach(() => {
    products = Products.supplyDefaultAssortment();
    productStockLevels = ProductStockLevels.withDefaultFixture();
    downtown = SelectedStoreContext.fromStore('Downtown PawPlace', '100 Main Street');
    westside = SelectedStoreContext.fromStore('Westside PawPlace', '42 Oak Avenue');
    employee = new StoreEmployee('Jordan Lee', 'Downtown PawPlace');
    salmon = products.everyCatalogProduct[0]!;
  });

  it('Scenario 2: valid quantity save updates real-time stock', () => {
    const saved = employee.saveProductStockLevels(salmon, downtown, 2, productStockLevels);
    const realTimeStock = new RealTimeStock();

    assert.equal(saved, 2);
    assert.equal(realTimeStock.showOnHandQuantityAtStore(salmon, downtown, productStockLevels), 2);
  });

  it('Scenario 3: invalid quantity is rejected and prior levels stay unchanged', () => {
    employee.saveProductStockLevels(salmon, downtown, -3, productStockLevels);

    assert.equal(productStockLevels.lastValidationMessage, 'validation message');
    assert.equal(productStockLevels.onHandCountFor(salmon, downtown), 12);
  });

  it('Scenario 4: stock update at one store leaves other stores unchanged', () => {
    employee.saveProductStockLevels(salmon, downtown, 4, productStockLevels);

    assert.equal(productStockLevels.onHandCountFor(salmon, downtown), 4);
    assert.equal(productStockLevels.onHandCountFor(salmon, westside), 8);
  });
});
