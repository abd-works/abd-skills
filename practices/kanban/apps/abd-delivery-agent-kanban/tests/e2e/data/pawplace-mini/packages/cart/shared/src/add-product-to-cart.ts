import { CartQuantity } from './cart-quantity';
import { UnavailableProductException } from './cart-exceptions';
import type { CartLine } from './cart-line';
import type { CartLines } from './cart-lines';
import type { Customer } from './customer';
import type { Product } from './product';
import type { SelectedStore } from './selected-store';
import type { ShoppingCart } from './shopping-cart';
import type { StockAvailability } from './stock-availability';

/** << Service >> — place product from catalog into shopping cart. */
export class AddProductToCart {
  placeProductFromCatalog(
    product: Product,
    shoppingCart: ShoppingCart,
    cartLines: CartLines,
    customer: Customer,
    stockAvailability: StockAvailability,
    selectedStore: SelectedStore,
  ): CartLine {
    if (stockAvailability.isUnavailable(product, selectedStore)) {
      stockAvailability.warnBeforeAddingUnavailableProduct(customer.displayName, product);
      throw new UnavailableProductException(product.catalogItemIdentity);
    }
    if (cartLines.hasLineForProduct(product)) {
      return cartLines.mergeAddIntoExistingProductLine(this, product, CartQuantity.one());
    }
    return cartLines.addNewProductLine(this, product, CartQuantity.one());
  }

  increaseQuantityOnExistingLine(cartLines: CartLines, product: Product): CartLine {
    return cartLines.mergeAddIntoExistingProductLine(this, product, CartQuantity.one());
  }

  createLineWithAtLeastOneQuantity(cartLines: CartLines, product: Product): CartLine {
    return cartLines.addNewProductLine(this, product, CartQuantity.one());
  }

  preventUnavailableProductAdd(
    stockAvailability: StockAvailability,
    product: Product,
    selectedStore: SelectedStore,
  ): void {
    if (stockAvailability.isUnavailable(product, selectedStore)) {
      throw new UnavailableProductException(product.catalogItemIdentity);
    }
  }
}
