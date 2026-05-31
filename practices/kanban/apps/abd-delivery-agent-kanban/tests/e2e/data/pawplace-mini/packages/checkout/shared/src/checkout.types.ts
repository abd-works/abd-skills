export interface ClickAndCollectStoreOption {
  storeIdentity: string;
  storeAddress: string;
}

export interface BillingAddressDto {
  name: string;
  street: string;
  city: string;
  postalCode: string;
  country: string;
}

export interface CheckoutSessionDto {
  guestOnlyLabel: boolean;
  eligibleStores: ClickAndCollectStoreOption[];
  clickAndCollectStore: ClickAndCollectStoreOption | null;
  email: string;
  billingAddress: BillingAddressDto | null;
  paymentMethodSelected: boolean;
  stripeWaveLabel: string;
  placeOrderBlocked: boolean;
  placeOrderBlockedReason: string | null;
  validationErrors: string[];
  processingPayment: boolean;
  orderTotal: number;
  paymentFailureMessage: string | null;
  billingFieldNames?: string[];
  checkoutSteps?: { store: boolean; billing: boolean; payment: boolean };
  nonCardPaymentOffered?: boolean;
  stripeWaveInvoked?: boolean;
  placedOrderId?: string | null;
}

export interface OrderConfirmationDto {
  orderId: string;
  clickAndCollectStore: string;
  total: number;
  orderConfirmationSent: boolean;
  emailSentTo: string;
  confirmationScreenSummary?: string;
  guestOnly?: boolean;
  billingAddress?: BillingAddressDto | null;
}

export type StripeWaveOutcome = 'success' | 'card declined';
