/**
 * Checkout & pay — shared test data (Increment 2 Sprint 2).
 */
export interface StoreTestData {
  storeIdentity: string;
  storeAddress: string;
}

export interface BillingAddressTestData {
  name: string;
  street: string;
  city: string;
  postalCode: string;
  country: string;
}

export abstract class CheckoutBaseHelper {
  static readonly STORE_DOWNTOWN: StoreTestData = {
    storeIdentity: 'Downtown PawPlace',
    storeAddress: '123 Main St',
  };

  static readonly STORE_WESTSIDE: StoreTestData = {
    storeIdentity: 'Westside PawPlace',
    storeAddress: '456 Oak Ave',
  };

  static readonly STORE_UPTOWN: StoreTestData = {
    storeIdentity: 'Uptown PawPlace',
    storeAddress: '789 Pine Rd',
  };

  static readonly BILLING_VALID: BillingAddressTestData = {
    name: 'Alex Rivera',
    street: '42 Maple Lane',
    city: 'Toronto',
    postalCode: 'M5V 1A1',
    country: 'Canada',
  };

  static readonly BILLING_REVISED: BillingAddressTestData = {
    name: 'Alex Rivera',
    street: '88 Cedar Court',
    city: 'Toronto',
    postalCode: 'M5V 2B2',
    country: 'Canada',
  };

  static readonly GUEST_EMAIL = 'alex.rivera@example.com';

  static readonly ORDER_TOTAL = 43.49;

  static readonly ORDER_ID = 'CNC-1042';

  abstract cleanup(): Promise<void>;

  protected notImplemented(step: string): never {
    throw new Error(`RED — ${step} not implemented (awaiting abd-clean-code)`);
  }

  async givenShoppingCartForCustomerHasNonEmptyCart(): Promise<void> {
    this.notImplemented('non-empty shopping cart for Alex Rivera');
  }

  async givenShoppingCartForCustomerHasNoCartLines(): Promise<void> {
    this.notImplemented('empty shopping cart for Alex Rivera');
  }

  async givenGuestCheckoutSessionStarted(): Promise<void> {
    this.notImplemented('guest checkout session from non-empty cart');
  }

  async givenClickAndCollectStoreSelectedOnSession(store: StoreTestData): Promise<void> {
    this.notImplemented(`click-and-collect store ${store.storeIdentity} on session`);
  }

  async givenValidBillingAddressOnSession(): Promise<void> {
    this.notImplemented('valid billing address on checkout session');
  }

  async givenPaymentMethodSelectedOnSession(): Promise<void> {
    this.notImplemented('card payment method selected on session');
  }

  async givenStripeWaveWillReportSuccess(): Promise<void> {
    this.notImplemented('StripeWave success outcome');
  }

  async givenStripeWaveWillReportFailure(reason: string): Promise<void> {
    this.notImplemented(`StripeWave failure ${reason}`);
  }
}
