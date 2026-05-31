import { AddProductToCart } from './add-product-to-cart';
import { CartQuantity } from './cart-quantity';
import { RemoveProductFromCart } from './remove-product-from-cart';
import { ShoppingCart } from './shopping-cart';
import { UpdateCartQuantity } from './update-cart-quantity';
import type { CartLine } from './cart-line';
import type { Product } from './product';
import type { SelectedStore } from './selected-store';
import type { StockAvailability } from './stock-availability';

/** << Entity >> — customer session with shopping cart actions. */
export class Customer {
  readonly displayName: string;
  readonly shoppingCart: ShoppingCart;
  readonly selectedStore: SelectedStore;
  private readonly addProductToCartService = new AddProductToCart();
  private readonly updateCartQuantityService = new UpdateCartQuantity();
  private readonly removeProductFromCartService = new RemoveProductFromCart();
  directedToRemove = false;

  constructor(displayName: string, selectedStore: SelectedStore) {
    this.displayName = displayName;
    this.selectedStore = selectedStore;
    this.shoppingCart = new ShoppingCart(this);
  }

  addProductToCart(product: Product, stockAvailability: StockAvailability): CartLine {
    return this.addProductToCartService.placeProductFromCatalog(
      product,
      this.shoppingCart,
      this.shoppingCart.cartLines,
      this,
      stockAvailability,
      this.selectedStore,
    );
  }

  openShoppingCartToViewLines(): readonly CartLine[] {
    return this.shoppingCart.showEachLineWithProductIdentity();
  }

  updateCartQuantityOnLine(cartLine: CartLine, newQuantity: CartQuantity): CartLine {
    return this.updateCartQuantityService.changeCountOnExistingLine(
      cartLine,
      newQuantity,
      this.shoppingCart.cartLines,
      this,
    );
  }

  removeProductFromCartOnLine(cartLine: CartLine): void {
    this.removeProductFromCartService.deleteProductLineFromShoppingCart(
      cartLine,
      this.shoppingCart.cartLines,
      this.shoppingCart,
    );
  }

  continueBrowsingWithPersistedCart(): ShoppingCart {
    this.shoppingCart.persistUpdatedCountsWhileBrowsing();
    return this.shoppingCart;
  }

  browseCatalogWithEmptyCart(): void {
    return;
  }

  directToRemoveProductFromCart(): void {
    this.directedToRemove = true;
  }

  directBackToCatalogOrCart(): void {
    return;
  }
}
