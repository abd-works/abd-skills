import { ALL_STORES } from '../../store/shared/mockStores';
import type { CheckoutSessionDto } from '@pawplace-mini/checkout-shared';
import type { OrderConfirmationDto } from '@pawplace-mini/checkout-shared';
import type { CheckoutSessionRecord } from './checkout.repository';

const BILLING_FIELD_NAMES = ['name', 'street', 'city', 'postalCode', 'country'] as const;

export function toCheckoutSessionDto(record: CheckoutSessionRecord): CheckoutSessionDto {
  const guest = record.guestCheckout;
  const eligibleStores = ALL_STORES.map((store) => ({
    storeIdentity: store.retailLocationIdentity,
    storeAddress: store.geographicPlacement,
  }));

  const store = guest.clickAndCollectStore;
  const billing = guest.billingAddress;
  const paymentSelected = guest.paymentMethod?.isSelected() ?? false;
  const prerequisitesMet = guest.blockPaymentUntilPrerequisitesMet();

  let placeOrderBlocked = true;
  let placeOrderBlockedReason: string | null = 'complete store, billing, and payment steps first';

  if (!store) {
    placeOrderBlockedReason = 'choose a click-and-collect store before payment';
  } else if (!billing?.isValid()) {
    placeOrderBlockedReason = 'enter a valid billing address before payment';
  } else if (!paymentSelected) {
    placeOrderBlockedReason = 'select card via StripeWave before payment';
  } else if (guest.processingPayment) {
    placeOrderBlockedReason = 'payment is processing';
    placeOrderBlocked = true;
  } else if (prerequisitesMet) {
    placeOrderBlocked = false;
    placeOrderBlockedReason = null;
  }

  const validationErrors: string[] = [];
  if (guest.paymentFailureMessage) {
    validationErrors.push(guest.paymentFailureMessage);
  }

  return {
    guestOnlyLabel: guest.guestOnlyLabel,
    eligibleStores,
    clickAndCollectStore: store
      ? { storeIdentity: store.storeIdentity, storeAddress: store.storeAddress }
      : null,
    email: guest.email,
    billingAddress: billing
      ? {
          name: billing.name,
          street: billing.street,
          city: billing.city,
          postalCode: billing.postalCode,
          country: billing.country,
        }
      : null,
    paymentMethodSelected: paymentSelected,
    stripeWaveLabel: 'Card via StripeWave',
    placeOrderBlocked,
    placeOrderBlockedReason,
    validationErrors,
    processingPayment: guest.processingPayment,
    orderTotal: guest.shoppingCart.calculateOrderTotal().amount,
    paymentFailureMessage: guest.paymentFailureMessage,
    billingFieldNames: [...BILLING_FIELD_NAMES],
    checkoutSteps: buildCheckoutSteps(guest),
    nonCardPaymentOffered: false,
    stripeWaveInvoked: record.stripeWave.lastResult != null || record.placedOrder != null,
    placedOrderId: record.placedOrder?.orderId ?? null,
  };
}

function buildCheckoutSteps(
  guest: CheckoutSessionRecord['guestCheckout'],
): { store: boolean; billing: boolean; payment: boolean } {
  return {
    store: guest.clickAndCollectStore != null,
    billing: guest.billingAddress?.isValid() ?? false,
    payment: guest.paymentMethod?.isSelected() ?? false,
  };
}

export function toOrderConfirmationDto(
  record: CheckoutSessionRecord,
): OrderConfirmationDto | null {
  if (!record.placedOrder || !record.orderConfirmation?.isComplete()) {
    return null;
  }
  const order = record.placedOrder;
  const store = order.clickAndCollectStore;
  return {
    orderId: order.orderId,
    clickAndCollectStore: store?.storeIdentity ?? '',
    total: Math.round(order.orderTotal.amount * 100) / 100,
    orderConfirmationSent: record.orderConfirmation.emailSentTo.length > 0,
    emailSentTo: record.orderConfirmation.emailSentTo,
    confirmationScreenSummary: record.orderConfirmation.confirmationScreenSummary,
    guestOnly: order.guestOnly,
    billingAddress: order.billingAddress
      ? {
          name: order.billingAddress.name,
          street: order.billingAddress.street,
          city: order.billingAddress.city,
          postalCode: order.billingAddress.postalCode,
          country: order.billingAddress.country,
        }
      : null,
  };
}
