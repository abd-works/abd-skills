/**
 * Manage Cart — client-tier helper (Vitest + Testing Library).
 */
import { fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {
  InMemoryCartApi,
  ProductDetailAddButton,
  ShoppingCartView,
} from '@pawplace-mini/cart-client';
import type { ShoppingCartDto } from '@pawplace-mini/cart-shared';
import {
  ManageCartBaseHelper,
  type ProductTestData,
} from './manage-cart.base';

function emptyCart(): ShoppingCartDto {
  return {
    customerDisplayName: ManageCartBaseHelper.CUSTOMER_ALEX_RIVERA.displayName,
    selectedStoreIdentity: ManageCartBaseHelper.SELECTED_STORE_DOWNTOWN.storeIdentity,
    cartLines: [],
    guestCheckoutOffered: false,
    guestCheckoutBlocked: true,
  };
}

function cartWithLine(product: ProductTestData, cartQuantity: number): ShoppingCartDto {
  return {
    customerDisplayName: ManageCartBaseHelper.CUSTOMER_ALEX_RIVERA.displayName,
    selectedStoreIdentity: ManageCartBaseHelper.SELECTED_STORE_DOWNTOWN.storeIdentity,
    cartLines: [
      {
        catalogItemIdentity: product.catalogItemIdentity,
        cartQuantity,
        unitPrice: product.unitPrice,
        lineTotal: product.unitPrice * cartQuantity,
      },
    ],
    guestCheckoutOffered: true,
    guestCheckoutBlocked: false,
    removeDistinctFromZeroQuantityEdit: true,
  };
}

export class ManageCartClientHelper extends ManageCartBaseHelper {
  private cartApi = new InMemoryCartApi(emptyCart());
  private container: HTMLElement | null = null;

  async cleanup(): Promise<void> {
    this.container?.remove();
    this.container = null;
    this.cartApi = new InMemoryCartApi(emptyCart());
  }

  protected async seedCustomerWithSelectedStore(): Promise<void> {
    this.cartApi.setCart(emptyCart());
  }

  protected async seedEmptyShoppingCart(): Promise<void> {
    this.renderShoppingCart(emptyCart());
  }

  protected async seedProductInCatalog(product: ProductTestData): Promise<void> {
    this.cartApi.registerProduct(product.catalogItemIdentity, product.unitPrice);
  }

  protected async seedStockAvailability(
    product: ProductTestData,
    availability: 'available' | 'unavailable',
  ): Promise<void> {
    this.cartApi.registerProduct(product.catalogItemIdentity, product.unitPrice);
    if (availability === 'unavailable') {
      // availability enforced at ProductDetailAddButton render time
    }
  }

  protected async seedCartLine(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    this.cartApi.registerProduct(product.catalogItemIdentity, product.unitPrice);
    this.cartApi.setCart(cartWithLine(product, cartQuantity));
  }

  protected async seedOnlyCartLine(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    await this.seedCartLine(product, cartQuantity);
  }

  protected async seedAfterRemoveConfirmed(_product: ProductTestData): Promise<void> {
    this.cartApi.setCart(emptyCart());
  }

  async whenCustomerClicksAddProductToCart(product: ProductTestData): Promise<void> {
    this.renderProductDetail(product, product.stockAvailability);
    if (product.stockAvailability === 'available') {
      await userEvent.click(screen.getByRole('button', { name: 'add to cart' }));
      this.renderShoppingCart(this.cartApi.currentCart());
    }
  }

  async whenCustomerOpensShoppingCartScreen(): Promise<void> {
    this.renderShoppingCart(this.cartApi.currentCart());
  }

  async whenCustomerChangesCartQuantityOnLine(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    this.renderShoppingCart(this.cartApi.currentCart());
    const input = screen.getByLabelText(`cart quantity ${product.catalogItemIdentity}`);
    fireEvent.change(input, { target: { value: String(cartQuantity) } });
    this.renderShoppingCart(this.cartApi.currentCart());
  }

  async whenCustomerClicksRemoveProductFromCart(product: ProductTestData): Promise<void> {
    this.renderShoppingCart(this.cartApi.currentCart());
    const row = screen.getByText(product.catalogItemIdentity).closest('li');
    if (!row) throw new Error('cart line not found');
    await userEvent.click(within(row).getByRole('button', { name: 'remove' }));
    this.renderShoppingCart(this.cartApi.currentCart());
  }

  thenUiShowsCartLineWithQuantity(
    product: ProductTestData,
    cartQuantity: number,
  ): void {
    const input = screen.getByLabelText(
      `cart quantity ${product.catalogItemIdentity}`,
    ) as HTMLInputElement;
    expect(Number(input.value)).toBe(cartQuantity);
  }

  thenUiShowsUnavailableWarningBeforeLineCreated(product: ProductTestData): void {
    expect(screen.getByRole('alert').textContent).toContain(product.catalogItemIdentity);
  }

  thenUiBlocksGuestCheckoutWhenCartEmpty(): void {
    expect(screen.getByRole('button', { name: 'checkout' })).toBeDisabled();
  }

  thenUiShowsRemoveActionDistinctFromZeroQuantity(_product: ProductTestData): void {
    expect(screen.getByTestId('remove-distinct-from-zero')).toBeInTheDocument();
  }

  private renderShoppingCart(cart: ShoppingCartDto): void {
    this.container?.remove();
    const view = render(
      <ShoppingCartView cartApi={this.cartApi} initialCart={cart} />,
    );
    this.container = view.container;
    this.cartApi.setCart(cart);
  }

  private renderProductDetail(
    product: ProductTestData,
    availability: 'available' | 'unavailable',
  ): void {
    this.container?.remove();
    const view = render(
      <ProductDetailAddButton
        cartApi={this.cartApi}
        catalogItemIdentity={product.catalogItemIdentity}
        stockAvailability={availability}
        onCartUpdated={(next) => this.cartApi.setCart(next)}
      />,
    );
    this.container = view.container;
  }
}
