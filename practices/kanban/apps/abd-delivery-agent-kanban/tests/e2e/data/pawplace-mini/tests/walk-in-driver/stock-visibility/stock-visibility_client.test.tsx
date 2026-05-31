/**
 * Stock visibility — client acceptance tests (Increment 1 Sprint 2).
 *
 * Story path: Walk-in driver → Stock visibility → [Story]
 * File: tests/walk-in-driver/stock-visibility/stock-visibility_client.test.tsx
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import {
  StockVisibilityClientHelper,
  DOWNTOWN_STORE,
  WESTSIDE_STORE,
  PRODUCT_SALMON,
  PRODUCT_CAT_TREE,
} from './helpers/stock-visibility.client';

describe('View Product Details — client', () => {
  const helper = new StockVisibilityClientHelper();

  beforeEach(async () => {
    await helper.givenSelectedStore(DOWNTOWN_STORE);
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('View Product Details — AC 1: catalog lists products at store', async () => {
    await helper.whenCustomerOpensBrowseCatalog();
    helper.thenUiShowsProductList();
  });

  it('View Product Details — AC 2: detail names product and description', async () => {
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsProductDetail(PRODUCT_SALMON);
  });

  it('View Product Details — AC 3: scoped no cart checkout payment', async () => {
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiHasNoCartCheckoutPaymentActions();
  });

  it('View Product Details — AC 4: no store prompts choose first', async () => {
    await helper.givenNoSelectedStore();
    await helper.whenCustomerOpensBrowseCatalog();
    helper.thenUiShowsChooseStorePrompt();
    helper.thenUiHasNoProductRows();
  });

  it('View Product Details — AC 5: back preserves selected store', async () => {
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsBackToCatalog();
    helper.thenUiShowsSelectedStoreContext(DOWNTOWN_STORE);
  });
});

describe('Display Real-Time Stock Availability — client', () => {
  const helper = new StockVisibilityClientHelper();

  beforeEach(async () => {
    await helper.givenSelectedStore(DOWNTOWN_STORE);
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Display Real-Time Stock Availability — AC 1: shows on-hand at store', async () => {
    await helper.givenRealTimeStockAtSelectedStore(PRODUCT_SALMON, 12);
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsRealTimeStock(12);
  });

  it('Display Real-Time Stock Availability — AC 2: sellable shows available', async () => {
    await helper.givenRealTimeStockAtSelectedStore(PRODUCT_SALMON, 5);
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsStockAvailability('available');
  });

  it('Display Real-Time Stock Availability — AC 3: zero shows unavailable no cart', async () => {
    await helper.givenRealTimeStockAtSelectedStore(PRODUCT_CAT_TREE, 0);
    await helper.whenCustomerOpensProductDetails(PRODUCT_CAT_TREE);
    helper.thenUiShowsStockAvailability('unavailable');
    helper.thenUiHasNoCartCheckoutPaymentActions();
  });

  it('Display Real-Time Stock Availability — AC 4: employee save updates customer view', async () => {
    await helper.givenRealTimeStockAtSelectedStore(PRODUCT_SALMON, 3);
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsRealTimeStock(3);
    await helper.givenRealTimeStockAtSelectedStore(PRODUCT_SALMON, 9);
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsRealTimeStock(9);
  });

  it('Display Real-Time Stock Availability — AC 5: no cross-store aggregate', async () => {
    await helper.givenRealTimeStockAtSelectedStore(PRODUCT_SALMON, 12);
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsRealTimeStock(12);
    helper.thenRealTimeStockAtStore(WESTSIDE_STORE, PRODUCT_SALMON, 8);
  });
});

describe('Update Product Stock Levels — client', () => {
  const helper = new StockVisibilityClientHelper();

  beforeEach(async () => {
    await helper.givenStoreEmployeeAtStore(DOWNTOWN_STORE);
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Update Product Stock Levels — AC 1: list editable quantities', async () => {
    await helper.whenEmployeeOpensStockMaintenance();
    helper.thenUiShowsEditableStockList();
  });

  it('Update Product Stock Levels — AC 2: valid save updates real-time stock', async () => {
    await helper.whenEmployeeOpensStockMaintenance();
    await helper.whenEmployeeEditsAndSavesLevel(PRODUCT_SALMON, 20);
    helper.thenRealTimeStockAtStore(DOWNTOWN_STORE, PRODUCT_SALMON, 20);
  });

  it('Update Product Stock Levels — AC 3: invalid rejected unchanged', async () => {
    await helper.whenEmployeeOpensStockMaintenance();
    await helper.whenEmployeeEditsAndSavesLevel(PRODUCT_SALMON, -1);
    helper.thenUiShowsValidationError();
    helper.thenRealTimeStockAtStore(DOWNTOWN_STORE, PRODUCT_SALMON, 12);
  });

  it('Update Product Stock Levels — AC 4: other stores unchanged', async () => {
    await helper.whenEmployeeOpensStockMaintenance();
    await helper.whenEmployeeEditsAndSavesLevel(PRODUCT_SALMON, 1);
    helper.thenRealTimeStockAtStore(WESTSIDE_STORE, PRODUCT_SALMON, 8);
  });

  it('Update Product Stock Levels — AC 5: customer blocked reads detail stock', async () => {
    await helper.givenCustomerSession();
    await helper.whenCustomerAttemptsStockMaintenance();
    helper.thenUiDeniesEmployeeRoute();
    await helper.givenSelectedStore(DOWNTOWN_STORE);
    await helper.whenCustomerOpensProductDetails(PRODUCT_SALMON);
    helper.thenUiShowsRealTimeStock(12);
  });
});
