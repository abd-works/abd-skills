/**
 * Manage Cart — shared test data and abstract Given/When/Then steps.
 * Epic: Shop & Pay Online | Sub-epic: Manage Cart | Increment 2 — cart (Sprint 1)
 * Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
 */

export interface CustomerTestData {
  displayName: string;
}

export interface SelectedStoreTestData {
  storeIdentity: string;
}

export interface ProductTestData {
  catalogItemIdentity: string;
  unitPrice: number;
  stockAvailability: 'available' | 'unavailable';
}

export abstract class ManageCartBaseHelper {
  static readonly CUSTOMER_ALEX_RIVERA: CustomerTestData = {
    displayName: 'Alex Rivera',
  };

  static readonly SELECTED_STORE_DOWNTOWN: SelectedStoreTestData = {
    storeIdentity: 'Downtown PawPlace',
  };

  static readonly PRODUCT_PREMIUM_SALMON_KIBBLE: ProductTestData = {
    catalogItemIdentity: 'Premium Salmon Kibble',
    unitPrice: 24.99,
    stockAvailability: 'available',
  };

  static readonly PRODUCT_LIMITED_EDITION_CAT_TREE: ProductTestData = {
    catalogItemIdentity: 'Limited Edition Cat Tree',
    unitPrice: 199.99,
    stockAvailability: 'unavailable',
  };

  static readonly PRODUCT_REFLECTIVE_DOG_LEASH: ProductTestData = {
    catalogItemIdentity: 'Reflective Dog Leash',
    unitPrice: 18.5,
    stockAvailability: 'available',
  };

  protected customer: CustomerTestData = ManageCartBaseHelper.CUSTOMER_ALEX_RIVERA;
  protected selectedStore: SelectedStoreTestData =
    ManageCartBaseHelper.SELECTED_STORE_DOWNTOWN;

  abstract cleanup(): Promise<void>;

  protected notImplemented(step: string): never {
    throw new Error(`RED — ${step} not implemented (awaiting abd-clean-code)`);
  }

  async givenCustomerAlexRiveraHasSelectedStoreDowntownPawPlace(): Promise<void> {
    this.customer = ManageCartBaseHelper.CUSTOMER_ALEX_RIVERA;
    this.selectedStore = ManageCartBaseHelper.SELECTED_STORE_DOWNTOWN;
    await this.seedCustomerWithSelectedStore();
  }

  async givenShoppingCartForCustomerHasNoCartLines(): Promise<void> {
    await this.seedEmptyShoppingCart();
  }

  async givenProductInCatalogScopedToSelectedStore(
    product: ProductTestData,
  ): Promise<void> {
    await this.seedProductInCatalog(product);
  }

  async givenStockAvailabilityForProductAtSelectedStore(
    product: ProductTestData,
    availability: 'available' | 'unavailable',
  ): Promise<void> {
    await this.seedStockAvailability(product, availability);
  }

  async givenShoppingCartHasCartLineForProductWithCartQuantity(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    await this.seedCartLine(product, cartQuantity);
  }

  async givenShoppingCartHasOnlyCartLineForProductWithCartQuantity(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void> {
    await this.seedOnlyCartLine(product, cartQuantity);
  }

  async givenCustomerConfirmedRemoveProductFromCart(
    product: ProductTestData,
  ): Promise<void> {
    await this.seedAfterRemoveConfirmed(product);
  }

  protected abstract seedCustomerWithSelectedStore(): Promise<void>;
  protected abstract seedEmptyShoppingCart(): Promise<void>;
  protected abstract seedProductInCatalog(product: ProductTestData): Promise<void>;
  protected abstract seedStockAvailability(
    product: ProductTestData,
    availability: 'available' | 'unavailable',
  ): Promise<void>;
  protected abstract seedCartLine(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void>;
  protected abstract seedOnlyCartLine(
    product: ProductTestData,
    cartQuantity: number,
  ): Promise<void>;
  protected abstract seedAfterRemoveConfirmed(product: ProductTestData): Promise<void>;
}
