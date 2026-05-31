import type { CartLine } from '../shared/src/cart-line';
import type { Customer } from '../shared/src/customer';
import type { CartLineDto, ShoppingCartDto } from '../shared/src/cart.schema';

export function toCartLineDto(line: CartLine): CartLineDto {
  return {
    catalogItemIdentity: line.product.catalogItemIdentity,
    cartQuantity: line.cartQuantity.value,
    unitPrice: line.product.unitPrice.amount,
    lineTotal: line.lineTotalFromQuantity(line.product.unitPrice).amount,
  };
}

export function toShoppingCartDto(
  customer: Customer,
  options?: {
    removeDistinctFromZeroQuantityEdit?: boolean;
    zeroQuantityRejectedMessage?: string;
    unavailableWarning?: string;
  },
): ShoppingCartDto {
  const cartLines = customer.openShoppingCartToViewLines().map(toCartLineDto);
  const isEmpty = customer.shoppingCart.isEmpty();
  return {
    customerDisplayName: customer.displayName,
    selectedStoreIdentity: customer.selectedStore.storeIdentity,
    cartLines,
    guestCheckoutOffered: !isEmpty,
    guestCheckoutBlocked: isEmpty,
    removeDistinctFromZeroQuantityEdit: options?.removeDistinctFromZeroQuantityEdit,
    zeroQuantityRejectedMessage: options?.zeroQuantityRejectedMessage,
    directedToRemove: customer.directedToRemove || undefined,
    unavailableWarning: options?.unavailableWarning,
  };
}
