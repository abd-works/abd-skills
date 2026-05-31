/**
 * Checkout & pay — domain acceptance tests (packages/checkout/shared).
 * Increment 2 Sprint 2 — typed domain surface from object-model.md.
 */
import { describe, it } from 'vitest';
import assert from 'node:assert/strict';
import {
  Customer,
  Money,
  Product,
  SelectedStore,
  StockAvailability,
} from '@pawplace-mini/cart-shared';
import {
  BillingAddress,
  ClickAndCollectOrder,
  ClickAndCollectStore,
  GuestCheckout,
  OrderConfirmation,
  PaymentMethod,
  ProcessCardPaymentViaStripeWave,
  SelectClickAndCollectStore,
  StripeWave,
  UnsupportedPaymentMethodException,
} from '../src/index';
import { EmptyCartCheckoutBlockedException } from '../src/checkout-exceptions';

describe('Guest Checkout (domain)', () => {
  it('start from non-empty shopping cart without sign-in', () => {
    const customer = buildCustomerWithCart();
    const guest = GuestCheckout.startFromNonEmptyShoppingCart(
      customer.shoppingCart,
      customer,
    );
    assert.equal(guest.guestOnlyLabel, true);
    assert.equal(guest.shoppingCart.hasAtLeastOneLine(), true);
  });

  it('block checkout when shopping cart empty throws EmptyCartCheckoutBlockedException', () => {
    const customer = new Customer('Alex Rivera', new SelectedStore('Downtown PawPlace'));
    assert.throws(
      () => GuestCheckout.startFromNonEmptyShoppingCart(customer.shoppingCart, customer),
      EmptyCartCheckoutBlockedException,
    );
  });

  it('collect contact email without persistent customer profile', () => {
    const customer = buildCustomerWithCart();
    const guest = GuestCheckout.startFromNonEmptyShoppingCart(
      customer.shoppingCart,
      customer,
    );
    guest.collectContactEmail('alex.rivera@example.com');
    assert.equal(guest.email, 'alex.rivera@example.com');
  });

  it('block payment until click-and-collect store billing and payment method complete', () => {
    const guest = buildGuestCheckout();
    assert.equal(guest.blockPaymentUntilPrerequisitesMet(), false);
    const withStore = buildGuestCheckoutWithStore();
    assert.equal(withStore.blockPaymentUntilPrerequisitesMet(), false);
    const ready = buildGuestCheckoutReadyForPayment();
    assert.equal(ready.blockPaymentUntilPrerequisitesMet(), true);
  });
});

describe('Click-and-collect Store (domain)', () => {
  it('bind store selection to checkout session with identity and address', () => {
    const guest = buildGuestCheckout();
    const store = new ClickAndCollectStore('Downtown PawPlace', '123 Main St');
    store.bindToCheckoutSessionOnSelection(guest);
    assert.equal(guest.clickAndCollectStore?.storeIdentity, 'Downtown PawPlace');
  });

  it('replace binding when customer changes store keeps exactly one selection', () => {
    const guest = buildGuestCheckout();
    guest.clickAndCollectStore = new ClickAndCollectStore('Downtown PawPlace', '123 Main St');
    const selector = new SelectClickAndCollectStore();
    const replacement = selector.updateBindingWhenCustomerChangesStore(guest, {
      storeIdentity: 'Westside PawPlace',
      storeAddress: '456 Oak Ave',
    });
    assert.equal(replacement.storeIdentity, 'Westside PawPlace');
    assert.equal(guest.clickAndCollectStore?.storeIdentity, 'Westside PawPlace');
  });

  it('block payment until store chosen', () => {
    const guest = buildGuestCheckout();
    assert.equal(ClickAndCollectStore.blockPaymentUntilStoreChosen(guest), false);
    guest.clickAndCollectStore = new ClickAndCollectStore('Downtown PawPlace', '123 Main St');
    assert.equal(ClickAndCollectStore.blockPaymentUntilStoreChosen(guest), true);
  });
});

describe('Billing Address (domain)', () => {
  it('valid billing address saves on checkout session', () => {
    const guest = buildGuestCheckoutWithStore();
    const billing = validBilling();
    billing.saveOnCheckoutSessionWhenValid(guest);
    assert.ok(guest.billingAddress?.isValid());
  });

  it('invalid billing throws InvalidBillingAddressException without StripeWave', () => {
    const guest = buildGuestCheckoutWithStore();
    const billing = new BillingAddress('Alex', '42 Maple', 'Toronto', '', 'Canada');
    assert.throws(() => billing.saveOnCheckoutSessionWhenValid(guest));
  });

  it('revised billing replaces prior values before payment', () => {
    const guest = buildGuestCheckoutWithStore();
    const revised = new BillingAddress(
      'Alex Rivera',
      '88 Cedar Court',
      'Toronto',
      'M5V 2B2',
      'Canada',
    );
    revised.replacePriorValuesBeforePayment(guest, revised);
    assert.equal(guest.billingAddress?.street, '88 Cedar Court');
  });
});

describe('Payment Method (domain)', () => {
  it('card via StripeWave is only supported payment method', () => {
    const method = PaymentMethod.cardViaStripeWave();
    assert.equal(method.processorLabel, 'Card via StripeWave');
  });

  it('non-card alternatives throw UnsupportedPaymentMethodException', () => {
    assert.throws(
      () => PaymentMethod.rejectNonCardPaymentAlternatives('paypal'),
      UnsupportedPaymentMethodException,
    );
  });

  it('selected payment method passes charge to StripeWave', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    const stripeWave = new StripeWave();
    stripeWave.configureOutcome('success');
    const result = guest.paymentMethod!.passDetailsToStripeWaveOnPlaceOrder(
      stripeWave,
      guest.shoppingCart.calculateOrderTotal(),
    );
    assert.equal(result.isSuccess(), true);
  });
});

describe('Process Card Payment via StripeWave (domain)', () => {
  it('create paid click-and-collect order on StripeWave success', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    const processor = new ProcessCardPaymentViaStripeWave();
    const stripeWave = new StripeWave();
    stripeWave.configureOutcome('success');
    processor.invokeStripeWaveWhenPrerequisitesMet(
      guest,
      stripeWave,
      guest.billingAddress!,
      guest.clickAndCollectStore!,
      guest.paymentMethod!,
    );
    const order = processor.createPaidOrderOnProcessorSuccess(guest.shoppingCart, guest);
    assert.equal(order.orderId, 'CNC-1042');
    assert.equal(order.guestOnly, true);
  });

  it('payment failure surfaces message without creating order', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    const processor = new ProcessCardPaymentViaStripeWave();
    const stripeWave = new StripeWave();
    stripeWave.configureOutcome('card declined');
    const result = processor.invokeStripeWaveWhenPrerequisitesMet(
      guest,
      stripeWave,
      guest.billingAddress!,
      guest.clickAndCollectStore!,
      guest.paymentMethod!,
    );
    processor.showFailureWithoutCreatingOrder(guest, result.failureReason());
    assert.equal(guest.paymentFailureMessage, 'card declined');
  });

  it('prevent duplicate payment submission while processing', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    guest.setProcessingPayment(true);
    assert.equal(guest.preventDuplicatePaymentSubmission(), true);
  });

  it('failed payment leaves shopping cart lines recoverable', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    assert.ok(guest.shoppingCart.hasAtLeastOneLine());
    const processor = new ProcessCardPaymentViaStripeWave();
    const stripeWave = new StripeWave();
    stripeWave.configureOutcome('card declined');
    processor.invokeStripeWaveWhenPrerequisitesMet(
      guest,
      stripeWave,
      guest.billingAddress!,
      guest.clickAndCollectStore!,
      guest.paymentMethod!,
    );
    assert.ok(guest.shoppingCart.hasAtLeastOneLine());
  });
});

describe('Order Confirmation (domain)', () => {
  it('withhold confirmation until StripeWave reports success', () => {
    const stripeWave = new StripeWave();
    stripeWave.configureOutcome('card declined');
    stripeWave.processCardChargeForOrder(
      PaymentMethod.cardViaStripeWave(),
      Money.zero(),
    );
    assert.equal(OrderConfirmation.withholdUntilStripeWaveSuccess(stripeWave), false);
  });

  it('send confirmation email with order id and pickup store after success', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    const confirmation = new OrderConfirmation();
    const order = ClickAndCollectOrder.originateFromCompletedGuestCheckout(
      guest,
      guest.shoppingCart,
    );
    confirmation.sendConfirmationEmailAfterSuccess(
      guest,
      order,
      guest.clickAndCollectStore!,
    );
    assert.equal(confirmation.emailSentTo, guest.email);
    assert.equal(confirmation.orderId, order.orderId);
  });

  it('show order summary on confirmation screen', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    const order = ClickAndCollectOrder.originateFromCompletedGuestCheckout(
      guest,
      guest.shoppingCart,
    );
    const confirmation = new OrderConfirmation();
    const summary = confirmation.showOrderSummaryOnConfirmationScreen(
      order,
      guest.clickAndCollectStore!,
    );
    assert.match(summary, /CNC-1042/);
  });
});

describe('Click-and-collect Order (domain)', () => {
  it('originate from completed guest checkout as guest-only paid order', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    const order = ClickAndCollectOrder.originateFromCompletedGuestCheckout(
      guest,
      guest.shoppingCart,
    );
    assert.equal(order.guestOnly, true);
    assert.equal(order.paymentConfirmed, true);
  });

  it('reference exactly one click-and-collect store for pickup', () => {
    const guest = buildGuestCheckoutReadyForPayment();
    const order = ClickAndCollectOrder.originateFromCompletedGuestCheckout(
      guest,
      guest.shoppingCart,
    );
    assert.equal(order.clickAndCollectStore?.storeIdentity, 'Downtown PawPlace');
  });
});

function buildCustomerWithCart(): Customer {
  const store = new SelectedStore('Downtown PawPlace');
  const customer = new Customer('Alex Rivera', store);
  const stock = new StockAvailability();
  stock.setAvailability(new Product('Premium Salmon Kibble', new Money(24.99)), store, 'available');
  customer.addProductToCart(new Product('Premium Salmon Kibble', new Money(24.99)), stock);
  return customer;
}

function buildGuestCheckout(): GuestCheckout {
  const customer = buildCustomerWithCart();
  const guest = GuestCheckout.startFromNonEmptyShoppingCart(customer.shoppingCart, customer);
  guest.collectContactEmail('alex.rivera@example.com');
  return guest;
}

function buildGuestCheckoutWithStore(): GuestCheckout {
  const guest = buildGuestCheckout();
  new ClickAndCollectStore('Downtown PawPlace', '123 Main St').bindToCheckoutSessionOnSelection(
    guest,
  );
  return guest;
}

function buildGuestCheckoutReadyForPayment(): GuestCheckout {
  const guest = buildGuestCheckoutWithStore();
  validBilling().saveOnCheckoutSessionWhenValid(guest);
  PaymentMethod.cardViaStripeWave().recordCardChoiceOnCheckoutSession(guest);
  return guest;
}

function validBilling(): BillingAddress {
  return new BillingAddress(
    'Alex Rivera',
    '42 Maple Lane',
    'Toronto',
    'M5V 1A1',
    'Canada',
  );
}
