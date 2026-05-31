/**
 * Stock visibility — client-tier helper (Vitest + Testing Library).
 */
import React from 'react';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect } from 'vitest';
import {
  CatalogListView,
  ProductDetailsView,
} from '@pawplace-mini/catalog-client';
import {
  RequireStoreEmployee,
  StockMaintenanceView,
} from '@pawplace-mini/inventory-client';
import {
  getProduct,
  getRealTimeStock,
  listProductsForStore,
  listStockForStore,
  resetCatalogFixture,
  setProductStockLevels,
} from '../../../../packages/catalog/shared/in-memory-catalog';
import { SelectedStoreProvider } from '../../../../packages/shared/selected-store';
import type { ProductTestData, SelectedStoreTestData } from './stock-visibility.base';

export {
  DOWNTOWN_STORE,
  WESTSIDE_STORE,
  PRODUCT_SALMON,
  PRODUCT_LEASH,
  PRODUCT_CAT_TREE,
} from './stock-visibility.base';

export class StockVisibilityClientHelper {
  private selectedStore: SelectedStoreTestData | null = null;
  private employeeStore: SelectedStoreTestData | null = null;
  private isEmployee = false;
  private stockOverride: Record<string, number> = {};

  async cleanup(): Promise<void> {
    resetCatalogFixture();
    this.selectedStore = null;
    this.employeeStore = null;
    this.isEmployee = false;
    this.stockOverride = {};
  }

  async givenSelectedStore(store: SelectedStoreTestData): Promise<void> {
    resetCatalogFixture();
    this.selectedStore = store;
  }

  async givenNoSelectedStore(): Promise<void> {
    resetCatalogFixture();
    this.selectedStore = null;
  }

  async givenRealTimeStockAtSelectedStore(
    product: ProductTestData,
    quantity: number,
  ): Promise<void> {
    if (!this.selectedStore) {
      throw new Error('selected store required');
    }
    setProductStockLevels(
      this.selectedStore.storeIdentity,
      product.catalogItemIdentity,
      quantity,
    );
    this.stockOverride[product.catalogItemIdentity] = quantity;
  }

  async givenStoreEmployeeAtStore(store: SelectedStoreTestData): Promise<void> {
    resetCatalogFixture();
    this.employeeStore = store;
    this.isEmployee = true;
  }

  async givenCustomerSession(): Promise<void> {
    this.isEmployee = false;
  }

  private resolveStock(product: ProductTestData): number {
    if (this.stockOverride[product.catalogItemIdentity] !== undefined) {
      return this.stockOverride[product.catalogItemIdentity];
    }
    if (!this.selectedStore) return 0;
    return getRealTimeStock(
      this.selectedStore.storeIdentity,
      product.catalogItemIdentity,
    );
  }

  async whenCustomerOpensBrowseCatalog(): Promise<void> {
    cleanup();
    const products = this.selectedStore
      ? listProductsForStore(this.selectedStore.storeIdentity)
      : [];
    render(
      <SelectedStoreProvider initialStore={this.selectedStore}>
        <CatalogListView products={products} />
      </SelectedStoreProvider>,
    );
  }

  async whenCustomerOpensProductDetails(product: ProductTestData): Promise<void> {
    cleanup();
    const catalogProduct = getProduct(product.catalogItemIdentity);
    if (!catalogProduct || !this.selectedStore) {
      throw new Error('missing product or selected store');
    }
    render(
      <SelectedStoreProvider initialStore={this.selectedStore}>
        <ProductDetailsView
          product={catalogProduct}
          realTimeStock={this.resolveStock(product)}
        />
      </SelectedStoreProvider>,
    );
  }

  async whenCustomerAttemptsStockMaintenance(): Promise<void> {
    cleanup();
    const store = this.employeeStore ?? this.selectedStore;
    if (!store) throw new Error('store required');
    render(
      <RequireStoreEmployee isEmployee={this.isEmployee}>
        <StockMaintenanceView
          storeIdentity={store.storeIdentity}
          stockRows={listStockForStore(store.storeIdentity)}
          onSaveLevels={(updates) => {
            for (const row of updates) {
              const result = setProductStockLevels(
                row.storeIdentity,
                row.catalogItemIdentity,
                row.productStockLevels,
              );
              if (!result.ok) return result;
            }
            return { ok: true as const };
          }}
        />
      </RequireStoreEmployee>,
    );
  }

  async whenEmployeeOpensStockMaintenance(): Promise<void> {
    cleanup();
    const store = this.employeeStore;
    if (!store) throw new Error('employee store required');
    render(
      <StockMaintenanceView
        storeIdentity={store.storeIdentity}
        stockRows={listStockForStore(store.storeIdentity)}
        onSaveLevels={(updates) => {
          for (const row of updates) {
            const result = setProductStockLevels(
              row.storeIdentity,
              row.catalogItemIdentity,
              row.productStockLevels,
            );
            if (!result.ok) return result;
          }
          return { ok: true as const };
        }}
      />,
    );
  }

  async whenEmployeeEditsAndSavesLevel(
    product: ProductTestData,
    levels: number,
  ): Promise<void> {
    const user = userEvent.setup();
    const table = screen.getByTestId('stock-list');
    const row = within(table).getByText(product.catalogItemIdentity).closest('tr');
    if (!row) throw new Error(`stock row not found for ${product.catalogItemIdentity}`);
    await user.click(within(row).getByRole('button', { name: 'edit level' }));
    const input = within(row).getByRole('spinbutton');
    fireEvent.change(input, { target: { value: String(levels) } });
    await user.click(screen.getByRole('button', { name: 'save levels' }));
  }

  thenUiShowsProductList(): void {
    expect(screen.getByTestId('product-list')).toBeInTheDocument();
    expect(screen.getByText('Premium Salmon Kibble')).toBeInTheDocument();
    expect(screen.getByText('Reflective Dog Leash')).toBeInTheDocument();
    expect(screen.getByText('Limited Edition Cat Tree')).toBeInTheDocument();
  }

  thenUiShowsProductDetail(product: ProductTestData): void {
    expect(screen.getByTestId('product-details')).toBeInTheDocument();
    expect(screen.getByText(product.catalogItemIdentity)).toBeInTheDocument();
    expect(screen.getByText(product.description)).toBeInTheDocument();
    expect(screen.getByText(`$${product.unitPrice.toFixed(2)}`)).toBeInTheDocument();
  }

  thenUiHasNoCartCheckoutPaymentActions(): void {
    expect(screen.queryByText(/shopping cart/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/checkout/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/payment/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/add to cart/i)).not.toBeInTheDocument();
  }

  thenUiShowsChooseStorePrompt(): void {
    expect(screen.getByTestId('choose-store-prompt')).toBeInTheDocument();
    expect(screen.getByText('choose a store first')).toBeInTheDocument();
  }

  thenUiHasNoProductRows(): void {
    expect(screen.queryByTestId('product-list')).not.toBeInTheDocument();
  }

  thenUiShowsBackToCatalog(): void {
    expect(screen.getByRole('button', { name: 'back to catalog' })).toBeInTheDocument();
  }

  thenUiShowsSelectedStoreContext(store: SelectedStoreTestData): void {
    const chrome = screen.getByTestId('selected-store-chrome');
    expect(chrome.textContent).toContain(store.storeIdentity);
  }

  thenUiShowsRealTimeStock(quantity: number): void {
    expect(screen.getByTestId('real-time-stock')).toHaveTextContent(String(quantity));
  }

  thenUiShowsStockAvailability(availability: 'available' | 'unavailable'): void {
    const badge = screen.getByTestId('stock-availability');
    expect(badge).toHaveAttribute('data-availability', availability);
    expect(badge.textContent).toContain(availability);
  }

  thenRealTimeStockAtStore(
    store: SelectedStoreTestData,
    product: ProductTestData,
    quantity: number,
  ): void {
    expect(
      getRealTimeStock(store.storeIdentity, product.catalogItemIdentity),
    ).toBe(quantity);
  }

  thenUiShowsEditableStockList(): void {
    expect(screen.getByTestId('stock-list')).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: 'edit level' }).length).toBeGreaterThan(0);
    expect(screen.getByRole('button', { name: 'save levels' })).toBeInTheDocument();
  }

  thenUiShowsValidationError(): void {
    expect(screen.getByTestId('validation-error-area')).toBeInTheDocument();
    expect(screen.getByText('validation message')).toBeInTheDocument();
  }

  thenUiDeniesEmployeeRoute(): void {
    expect(screen.getByTestId('employee-access-denied')).toBeInTheDocument();
    expect(screen.queryByTestId('update-stock')).not.toBeInTheDocument();
  }
}
