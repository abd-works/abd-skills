import { useState } from 'react';
import type { ShoppingCartDto } from '@pawplace-mini/cart-shared';
import type { CartApi } from './cart.api';

interface ShoppingCartViewProps {
  cartApi: CartApi;
  initialCart: ShoppingCartDto;
}

export function ShoppingCartView({ cartApi, initialCart }: ShoppingCartViewProps) {
  const [cart, setCart] = useState(initialCart);

  async function changeQuantity(catalogItemIdentity: string, cartQuantity: number) {
    const next = await cartApi.updateCartQuantity(catalogItemIdentity, cartQuantity);
    setCart({ ...next });
  }

  async function removeLine(catalogItemIdentity: string) {
    const next = await cartApi.removeProductFromCart(catalogItemIdentity);
    setCart({ ...next });
  }

  return (
    <main>
      <h1>Shopping Cart</h1>
      {cart.zeroQuantityRejectedMessage ? (
        <p role="alert">{cart.zeroQuantityRejectedMessage}</p>
      ) : null}
      {cart.cartLines.length === 0 ? (
        <p>browse catalog prompt</p>
      ) : (
        <ul>
          {cart.cartLines.map((line) => (
            <li key={line.catalogItemIdentity}>
              <span>{line.catalogItemIdentity}</span>
              <label>
                cart quantity
                <input
                  aria-label={`cart quantity ${line.catalogItemIdentity}`}
                  type="number"
                  min={1}
                  value={line.cartQuantity}
                  onChange={(event) =>
                    void changeQuantity(line.catalogItemIdentity, Number(event.target.value))
                  }
                />
              </label>
              <span>{line.lineTotal.toFixed(2)}</span>
              <button type="button" onClick={() => void removeLine(line.catalogItemIdentity)}>
                remove
              </button>
            </li>
          ))}
        </ul>
      )}
      <button type="button" disabled={cart.guestCheckoutBlocked}>
        checkout
      </button>
      {cart.removeDistinctFromZeroQuantityEdit ? (
        <span data-testid="remove-distinct-from-zero">remove distinct from zero quantity edit</span>
      ) : null}
    </main>
  );
}

interface ProductDetailAddProps {
  cartApi: CartApi;
  catalogItemIdentity: string;
  stockAvailability: 'available' | 'unavailable';
  onCartUpdated(cart: ShoppingCartDto): void;
}

export function ProductDetailAddButton({
  cartApi,
  catalogItemIdentity,
  stockAvailability,
  onCartUpdated,
}: ProductDetailAddProps) {
  const unavailable = stockAvailability === 'unavailable';
  const [warning, setWarning] = useState<string | null>(
    unavailable ? `stock availability unavailable for ${catalogItemIdentity}` : null,
  );

  async function addToCart() {
    if (unavailable) {
      setWarning(`stock availability unavailable for ${catalogItemIdentity}`);
      return;
    }
    const next = await cartApi.addProductToCart(catalogItemIdentity);
    onCartUpdated(next);
  }

  return (
    <section>
      <h2>{catalogItemIdentity}</h2>
      {warning ? <p role="alert">{warning}</p> : null}
      <button
        type="button"
        disabled={stockAvailability === 'unavailable'}
        onClick={() => void addToCart()}
      >
        add to cart
      </button>
    </section>
  );
}
