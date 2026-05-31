import { CartQuantity } from './cart-quantity';
import type { CartLine } from './cart-line';
import type { CartLines } from './cart-lines';
import type { Customer } from './customer';
import type { ShoppingCart } from './shopping-cart';

/** << Service >> — delete product line from shopping cart. */
export class RemoveProductFromCart {
  deleteProductLineFromShoppingCart(
    cartLine: CartLine,
    cartLines: CartLines,
    shoppingCart: ShoppingCart,
  ): void {
    cartLines.removeProductLineFromCollection(this, cartLine);
    this.clearLineCartQuantityOnRemoval(cartLine);
    this.emptyCartWhenLastLineRemoved(shoppingCart, cartLines);
  }

  clearLineCartQuantityOnRemoval(cartLine: CartLine): void {
    cartLine.cartQuantity = new CartQuantity(0);
  }

  offerDistinctFromZeroQuantityEdit(_customer: Customer): void {
    return;
  }

  emptyCartWhenLastLineRemoved(shoppingCart: ShoppingCart, cartLines: CartLines): void {
    if (cartLines.isEmpty()) {
      shoppingCart.blockCheckoutEntryWhenEmpty();
    }
  }
}
