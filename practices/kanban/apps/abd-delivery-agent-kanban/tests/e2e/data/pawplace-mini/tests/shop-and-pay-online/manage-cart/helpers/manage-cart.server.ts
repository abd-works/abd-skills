/**

 * Manage Cart — server-tier helper (Supertest + CartService / CartApi).

 */

import assert from 'node:assert/strict';

import type { Express } from 'express';

import request from 'supertest';

import { createAppServer } from '@pawplace-mini/app-server';

import type { CartService } from '@pawplace-mini/cart-server';

import type { ShoppingCartDto } from '@pawplace-mini/cart-shared';

import {

  ManageCartBaseHelper,

  type ProductTestData,

} from './manage-cart.base';



export class ManageCartServerHelper extends ManageCartBaseHelper {

  private readonly app: Express;

  private readonly service: CartService;

  private readonly sessionId = 'test-session';

  private lastCart!: ShoppingCartDto;



  constructor() {

    super();

    const server = createAppServer();

    this.app = server.app;

    this.service = server.service;

  }



  async cleanup(): Promise<void> {

    this.service.resetFixture();

    this.lastCart = undefined as unknown as ShoppingCartDto;

  }



  protected async seedCustomerWithSelectedStore(): Promise<void> {

    const response = await request(this.app)

      .post('/api/v1/sessions')

      .set('x-session-id', this.sessionId)

      .send({

        displayName: this.customer.displayName,

        selectedStoreIdentity: this.selectedStore.storeIdentity,

      });

    assert.equal(response.status, 201);

    this.lastCart = response.body.cart;

  }



  protected async seedEmptyShoppingCart(): Promise<void> {

    await request(this.app)

      .post('/api/v1/sessions')

      .set('x-session-id', this.sessionId)

      .send({

        displayName: this.customer.displayName,

        selectedStoreIdentity: this.selectedStore.storeIdentity,

      });

    const response = await request(this.app)

      .get('/api/v1/cart')

      .set('x-session-id', this.sessionId);

    this.lastCart = response.body;

  }



  protected async seedProductInCatalog(_product: ProductTestData): Promise<void> {

    return;

  }



  protected async seedStockAvailability(

    product: ProductTestData,

    availability: 'available' | 'unavailable',

  ): Promise<void> {

    await this.ensureSession();

    this.service.setStockAvailability(

      this.sessionId,

      product.catalogItemIdentity,

      availability,

    );

  }



  protected async seedCartLine(

    product: ProductTestData,

    cartQuantity: number,

  ): Promise<void> {

    await this.ensureSession();

    this.lastCart = this.service.seedCartLine(

      this.sessionId,

      product.catalogItemIdentity,

      cartQuantity,

    );

  }



  protected async seedOnlyCartLine(

    product: ProductTestData,

    cartQuantity: number,

  ): Promise<void> {

    await this.ensureSession();

    this.lastCart = this.service.seedOnlyCartLine(

      this.sessionId,

      product.catalogItemIdentity,

      cartQuantity,

    );

  }



  protected async seedAfterRemoveConfirmed(product: ProductTestData): Promise<void> {

    await this.ensureSession();

    this.service.seedCartLine(this.sessionId, product.catalogItemIdentity, 2);

    this.lastCart = this.service.removeProductFromCart(

      this.sessionId,

      product.catalogItemIdentity,

    );

  }



  private async ensureSession(): Promise<void> {

    if (this.lastCart) return;

    await this.seedCustomerWithSelectedStore();

  }



  async whenCustomerViewsProductDetailAndRunsAddProductToCart(

    product: ProductTestData,

  ): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .post('/api/v1/cart/lines')

      .set('x-session-id', this.sessionId)

      .send({ catalogItemIdentity: product.catalogItemIdentity });

    this.lastCart = response.body;

  }



  async whenCustomerRunsAddProductToCartAgain(product: ProductTestData): Promise<void> {

    await this.whenCustomerViewsProductDetailAndRunsAddProductToCart(product);

  }



  async whenCustomerAttemptsAddProductToCart(product: ProductTestData): Promise<void> {

    await this.whenCustomerViewsProductDetailAndRunsAddProductToCart(product);

  }



  async whenCustomerOpensShoppingCart(): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .get('/api/v1/cart')

      .set('x-session-id', this.sessionId);

    this.lastCart = response.body;

  }



  async whenCustomerBrowsesCatalogScopedToSelectedStore(): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .get('/api/v1/cart/catalog')

      .query({ store: this.selectedStore.storeIdentity });

    assert.ok(response.body.products.length > 0);

  }



  async whenCustomerRunsUpdateCartQuantityOnLine(

    product: ProductTestData,

    cartQuantity: number,

  ): Promise<void> {

    const response = await request(this.app)

      .patch(`/api/v1/cart/lines/${encodeURIComponent(product.catalogItemIdentity)}`)

      .set('x-session-id', this.sessionId)

      .send({ cartQuantity });

    this.lastCart = response.body;

  }



  async whenCustomerAttemptsUpdateCartQuantityOnLineToZero(

    product: ProductTestData,

  ): Promise<void> {

    await this.whenCustomerRunsUpdateCartQuantityOnLine(product, 0);

  }



  async whenCustomerReturnsToCatalogAndOpensShoppingCartAgain(): Promise<void> {

    await this.whenCustomerBrowsesCatalogScopedToSelectedStore();

    await this.whenCustomerOpensShoppingCart();

  }



  async whenCustomerViewsCartLineOnShoppingCart(product: ProductTestData): Promise<void> {

    await this.whenCustomerOpensShoppingCart();

    this.lastCart = this.service.viewCartLineForRemoveOffer(

      this.sessionId,

      product.catalogItemIdentity,

    );

  }



  async whenCustomerConfirmsRemoveProductFromCart(

    product: ProductTestData,

  ): Promise<void> {

    const response = await request(this.app)

      .delete(`/api/v1/cart/lines/${encodeURIComponent(product.catalogItemIdentity)}`)

      .set('x-session-id', this.sessionId);

    this.lastCart = response.body;

  }



  private findLine(product: ProductTestData) {

    return this.lastCart.cartLines.find(

      (line) => line.catalogItemIdentity === product.catalogItemIdentity,

    );

  }



  thenCartLinesIncludeOneCartLineForProduct(

    product: ProductTestData,

    cartQuantity: number,

    lineTotal: number,

  ): void {

    const line = this.findLine(product);

    assert.ok(line, `expected cart line for ${product.catalogItemIdentity}`);

    assert.equal(line!.cartQuantity, cartQuantity);

    assert.equal(line!.lineTotal, lineTotal);

  }



  thenCartLinesStillHasExactlyOneCartLineForProductWithCartQuantity(

    product: ProductTestData,

    cartQuantity: number,

  ): void {

    const matches = this.lastCart.cartLines.filter(

      (line) => line.catalogItemIdentity === product.catalogItemIdentity,

    );

    assert.equal(matches.length, 1);

    assert.equal(matches[0]!.cartQuantity, cartQuantity);

  }



  thenAddProductToCartPreventsPlacementAndNoCartLineForProduct(

    product: ProductTestData,

  ): void {

    assert.ok(this.lastCart.unavailableWarning);

    assert.equal(this.findLine(product), undefined);

  }



  thenShoppingCartShowsCartLineWithIdentityAndEditableQuantity(

    product: ProductTestData,

    cartQuantity: number,

  ): void {

    const line = this.findLine(product);

    assert.ok(line);

    assert.equal(line!.cartQuantity, cartQuantity);

  }



  thenGuestCheckoutNotOfferedAndCheckoutBlockedWhenEmpty(): void {

    assert.equal(this.lastCart.cartLines.length, 0);

    assert.equal(this.lastCart.guestCheckoutBlocked, true);

    assert.equal(this.lastCart.guestCheckoutOffered, false);

  }



  thenShoppingCartShowsEditableCartQuantityOnEachLine(): void {

    assert.ok(this.lastCart.cartLines.length >= 2);

    for (const line of this.lastCart.cartLines) {

      assert.ok(line.cartQuantity >= 1);

    }

  }



  thenCartLinePersistsCartQuantityAndLineTotal(

    product: ProductTestData,

    cartQuantity: number,

    lineTotal: number,

  ): void {

    const line = this.findLine(product);

    assert.equal(line!.cartQuantity, cartQuantity);

    assert.equal(line!.lineTotal, lineTotal);

  }



  thenUpdateCartQuantityRejectsZeroAndDirectsToRemove(

    product: ProductTestData,

    unchangedQuantity: number,

  ): void {

    assert.ok(this.lastCart.zeroQuantityRejectedMessage);

    assert.equal(this.lastCart.directedToRemove, true);

    assert.equal(this.findLine(product)!.cartQuantity, unchangedQuantity);

  }



  thenCartLineStillShowsCartQuantityAfterBrowsing(

    product: ProductTestData,

    cartQuantity: number,

  ): void {

    assert.equal(this.findLine(product)!.cartQuantity, cartQuantity);

  }



  thenShoppingCartOffersRemoveDistinctFromZeroQuantityEdit(

    _product: ProductTestData,

  ): void {

    assert.equal(this.lastCart.removeDistinctFromZeroQuantityEdit, true);

  }



  thenCartLinesHasNoCartLineForProductAndRemainingUnchanged(

    removed: ProductTestData,

    remaining: ProductTestData,

    remainingQuantity: number,

  ): void {

    assert.equal(this.findLine(removed), undefined);

    assert.equal(this.findLine(remaining)!.cartQuantity, remainingQuantity);

  }



  thenShoppingCartEmptyAndGuestCheckoutBlocked(): void {

    this.thenGuestCheckoutNotOfferedAndCheckoutBlockedWhenEmpty();

  }



  thenNoRestoredCartLineForProduct(removed: ProductTestData): void {

    assert.equal(this.findLine(removed), undefined);

  }

}


