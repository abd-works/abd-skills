import {
  getProduct,
  getRealTimeStock,
  listProductsForStore,
  resetCatalogFixture,
  seedDefaultStock,
  setProductStockLevels,
} from '../../catalog/shared/in-memory-catalog';
import { CartQuantity } from '../shared/src/cart-quantity';
import {
  UnavailableProductException,
  ZeroQuantityRejectedException,
} from '../shared/src/cart-exceptions';
import { Money } from '../shared/src/money';
import { Product } from '../shared/src/product';
import { RemoveProductFromCart } from '../shared/src/remove-product-from-cart';
import type { ShoppingCartDto } from '../shared/src/cart.schema';
import { CartRepository, type CartSessionRecord } from './cart.repository';
import { toShoppingCartDto } from './cart.mapper';

export class CartService {
  constructor(private readonly repository: CartRepository) {}

  resetFixture(): void {
    this.repository.reset();
    resetCatalogFixture();
  }

  seedCatalogDefaults(): void {
    seedDefaultStock();
  }

  createGuestSession(
    sessionId: string,
    displayName: string,
    storeIdentity: string,
  ): ShoppingCartDto {
    const record = this.repository.createGuestSession(
      sessionId,
      displayName,
      storeIdentity,
    );
    return toShoppingCartDto(record.customer);
  }

  getShoppingCart(sessionId: string): ShoppingCartDto {
    const record = this.requireSession(sessionId);
    return toShoppingCartDto(record.customer);
  }

  listCatalogForStore(storeIdentity: string) {
    return listProductsForStore(storeIdentity).map((item) => ({
      catalogItemIdentity: item.catalogItemIdentity,
      unitPrice: item.unitPrice,
      stockLevels: getRealTimeStock(storeIdentity, item.catalogItemIdentity),
    }));
  }

  setStockAvailability(
    sessionId: string,
    catalogItemIdentity: string,
    availability: 'available' | 'unavailable',
  ): void {
    const record = this.requireSession(sessionId);
    const product = this.requireProduct(catalogItemIdentity);
    const levels = availability === 'unavailable' ? 0 : 10;
    setProductStockLevels(
      record.customer.selectedStore.storeIdentity,
      catalogItemIdentity,
      levels,
    );
    record.stockAvailability.setAvailability(
      product,
      record.customer.selectedStore,
      availability,
    );
  }

  addProductToCart(
    sessionId: string,
    catalogItemIdentity: string,
  ): ShoppingCartDto {
    const record = this.requireSession(sessionId);
    const product = this.requireProduct(catalogItemIdentity);
    this.syncStockFromCatalog(record, product);
    try {
      record.customer.addProductToCart(product, record.stockAvailability);
    } catch (error) {
      if (error instanceof UnavailableProductException) {
        return toShoppingCartDto(record.customer, {
          unavailableWarning: `product unavailable: ${catalogItemIdentity}`,
        });
      }
      throw error;
    }
    return toShoppingCartDto(record.customer);
  }

  updateCartQuantity(
    sessionId: string,
    catalogItemIdentity: string,
    cartQuantity: number,
  ): ShoppingCartDto {
    const record = this.requireSession(sessionId);
    const product = this.requireProduct(catalogItemIdentity);
    const cartLine = record.customer.shoppingCart.cartLines.findLineForProduct(product);
    try {
      record.customer.updateCartQuantityOnLine(
        cartLine,
        new CartQuantity(cartQuantity),
      );
    } catch (error) {
      if (error instanceof ZeroQuantityRejectedException) {
        return toShoppingCartDto(record.customer, {
          zeroQuantityRejectedMessage: error.messageToCustomer,
        });
      }
      throw error;
    }
    return toShoppingCartDto(record.customer);
  }

  removeProductFromCart(
    sessionId: string,
    catalogItemIdentity: string,
  ): ShoppingCartDto {
    const record = this.requireSession(sessionId);
    const product = this.requireProduct(catalogItemIdentity);
    const cartLine = record.customer.shoppingCart.cartLines.findLineForProduct(product);
    record.customer.removeProductFromCartOnLine(cartLine);
    return toShoppingCartDto(record.customer);
  }

  viewCartLineForRemoveOffer(sessionId: string, catalogItemIdentity: string): ShoppingCartDto {
    const record = this.requireSession(sessionId);
    const removeService = new RemoveProductFromCart();
    removeService.offerDistinctFromZeroQuantityEdit(record.customer);
    return toShoppingCartDto(record.customer, {
      removeDistinctFromZeroQuantityEdit: true,
    });
  }

  seedCartLine(
    sessionId: string,
    catalogItemIdentity: string,
    cartQuantity: number,
  ): ShoppingCartDto {
    const record = this.requireSession(sessionId);
    const product = this.requireProduct(catalogItemIdentity);
    record.stockAvailability.setAvailability(
      product,
      record.customer.selectedStore,
      'available',
    );
    setProductStockLevels(
      record.customer.selectedStore.storeIdentity,
      catalogItemIdentity,
      10,
    );
    if (record.customer.shoppingCart.cartLines.hasLineForProduct(product)) {
      const line = record.customer.shoppingCart.cartLines.findLineForProduct(product);
      record.customer.updateCartQuantityOnLine(line, new CartQuantity(cartQuantity));
    } else {
      record.customer.addProductToCart(product, record.stockAvailability);
      if (cartQuantity > 1) {
        const line = record.customer.shoppingCart.cartLines.findLineForProduct(product);
        record.customer.updateCartQuantityOnLine(line, new CartQuantity(cartQuantity));
      }
    }
    return toShoppingCartDto(record.customer);
  }

  seedOnlyCartLine(
    sessionId: string,
    catalogItemIdentity: string,
    cartQuantity: number,
  ): ShoppingCartDto {
    this.clearCartLines(sessionId);
    return this.seedCartLine(sessionId, catalogItemIdentity, cartQuantity);
  }

  clearCartLines(sessionId: string): ShoppingCartDto {
    const record = this.requireSession(sessionId);
    const lines = [...record.customer.shoppingCart.cartLines.allLines()];
    for (const line of lines) {
      record.customer.removeProductFromCartOnLine(line);
    }
    return toShoppingCartDto(record.customer);
  }

  private requireSession(sessionId: string) {
    const record = this.repository.findSession(sessionId);
    if (!record) {
      throw new Error(`cart session not found: ${sessionId}`);
    }
    return record;
  }

  private requireProduct(catalogItemIdentity: string): Product {
    const catalogProduct = getProduct(catalogItemIdentity);
    if (!catalogProduct) {
      throw new Error(`product not found: ${catalogItemIdentity}`);
    }
    return new Product(
      catalogProduct.catalogItemIdentity,
      new Money(catalogProduct.unitPrice),
    );
  }

  private syncStockFromCatalog(record: CartSessionRecord, product: Product): void {
    const store = record.customer.selectedStore;
    const stock = getRealTimeStock(store.storeIdentity, product.catalogItemIdentity);
    const status = stock === 0 ? 'unavailable' : 'available';
    record.stockAvailability.setAvailability(product, store, status);
  }
}
