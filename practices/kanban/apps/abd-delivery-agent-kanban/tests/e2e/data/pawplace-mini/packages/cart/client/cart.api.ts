import type { ShoppingCartDto } from '@pawplace-mini/cart-shared';

export interface CartApi {
  getShoppingCart(): Promise<ShoppingCartDto>;
  addProductToCart(catalogItemIdentity: string): Promise<ShoppingCartDto>;
  updateCartQuantity(catalogItemIdentity: string, cartQuantity: number): Promise<ShoppingCartDto>;
  removeProductFromCart(catalogItemIdentity: string): Promise<ShoppingCartDto>;
}

export class InMemoryCartApi implements CartApi {
  private readonly productPrices = new Map<string, number>();

  constructor(private cart: ShoppingCartDto) {}

  registerProduct(catalogItemIdentity: string, unitPrice: number): void {
    this.productPrices.set(catalogItemIdentity, unitPrice);
  }

  currentCart(): ShoppingCartDto {
    return this.cart;
  }

  async getShoppingCart(): Promise<ShoppingCartDto> {
    return this.cart;
  }

  async addProductToCart(catalogItemIdentity: string): Promise<ShoppingCartDto> {
    const existing = this.cart.cartLines.find(
      (line) => line.catalogItemIdentity === catalogItemIdentity,
    );
    if (existing) {
      existing.cartQuantity += 1;
      existing.lineTotal = existing.unitPrice * existing.cartQuantity;
    } else {
      const unitPrice = this.productPrices.get(catalogItemIdentity) ?? 0;
      this.cart.cartLines.push({
        catalogItemIdentity,
        cartQuantity: 1,
        unitPrice,
        lineTotal: unitPrice,
      });
    }
    this.refreshCheckoutFlags();
    return this.cart;
  }

  setCart(cart: ShoppingCartDto): void {
    this.cart = cart;
  }

  async updateCartQuantity(
    catalogItemIdentity: string,
    cartQuantity: number,
  ): Promise<ShoppingCartDto> {
    if (cartQuantity === 0) {
      this.cart.zeroQuantityRejectedMessage =
        'Update cart quantity must not leave a line with zero cart quantity. Run remove product from cart instead.';
      this.cart.directedToRemove = true;
      return this.cart;
    }
    const line = this.cart.cartLines.find(
      (entry) => entry.catalogItemIdentity === catalogItemIdentity,
    );
    if (line) {
      line.cartQuantity = cartQuantity;
      line.lineTotal = line.unitPrice * cartQuantity;
    }
    return this.cart;
  }

  async removeProductFromCart(catalogItemIdentity: string): Promise<ShoppingCartDto> {
    this.cart.cartLines = this.cart.cartLines.filter(
      (line) => line.catalogItemIdentity !== catalogItemIdentity,
    );
    this.refreshCheckoutFlags();
    return this.cart;
  }

  private refreshCheckoutFlags(): void {
    this.cart.guestCheckoutBlocked = this.cart.cartLines.length === 0;
    this.cart.guestCheckoutOffered = this.cart.cartLines.length > 0;
  }
}
