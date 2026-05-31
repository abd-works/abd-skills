/**
 * Manage Cart — domain acceptance tests (packages/cart/shared).
 * Increment 2 Sprint 1 — typed domain surface from object-model.md.
 */
import { describe, it } from 'vitest';
import assert from 'node:assert/strict';
import {
  AddProductToCart,
  CartQuantity,
  Customer,
  Money,
  Product,
  RemoveProductFromCart,
  SelectedStore,
  ShoppingCart,
  StockAvailability,
  UnavailableProductException,
  UpdateCartQuantity,
  ZeroQuantityRejectedException,
} from '../src/index';

describe('Add Product To Cart (domain)', () => {
  it('merge add into existing product line increases cart quantity without duplicate', () => {
    const store = new SelectedStore('Downtown PawPlace');
    const customer = new Customer('Alex Rivera', store);
    const stock = new StockAvailability();
    const salmon = new Product('Premium Salmon Kibble', new Money(24.99));
    stock.setAvailability(salmon, store, 'available');

    customer.addProductToCart(salmon, stock);
    customer.addProductToCart(salmon, stock);

    assert.equal(customer.shoppingCart.cartLines.lineCount(), 1);
    const line = customer.shoppingCart.cartLines.findLineForProduct(salmon);
    assert.equal(line.cartQuantity.value, 2);
  });

  it('unavailable product add throws UnavailableProductException', () => {
    const store = new SelectedStore('Downtown PawPlace');
    const customer = new Customer('Alex Rivera', store);
    const stock = new StockAvailability();
    const catTree = new Product('Limited Edition Cat Tree', new Money(199.99));
    stock.setAvailability(catTree, store, 'unavailable');
    const addProduct = new AddProductToCart();

    assert.throws(
      () =>
        addProduct.placeProductFromCatalog(
          catTree,
          customer.shoppingCart,
          customer.shoppingCart.cartLines,
          customer,
          stock,
          store,
        ),
      UnavailableProductException,
    );
  });
});

describe('Update Cart Quantity (domain)', () => {
  it('zero cart quantity update throws ZeroQuantityRejectedException', () => {
    const store = new SelectedStore('Downtown PawPlace');
    const customer = new Customer('Alex Rivera', store);
    const stock = new StockAvailability();
    const salmon = new Product('Premium Salmon Kibble', new Money(24.99));
    stock.setAvailability(salmon, store, 'available');
    customer.addProductToCart(salmon, stock);
    customer.addProductToCart(salmon, stock);
    const line = customer.shoppingCart.cartLines.findLineForProduct(salmon);
    const update = new UpdateCartQuantity();

    assert.throws(
      () =>
        update.changeCountOnExistingLine(
          line,
          new CartQuantity(0),
          customer.shoppingCart.cartLines,
          customer,
        ),
      ZeroQuantityRejectedException,
    );
    assert.equal(customer.directedToRemove, true);
  });
});

describe('Remove Product From Cart (domain)', () => {
  it('removing last line empties shopping cart', () => {
    const store = new SelectedStore('Downtown PawPlace');
    const customer = new Customer('Alex Rivera', store);
    const stock = new StockAvailability();
    const leash = new Product('Reflective Dog Leash', new Money(18.5));
    stock.setAvailability(leash, store, 'available');
    customer.addProductToCart(leash, stock);
    const line = customer.shoppingCart.cartLines.findLineForProduct(leash);
    const remove = new RemoveProductFromCart();

    remove.deleteProductLineFromShoppingCart(
      line,
      customer.shoppingCart.cartLines,
      customer.shoppingCart,
    );

    assert.equal(customer.shoppingCart.isEmpty(), true);
    assert.equal(customer.shoppingCart.blockCheckoutEntryWhenEmpty(), true);
  });
});
