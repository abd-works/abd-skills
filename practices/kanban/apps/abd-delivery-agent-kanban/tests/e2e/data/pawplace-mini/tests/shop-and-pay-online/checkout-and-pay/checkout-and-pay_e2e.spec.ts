/**
 * Checkout & pay — E2E acceptance tests (Increment 2 Sprint 2).
 *
 * Story path: Shop & Pay Online → Checkout & pay → [Story]
 * File: tests/shop-and-pay-online/checkout-and-pay/checkout-and-pay_e2e.spec.ts
 */
import { test } from '@playwright/test';
import { CheckoutE2EHelper } from './helpers/checkout.e2e';
import { CheckoutBaseHelper } from './helpers/checkout.base';

test.describe('Select Click-and-Collect Store — E2E', () => {
  const helper = new CheckoutE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 1: guest checkout shows all eligible stores', async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.whenCustomerCompletesGuestCheckoutFlow(CheckoutBaseHelper.STORE_DOWNTOWN);
    helper.thenBrowserShowsGuestCheckoutWithAllStores();
  });

  test('Scenario 3: place order blocked without click-and-collect store', async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.givenGuestCheckoutSessionStarted();
    helper.thenBrowserBlocksPlaceOrderWithoutStore();
  });
});

test.describe('Enter Billing Address — E2E', () => {
  const helper = new CheckoutE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 3: incomplete billing shows validation errors', async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
    helper.thenBrowserShowsBillingValidationErrors();
  });
});

test.describe('Process Card Payment via StripeWave — E2E', () => {
  const helper = new CheckoutE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 3: declined card shows failure without order confirmation', async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.whenCustomerCompletesPaymentWithDeclinedCard(CheckoutBaseHelper.STORE_DOWNTOWN);
    helper.thenBrowserShowsPaymentFailureMessage('card declined');
  });
});

test.describe('Confirm Order and Send Confirmation Email — E2E', () => {
  const helper = new CheckoutE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 2: confirmation screen shows order summary', async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.whenCustomerCompletesGuestCheckoutFlow(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.whenCustomerViewsOrderConfirmationScreen();
    helper.thenBrowserShowsOrderConfirmationSummary(
      CheckoutBaseHelper.ORDER_ID,
      CheckoutBaseHelper.STORE_DOWNTOWN,
      CheckoutBaseHelper.ORDER_TOTAL,
    );
  });
});
