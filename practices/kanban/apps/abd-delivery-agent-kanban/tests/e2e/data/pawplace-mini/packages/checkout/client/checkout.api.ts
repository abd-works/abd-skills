import type {
  BillingAddressDto,
  CheckoutSessionDto,
  ClickAndCollectStoreOption,
  OrderConfirmationDto,
  StripeWaveOutcome,
} from '../shared/src/checkout.types';

export interface CheckoutApi {
  getSession(): CheckoutSessionDto;
  selectClickAndCollectStore(storeIdentity: string): Promise<CheckoutSessionDto>;
  setGuestEmail(email: string): Promise<CheckoutSessionDto>;
  enterBillingAddress(address: BillingAddressDto): Promise<CheckoutSessionDto>;
  selectPaymentMethod(): Promise<CheckoutSessionDto>;
  placeOrder(): Promise<{ session: CheckoutSessionDto; confirmation: OrderConfirmationDto | null }>;
  setStripeWaveOutcome(outcome: StripeWaveOutcome): void;
  getLastConfirmation(): OrderConfirmationDto | null;
}

const DEFAULT_STORES: ClickAndCollectStoreOption[] = [
  { storeIdentity: 'Downtown PawPlace', storeAddress: '123 Main St' },
  { storeIdentity: 'Westside PawPlace', storeAddress: '456 Oak Ave' },
  { storeIdentity: 'Uptown PawPlace', storeAddress: '789 Pine Rd' },
];

export class InMemoryCheckoutApi implements CheckoutApi {
  private session: CheckoutSessionDto;
  private stripeWaveOutcome: StripeWaveOutcome = 'success';
  private lastConfirmation: OrderConfirmationDto | null = null;
  private orderSequence = 1042;

  constructor(orderTotal = 43.49) {
    this.session = this.freshSession(orderTotal);
  }

  private freshSession(orderTotal: number): CheckoutSessionDto {
    return {
      guestOnlyLabel: true,
      eligibleStores: [...DEFAULT_STORES],
      clickAndCollectStore: null,
      email: '',
      billingAddress: null,
      paymentMethodSelected: false,
      stripeWaveLabel: 'StripeWave',
      placeOrderBlocked: true,
      placeOrderBlockedReason: 'click-and-collect store required',
      validationErrors: [],
      processingPayment: false,
      orderTotal,
      paymentFailureMessage: null,
    };
  }

  getSession(): CheckoutSessionDto {
    return this.session;
  }

  setStripeWaveOutcome(outcome: StripeWaveOutcome): void {
    this.stripeWaveOutcome = outcome;
  }

  getLastConfirmation(): OrderConfirmationDto | null {
    return this.lastConfirmation;
  }

  reset(orderTotal = 43.49): void {
    this.session = this.freshSession(orderTotal);
    this.lastConfirmation = null;
    this.stripeWaveOutcome = 'success';
  }

  async selectClickAndCollectStore(storeIdentity: string): Promise<CheckoutSessionDto> {
    const store = this.session.eligibleStores.find((s) => s.storeIdentity === storeIdentity);
    if (store) {
      this.session.clickAndCollectStore = store;
    }
    this.refreshPlaceOrderState();
    return this.session;
  }

  async setGuestEmail(email: string): Promise<CheckoutSessionDto> {
    this.session.email = email;
    return this.session;
  }

  async enterBillingAddress(address: BillingAddressDto): Promise<CheckoutSessionDto> {
    const errors: string[] = [];
    if (!address.name.trim()) errors.push('name required');
    if (!address.street.trim()) errors.push('street required');
    if (!address.city.trim()) errors.push('city required');
    if (!address.postalCode.trim()) errors.push('postal code required');
    if (!address.country.trim()) errors.push('country required');

    if (errors.length > 0) {
      this.session.validationErrors = errors;
      this.session.billingAddress = null;
    } else {
      this.session.validationErrors = [];
      this.session.billingAddress = { ...address };
    }
    this.refreshPlaceOrderState();
    return this.session;
  }

  async selectPaymentMethod(): Promise<CheckoutSessionDto> {
    this.session.paymentMethodSelected = true;
    this.refreshPlaceOrderState();
    return this.session;
  }

  async placeOrder(): Promise<{
    session: CheckoutSessionDto;
    confirmation: OrderConfirmationDto | null;
  }> {
    if (this.session.placeOrderBlocked || this.session.processingPayment) {
      return { session: this.session, confirmation: null };
    }

    this.session.processingPayment = true;
    this.session.paymentFailureMessage = null;

    if (this.stripeWaveOutcome === 'card declined') {
      this.session.processingPayment = false;
      this.session.paymentFailureMessage = 'card declined';
      this.session.validationErrors = ['card declined'];
      return { session: this.session, confirmation: null };
    }

    const orderId = `CNC-${this.orderSequence}`;
    this.orderSequence += 1;
    this.lastConfirmation = {
      orderId,
      clickAndCollectStore: this.session.clickAndCollectStore!.storeIdentity,
      total: this.session.orderTotal,
      orderConfirmationSent: true,
      emailSentTo: this.session.email,
    };
    this.session.processingPayment = false;
    return { session: this.session, confirmation: this.lastConfirmation };
  }

  private refreshPlaceOrderState(): void {
    const errors: string[] = [];
    if (!this.session.clickAndCollectStore) {
      errors.push('click-and-collect store required');
    }
    if (!this.session.billingAddress) {
      errors.push('billing address required');
    }
    if (!this.session.paymentMethodSelected) {
      errors.push('payment method required');
    }

    this.session.placeOrderBlocked = errors.length > 0 || this.session.processingPayment;
    this.session.placeOrderBlockedReason = errors[0] ?? null;
    if (this.session.billingAddress) {
      this.session.validationErrors = this.session.validationErrors.filter(
        (e) => !['name required', 'street required', 'city required', 'postal code required', 'country required'].includes(e),
      );
    }
  }
}
