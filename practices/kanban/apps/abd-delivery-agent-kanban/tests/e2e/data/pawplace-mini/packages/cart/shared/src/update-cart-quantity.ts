import { ZeroQuantityRejectedException } from './cart-exceptions';
import type { CartLine } from './cart-line';
import type { CartLines } from './cart-lines';
import type { CartQuantity } from './cart-quantity';
import type { Customer } from './customer';

/** << Service >> — change cart quantity on an existing line. */
export class UpdateCartQuantity {
  changeCountOnExistingLine(
    cartLine: CartLine,
    newQuantity: CartQuantity,
    cartLines: CartLines,
    customer: Customer,
  ): CartLine {
    if (newQuantity.isZero()) {
      this.rejectZeroQuantityUpdate(customer);
    }
    return cartLines.applyQuantityChangeOnLine(this, cartLine, newQuantity);
  }

  saveHigherCountOnIncrease(
    cartLine: CartLine,
    newQuantity: CartQuantity,
    cartLines: CartLines,
  ): CartLine {
    return cartLines.applyQuantityChangeOnLine(this, cartLine, newQuantity);
  }

  saveLowerPositiveCountOnDecrease(
    cartLine: CartLine,
    newQuantity: CartQuantity,
    cartLines: CartLines,
  ): CartLine {
    return cartLines.applyQuantityChangeOnLine(this, cartLine, newQuantity);
  }

  rejectZeroQuantityUpdate(customer: Customer): never {
    this.directCustomerToRemoveInstead(customer);
    throw new ZeroQuantityRejectedException();
  }

  directCustomerToRemoveInstead(customer: Customer): void {
    customer.directToRemoveProductFromCart();
  }
}
