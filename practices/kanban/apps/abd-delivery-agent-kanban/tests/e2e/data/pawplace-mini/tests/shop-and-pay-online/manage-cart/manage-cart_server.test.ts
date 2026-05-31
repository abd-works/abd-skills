/**
 * Manage Cart — server acceptance tests (Increment 2 Sprint 1).
 *
 * Story path: Shop & Pay Online → Manage Cart → [Story]
 * File: tests/shop-and-pay-online/manage-cart/manage-cart_server.test.ts
 * Classes: TestAddProductToCart | TestUpdateCartQuantity | TestRemoveProductFromCart
 *
 * Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import { ManageCartServerHelper } from './helpers/manage-cart.server';
import { ManageCartBaseHelper } from './helpers/manage-cart.base';

describe('Add Product to Cart', () => {
  const helper = new ManageCartServerHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: product from catalog detail lands in shopping cart with cart quantity', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenShoppingCartForCustomerHasNoCartLines();
    await helper.givenProductInCatalogScopedToSelectedStore(product);
    await helper.givenStockAvailabilityForProductAtSelectedStore(
      product,
      'available',
    );
    await helper.whenCustomerViewsProductDetailAndRunsAddProductToCart(product);
    helper.thenCartLinesIncludeOneCartLineForProduct(product, 1, 24.99);
  });

  it('Scenario 2: repeat add merges into existing line without duplicate', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerRunsAddProductToCartAgain(product);
    helper.thenCartLinesStillHasExactlyOneCartLineForProductWithCartQuantity(
      product,
      2,
    );
  });

  it('Scenario 3: unavailable product is blocked from shopping cart without acknowledgment', async () => {
    const product = ManageCartBaseHelper.PRODUCT_LIMITED_EDITION_CAT_TREE;
    await helper.givenProductInCatalogScopedToSelectedStore(product);
    await helper.givenStockAvailabilityForProductAtSelectedStore(
      product,
      'unavailable',
    );
    await helper.whenCustomerAttemptsAddProductToCart(product);
    helper.thenAddProductToCartPreventsPlacementAndNoCartLineForProduct(product);
  });

  it('Scenario 4: shopping cart shows product identity and cart quantity after add', async () => {
    const product = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerOpensShoppingCart();
    helper.thenShoppingCartShowsCartLineWithIdentityAndEditableQuantity(product, 1);
  });

  it('Scenario 5: empty shopping cart allows catalog browse but not guest checkout', async () => {
    await helper.givenShoppingCartForCustomerHasNoCartLines();
    await helper.whenCustomerBrowsesCatalogScopedToSelectedStore();
    helper.thenGuestCheckoutNotOfferedAndCheckoutBlockedWhenEmpty();
  });
});

describe('Update Cart Quantity', () => {
  const helper = new ManageCartServerHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: each cart line shows editable cart quantity on shopping cart', async () => {
    const salmon = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    const leash = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(salmon, 1);
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(leash, 2);
    await helper.whenCustomerOpensShoppingCart();
    helper.thenShoppingCartShowsEditableCartQuantityOnEachLine();
  });

  it('Scenario 2: increased cart quantity saves higher count and updates line total', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerRunsUpdateCartQuantityOnLine(product, 3);
    helper.thenCartLinePersistsCartQuantityAndLineTotal(product, 3, 74.97);
  });

  it('Scenario 3: decrease to a positive whole number saves lower count and keeps line', async () => {
    const product = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 4);
    await helper.whenCustomerRunsUpdateCartQuantityOnLine(product, 2);
    helper.thenCartLinePersistsCartQuantityAndLineTotal(product, 2, 37.0);
  });

  it('Scenario 4: zero cart quantity update is rejected and directs to remove product from cart', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 2);
    await helper.whenCustomerAttemptsUpdateCartQuantityOnLineToZero(product);
    helper.thenUpdateCartQuantityRejectsZeroAndDirectsToRemove(product, 2);
  });

  it('Scenario 5: updated cart quantities persist while customer continues browsing', async () => {
    const product = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerRunsUpdateCartQuantityOnLine(product, 3);
    await helper.whenCustomerReturnsToCatalogAndOpensShoppingCartAgain();
    helper.thenCartLineStillShowsCartQuantityAfterBrowsing(product, 3);
  });
});

describe('Remove Product from Cart', () => {
  const helper = new ManageCartServerHelper();

  beforeEach(async () => {
    await helper.givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: remove product from cart is offered distinctly from zero quantity edit', async () => {
    const product = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(product, 2);
    await helper.whenCustomerViewsCartLineOnShoppingCart(product);
    helper.thenShoppingCartOffersRemoveDistinctFromZeroQuantityEdit(product);
  });

  it('Scenario 2: confirmed remove deletes product line from shopping cart', async () => {
    const salmon = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    const leash = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(salmon, 3);
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(leash, 1);
    await helper.whenCustomerConfirmsRemoveProductFromCart(salmon);
    helper.thenCartLinesHasNoCartLineForProductAndRemainingUnchanged(salmon, leash, 1);
  });

  it('Scenario 3: removing last line empties shopping cart and blocks guest checkout', async () => {
    const product = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasOnlyCartLineForProductWithCartQuantity(product, 1);
    await helper.whenCustomerConfirmsRemoveProductFromCart(product);
    helper.thenShoppingCartEmptyAndGuestCheckoutBlocked();
  });

  it('Scenario 4: removing one line leaves remaining lines and cart quantities unchanged', async () => {
    const salmon = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    const leash = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(salmon, 2);
    await helper.givenShoppingCartHasCartLineForProductWithCartQuantity(leash, 3);
    await helper.whenCustomerConfirmsRemoveProductFromCart(salmon);
    helper.thenCartLinesHasNoCartLineForProductAndRemainingUnchanged(salmon, leash, 3);
  });

  it('Scenario 5: customer can add product again after remove without restoring removed line', async () => {
    const salmon = ManageCartBaseHelper.PRODUCT_PREMIUM_SALMON_KIBBLE;
    const leash = ManageCartBaseHelper.PRODUCT_REFLECTIVE_DOG_LEASH;
    await helper.givenCustomerConfirmedRemoveProductFromCart(salmon);
    await helper.whenCustomerBrowsesCatalogScopedToSelectedStore();
    await helper.whenCustomerViewsProductDetailAndRunsAddProductToCart(leash);
    helper.thenNoRestoredCartLineForProduct(salmon);
  });
});
