/**
 * Manage Cart — client acceptance tests (Increment 2 Sprint 1).
 *
 * Story path: Shop & Pay Online → Manage Cart → [Story]
 * File: tests/shop-and-pay-online/manage-cart/manage-cart_client.test.tsx
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import { ManageCartClientHelper } from './helpers/manage-cart.client';
import { ManageCartBaseHelper } from './helpers/manage-cart.base';

describe('Add Product to Cart — client', () => {
  const helper = new ManageCartClientHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: product detail add places line in shopping cart', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenShoppingCartForCustomerHasNoCartLines();
    await helper.givenProductInCatalogScopedToSelectedStore(product);
    await helper.whenCustomerClicksAddProductToCart(product);
    helper.thenUiShowsCartLineWithQuantity(product, 1);
  });

  it('Scenario 3: unavailable product shows warning before line created', async () => {
    const product = ManageCartBaseHelper.PRODUCT_LIMITED_EDITION_CAT_TREE;
    await helper.givenProductInCatalogScopedToSelectedStore(product);
    await helper.givenStockAvailabilityForProductAtSelectedStore(
      product,
      'unavailable',
    );
    await helper.whenCustomerClicksAddProductToCart(product);
    helper.thenUiShowsUnavailableWarningBeforeLineCreated(product);
  });

  it('Scenario 5: empty cart blocks guest checkout affordance', async () => {
    await helper.givenShoppingCartForCustomerHasNoCartLines();
    await helper.whenCustomerOpensShoppingCartScreen();
    helper.thenUiBlocksGuestCheckoutWhenCartEmpty();
  });
});

describe('Update Cart Quantity — client', () => {
  const helper = new ManageCartClientHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 2: increased cart quantity updates displayed line total', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerChangesCartQuantityOnLine(product, 3);
    helper.thenUiShowsCartLineWithQuantity(product, 3);
  });
});

describe('Remove Product from Cart — client', () => {
  const helper = new ManageCartClientHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: remove action distinct from zero quantity edit', async () => {
    const product = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 2);
    await helper.whenCustomerOpensShoppingCartScreen();
    helper.thenUiShowsRemoveActionDistinctFromZeroQuantity(product);
  });

  it('Scenario 3: removing last line empties cart UI', async () => {
    const product = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasOnlyCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerClicksRemoveProductFromCart(product);
    helper.thenUiBlocksGuestCheckoutWhenCartEmpty();
  });
});
