/**
 * Manage Cart — E2E acceptance tests (Increment 2 Sprint 1).
 *
 * Story path: Shop & Pay Online → Manage Cart → [Story]
 * File: tests/shop-and-pay-online/manage-cart/manage-cart_e2e.spec.ts
 */
import { test } from '@playwright/test';
import { ManageCartE2EHelper } from './helpers/manage-cart.e2e';
import { ManageCartBaseHelper } from './helpers/manage-cart.base';

test.describe('Add Product to Cart — E2E', () => {
  const helper = new ManageCartE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 1: add from product detail creates cart line', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
    await helper.givenShoppingCartForCustomerHasNoCartLines();
    await helper.givenProductInCatalogScopedToSelectedStore(product);
    await helper.whenCustomerCompletesAddToCartFlow(product);
    helper.thenBrowserShowsExpectedCartState(
      'cart line for Premium Salmon Kibble with Cart Quantity 1',
    );
  });

  test('Scenario 2: repeat add merges quantity on single line', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerCompletesAddToCartFlow(product);
    helper.thenBrowserShowsExpectedCartState(
      'exactly one cart line for Premium Salmon Kibble with Cart Quantity 2',
    );
  });
});

test.describe('Update Cart Quantity — E2E', () => {
  const helper = new ManageCartE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 5: updated quantities persist after browsing', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerCompletesUpdateQuantityFlow(product, 3);
    helper.thenBrowserShowsExpectedCartState(
      'Premium Salmon Kibble still shows Cart Quantity 3 after returning to cart',
    );
  });
});

test.describe('Remove Product from Cart — E2E', () => {
  const helper = new ManageCartE2EHelper();

  test.afterEach(async () => {
    await helper.cleanup();
  });

  test('Scenario 3: removing last line blocks checkout entry', async () => {
    const product = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
    await helper.givenShoppingCartHasOnlyCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerCompletesRemoveFromCartFlow(product);
    helper.thenBrowserShowsExpectedCartState(
      'empty shopping cart with guest checkout blocked',
    );
  });
});
