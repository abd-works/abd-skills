/**
 * Checkout & pay — E2E-tier helper (Playwright).
 */
import assert from 'node:assert/strict';
import type { BillingAddressTestData, StoreTestData } from './checkout.base';
import { CheckoutBaseHelper } from './checkout.base';

export class CheckoutE2EHelper extends CheckoutBaseHelper {
  async cleanup(): Promise<void> {
    this.notImplemented('e2e cleanup');
  }

  async whenCustomerCompletesGuestCheckoutFlow(store: StoreTestData): Promise<void> {
    this.notImplemented(`E2E guest checkout at ${store.storeIdentity}`);
  }

  async whenCustomerCompletesPaymentWithDeclinedCard(store: StoreTestData): Promise<void> {
    this.notImplemented(`E2E declined payment at ${store.storeIdentity}`);
  }

  async whenCustomerViewsOrderConfirmationScreen(): Promise<void> {
    this.notImplemented('E2E order confirmation screen');
  }

  thenBrowserShowsGuestCheckoutWithAllStores(): void {
    assert.fail('RED — E2E guest checkout store list not implemented');
  }

  thenBrowserShowsOrderConfirmationSummary(
    orderId: string,
    store: StoreTestData,
    total: number,
  ): void {
    assert.fail(`RED — E2E confirmation ${orderId} at ${store.storeIdentity} not implemented`);
  }

  thenBrowserShowsPaymentFailureMessage(reason: string): void {
    assert.fail(`RED — E2E payment failure ${reason} not implemented`);
  }

  thenBrowserBlocksPlaceOrderWithoutStore(): void {
    assert.fail('RED — E2E place order blocked without store not implemented');
  }

  thenBrowserShowsBillingValidationErrors(): void {
    assert.fail('RED — E2E billing validation errors not implemented');
  }
}
