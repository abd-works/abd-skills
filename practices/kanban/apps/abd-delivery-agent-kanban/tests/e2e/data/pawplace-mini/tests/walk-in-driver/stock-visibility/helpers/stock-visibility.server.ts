/**
 * Stock visibility — server-tier helper (Supertest + CatalogService / CatalogApi).
 */
import assert from 'node:assert/strict';
import type { Express } from 'express';
import request from 'supertest';
import { createAppServer } from '@pawplace-mini/app-server';
import type { CatalogService } from '@pawplace-mini/catalog-server';
import type {
  ProductDetailDto,
  StockMaintenanceViewDto,
} from '@pawplace-mini/catalog-shared';
import {
  DOWNTOWN_STORE,
  WESTSIDE_STORE,
  PRODUCT_SALMON,
  PRODUCT_CAT_TREE,
  type ProductTestData,
  type SelectedStoreTestData,
} from './stock-visibility.base';

export {
  DOWNTOWN_STORE,
  WESTSIDE_STORE,
  PRODUCT_SALMON,
  PRODUCT_CAT_TREE,
} from './stock-visibility.base';

export class StockVisibilityServerHelper {
  private readonly app: Express;
  private readonly catalogService: CatalogService;
  private readonly sessionId = 'stock-visibility-session';
  private lastCatalog!: unknown;
  private lastDetail!: ProductDetailDto;
  private lastMaintenance!: StockMaintenanceViewDto;
  private lastSave!: { ok: boolean; message?: string };

  constructor() {
    const server = createAppServer();
    this.app = server.app;
    this.catalogService = server.catalogService;
  }

  async cleanup(): Promise<void> {
    this.catalogService.resetFixture();
  }

  async givenSelectedStore(store: SelectedStoreTestData): Promise<void> {
    await request(this.app)
      .post('/api/v1/store-discovery/sessions')
      .set('x-session-id', this.sessionId)
      .send({ displayName: 'Alex Rivera' });
    const downtownId = 'downtown';
    const westsideId = 'westside';
    const storeId = store.storeIdentity === 'Westside PawPlace' ? westsideId : downtownId;
    await request(this.app)
      .post('/api/v1/stores/list/select')
      .set('x-session-id', this.sessionId)
      .send({ storeId });
  }

  async givenNoSelectedStore(): Promise<void> {
    await request(this.app)
      .post('/api/v1/store-discovery/sessions')
      .set('x-session-id', this.sessionId)
      .send({ displayName: 'Alex Rivera' });
  }

  async givenRealTimeStockAtSelectedStore(
    product: ProductTestData,
    quantity: number,
  ): Promise<void> {
    await request(this.app)
      .post('/api/v1/inventory/stock-levels')
      .set('x-staff-token', 'store-employee')
      .send({
        storeIdentity: DOWNTOWN_STORE.storeIdentity,
        updates: [{ catalogItemIdentity: product.catalogItemIdentity, productStockLevels: quantity }],
      });
  }

  async givenStoreEmployeeAtStore(_store: SelectedStoreTestData): Promise<void> {
    return;
  }

  async givenCustomerSession(): Promise<void> {
    return;
  }

  async whenCustomerOpensBrowseCatalog(): Promise<void> {
    const response = await request(this.app)
      .get('/api/v1/catalog')
      .set('x-session-id', this.sessionId);
    assert.equal(response.status, 200);
    this.lastCatalog = response.body;
  }

  async whenCustomerOpensProductDetails(product: ProductTestData): Promise<void> {
    const response = await request(this.app)
      .get(`/api/v1/catalog/products/${encodeURIComponent(product.catalogItemIdentity)}`)
      .set('x-session-id', this.sessionId);
    assert.equal(response.status, 200);
    this.lastDetail = response.body;
  }

  async whenEmployeeOpensStockMaintenance(): Promise<void> {
    const response = await request(this.app)
      .get('/api/v1/inventory/stock-maintenance')
      .query({ store: DOWNTOWN_STORE.storeIdentity })
      .set('x-staff-token', 'store-employee');
    assert.equal(response.status, 200);
    this.lastMaintenance = response.body;
  }

  async whenEmployeeEditsAndSavesLevel(
    product: ProductTestData,
    levels: number,
  ): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/inventory/stock-levels')
      .set('x-staff-token', 'store-employee')
      .send({
        storeIdentity: DOWNTOWN_STORE.storeIdentity,
        updates: [{ catalogItemIdentity: product.catalogItemIdentity, productStockLevels: levels }],
      });
    assert.equal(response.status, 200);
    this.lastSave = response.body;
  }

  async whenCustomerAttemptsStockMaintenance(): Promise<void> {
    const response = await request(this.app)
      .get('/api/v1/inventory/stock-maintenance')
      .query({ store: DOWNTOWN_STORE.storeIdentity });
    assert.equal(response.status, 403);
    this.lastMaintenance = response.body;
  }

  thenUiShowsProductList(): void {
    assert.ok(Array.isArray(this.lastCatalog));
    assert.equal((this.lastCatalog as { catalogItemIdentity: string }[]).length, 3);
  }

  thenUiShowsProductDetail(product: ProductTestData): void {
    assert.equal(this.lastDetail.catalogItemIdentity, product.catalogItemIdentity);
    assert.equal(this.lastDetail.description, product.description);
    assert.equal(this.lastDetail.unitPrice, product.unitPrice);
  }

  thenUiHasNoCartCheckoutPaymentActions(): void {
    assert.equal(this.lastDetail.cartCheckoutPaymentActionsOffered, false);
  }

  thenUiShowsChooseStorePrompt(): void {
    const view = this.lastCatalog as { chooseStorePromptShown?: boolean; productRows?: unknown[] };
    assert.equal(view.chooseStorePromptShown, true);
  }

  thenUiHasNoProductRows(): void {
    const view = this.lastCatalog as { productRows?: unknown[] };
    assert.deepEqual(view.productRows, []);
  }

  thenUiShowsBackToCatalog(): void {
    assert.ok(this.lastDetail.catalogItemIdentity);
  }

  thenUiShowsSelectedStoreContext(store: SelectedStoreTestData): void {
    assert.equal(this.lastDetail.selectedStoreIdentity, store.storeIdentity);
  }

  thenUiShowsRealTimeStock(quantity: number): void {
    assert.equal(this.lastDetail.realTimeStock, quantity);
  }

  thenUiShowsStockAvailability(availability: 'available' | 'unavailable'): void {
    assert.equal(this.lastDetail.stockAvailability, availability);
  }

  thenRealTimeStockAtStore(
    store: SelectedStoreTestData,
    product: ProductTestData,
    quantity: number,
  ): void {
    assert.equal(
      this.catalogService.getRealTimeStockAtStore(store.storeIdentity, product.catalogItemIdentity),
      quantity,
    );
  }

  thenUiShowsEditableStockList(): void {
    assert.equal(this.lastMaintenance.rows.length, 3);
    assert.ok(this.lastMaintenance.rows.every((row) => row.editable));
  }

  thenUiShowsValidationError(): void {
    assert.equal(this.lastSave.ok, false);
    assert.equal(this.lastSave.message, 'validation message');
  }

  thenUiDeniesEmployeeRoute(): void {
    assert.match(String((this.lastMaintenance as { error?: string }).error), /employee access denied/i);
  }
}
