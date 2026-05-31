/**
 * Manage Cart — E2E-tier helper (Playwright).
 */
import {
  ManageCartBaseHelper,
  type ProductTestData,
} from './manage-cart.base';

export class ManageCartE2EHelper extends ManageCartBaseHelper {
  async cleanup(): Promise<void> {
    this.notImplemented('e2e cleanup');
  }

  protected async seedCustomerWithSelectedStore(): Promise<void> {
    this.notImplemented('browser session with selected store');
  }

  protected async seedEmptyShoppingCart(): Promise<void> {
    this.notImplemented('browser with empty cart');
  }

  protected async seedProductInCatalog(product: ProductTestData): Promise<void> {
    this.notImplemented(`navigate to product ${product.catalogItemIdentity}`);
  }

  protected async seedStockAvailability(
    product: ProductTestData,
    availability: 'available' | 'unavailable',
  ): Promise<void> {
    this.notImplemented(
      `seed ${availability} stock for ${product.catalogItemIdentity}`,
    );
  }

  protected async seedCartLine(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    this.notImplemented(
      `browser cart with ${product.catalogItemIdentity} qty ${cartQuantity}`,
    );
  }

  protected async seedOnlyCartLine(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    this.notImplemented(
      `browser cart with only ${product.catalogItemIdentity} qty ${cartQuantity}`,
    );
  }

  protected async seedAfterRemoveConfirmed(
    product: ProductTestData,
  ): Promise<void> {
    this.notImplemented(`browser after remove ${product.catalogItemIdentity}`);
  }

  async whenCustomerCompletesAddToCartFlow(product: ProductTestData): Promise<void> {
    this.notImplemented(`E2E add to cart ${product.catalogItemIdentity}`);
  }

  async whenCustomerCompletesUpdateQuantityFlow(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    this.notImplemented(
      `E2E update qty ${cartQuantity} for ${product.catalogItemIdentity}`,
    );
  }

  async whenCustomerCompletesRemoveFromCartFlow(
    product: ProductTestData,
  ): Promise<void> {
    this.notImplemented(`E2E remove ${product.catalogItemIdentity}`);
  }

  thenBrowserShowsExpectedCartState(message: string): void {
    this.notImplemented(`E2E assert: ${message}`);
  }
}
