import { CartQuantity } from './cart-quantity';
import { Money } from './money';
import type { Product } from './product';

/** << Entity >> — one product line with cart quantity in a shopping cart. */
export class CartLine {
  readonly product: Product;
  cartQuantity: CartQuantity;

  constructor(product: Product, cartQuantity: CartQuantity) {
    if (!cartQuantity.isPositiveWholeNumber()) {
      throw new Error('cart line cart quantity must be a positive whole number');
    }
    this.product = product;
    this.cartQuantity = cartQuantity;
  }

  lineTotalFromQuantity(unitPrice: Money): Money {
    return unitPrice.multiplyBy(this.cartQuantity.value);
  }

  matchesProduct(product: Product): boolean {
    return this.product.equals(product);
  }
}
