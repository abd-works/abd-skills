import { CartLine } from './cart-line';
import { CartQuantity } from './cart-quantity';
import type { Product } from './product';
import type { AddProductToCart } from './add-product-to-cart';
import type { RemoveProductFromCart } from './remove-product-from-cart';
import type { UpdateCartQuantity } from './update-cart-quantity';

/** << Entity >> — collection of cart lines with merge-on-add rules. */
export class CartLines {
  private readonly lines: CartLine[] = [];

  mergeAddIntoExistingProductLine(
    _addProductToCart: AddProductToCart,
    product: Product,
    cartQuantity: CartQuantity,
  ): CartLine {
    const existingLine = this.findLineForProduct(product);
    const updatedQuantity = existingLine.cartQuantity.increaseBy(cartQuantity.value);
    existingLine.cartQuantity = updatedQuantity;
    return existingLine;
  }

  addNewProductLine(
    _addProductToCart: AddProductToCart,
    product: Product,
    cartQuantity: CartQuantity,
  ): CartLine {
    const newLine = new CartLine(product, cartQuantity);
    this.lines.push(newLine);
    return newLine;
  }

  removeProductLineFromCollection(
    _removeProductFromCart: RemoveProductFromCart,
    cartLine: CartLine,
  ): void {
    const index = this.lines.indexOf(cartLine);
    if (index >= 0) {
      this.lines.splice(index, 1);
    }
  }

  applyQuantityChangeOnLine(
    _updateCartQuantity: UpdateCartQuantity,
    cartLine: CartLine,
    newQuantity: CartQuantity,
  ): CartLine {
    cartLine.cartQuantity = newQuantity;
    return cartLine;
  }

  leaveRemainingLinesUnchanged(excludedLine: CartLine): CartLine[] {
    return this.lines.filter((line) => line !== excludedLine);
  }

  findLineForProduct(product: Product): CartLine {
    const line = this.lines.find((entry) => entry.matchesProduct(product));
    if (!line) {
      throw new Error(`cart line not found for ${product.catalogItemIdentity}`);
    }
    return line;
  }

  hasLineForProduct(product: Product): boolean {
    return this.lines.some((line) => line.matchesProduct(product));
  }

  allLines(): readonly CartLine[] {
    return this.lines;
  }

  isEmpty(): boolean {
    return this.lines.length === 0;
  }

  lineCount(): number {
    return this.lines.length;
  }

  persistCurrentState(): void {
    return;
  }

  clearAll(): void {
    this.lines.length = 0;
  }
}
