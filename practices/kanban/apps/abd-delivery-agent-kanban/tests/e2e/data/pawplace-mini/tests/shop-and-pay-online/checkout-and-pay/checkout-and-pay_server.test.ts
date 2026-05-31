/**
 * Checkout & pay — server acceptance tests (Increment 2 Sprint 2).
 *
 * Story path: Shop & Pay Online → Checkout & pay → [Story]
 * File: tests/shop-and-pay-online/checkout-and-pay/checkout-and-pay_server.test.ts
 *
 * Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
 */
import { describe, it, beforeEach, afterEach } from 'vitest';
import { CheckoutServerHelper } from './helpers/checkout.server';
import { CheckoutBaseHelper } from './helpers/checkout.base';

describe('Select Click-and-Collect Store', () => {
  const helper = new CheckoutServerHelper();

  beforeEach(async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: guest checkout presents every eligible store as click-and-collect store', async () => {
    await helper.whenCustomerStartsGuestCheckoutFromShoppingCart();
    helper.thenGuestCheckoutPresentsAllEligibleStores();
  });

  it('Scenario 2: store selection binds click-and-collect store with identity and address', async () => {
    const store = CheckoutBaseHelper.STORE_DOWNTOWN;
    await helper.whenCustomerStartsGuestCheckoutFromShoppingCart();
    await helper.whenCustomerSelectsClickAndCollectStoreViaApi(store);
    helper.thenClickAndCollectStoreBoundWithIdentityAndAddress(store);
  });

  it('Scenario 3: payment blocked until click-and-collect store is chosen', async () => {
    await helper.whenCustomerStartsGuestCheckoutFromShoppingCart();
    await helper.whenCustomerAttemptsProcessCardPaymentViaStripeWave();
    helper.thenGuestCheckoutBlocksStripeWaveWithoutStore();
  });

  it('Scenario 4: changing click-and-collect store replaces prior binding with one store', async () => {
    const store = CheckoutBaseHelper.STORE_WESTSIDE;
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.whenCustomerSelectsClickAndCollectStoreViaApi(store);
    helper.thenOnlyOneClickAndCollectStoreRemainsOnSession(store);
  });

  it('Scenario 5: chosen click-and-collect store attaches to placed order on payment success', async () => {
    const store = CheckoutBaseHelper.STORE_UPTOWN;
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(store);
    await helper.givenValidBillingAddressOnSession();
    await helper.givenPaymentMethodSelectedOnSession();
    await helper.givenStripeWaveWillReportSuccess();
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenPlacedOrderReferencesClickAndCollectStore(store);
  });
});

describe('Check Out as Guest', () => {
  const helper = new CheckoutServerHelper();

  beforeEach(async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: non-empty shopping cart starts guest checkout without sign-in', async () => {
    await helper.whenCustomerStartsGuestCheckoutFromShoppingCart();
    helper.thenGuestCheckoutStartsWithoutSignIn();
  });

  it('Scenario 2: guest checkout collects contact email without registration offer', async () => {
    await helper.whenCustomerStartsGuestCheckoutFromShoppingCart();
    helper.thenGuestCheckoutCollectsContactEmailWithoutRegistration();
  });

  it('Scenario 3: empty shopping cart blocks guest checkout entry', async () => {
    await helper.givenShoppingCartForCustomerHasNoCartLines();
    await helper.whenCustomerStartsGuestCheckoutFromShoppingCart();
    helper.thenGuestCheckoutBlockedWhenCartEmpty();
  });

  it('Scenario 4: guest checkout advances store then billing then payment in order', async () => {
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.whenCustomerEntersBillingAddressViaApi(CheckoutBaseHelper.BILLING_VALID);
    await helper.whenCustomerSelectsPaymentMethodViaApi();
    helper.thenCheckoutStepsProgressStoreBillingPayment();
  });

  it('Scenario 5: successful guest checkout creates click-and-collect order without customer account', async () => {
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.givenValidBillingAddressOnSession();
    await helper.givenPaymentMethodSelectedOnSession();
    await helper.givenStripeWaveWillReportSuccess();
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenGuestCheckoutCreatesGuestOnlyOrder(CheckoutBaseHelper.ORDER_ID);
  });
});

describe('Enter Billing Address', () => {
  const helper = new CheckoutServerHelper();

  beforeEach(async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: billing step presents name and postal fields before payment', async () => {
    helper.thenBillingStepPresentsRequiredFields();
  });

  it('Scenario 2: valid billing address saves on checkout session and unlocks payment step', async () => {
    const address = CheckoutBaseHelper.BILLING_VALID;
    await helper.whenCustomerEntersBillingAddressViaApi(address);
    helper.thenValidBillingAddressSavedOnSession(address);
  });

  it('Scenario 3: incomplete billing address is rejected without StripeWave invocation', async () => {
    await helper.whenCustomerEntersBillingAddressViaApi({
      ...CheckoutBaseHelper.BILLING_VALID,
      postalCode: '',
    });
    helper.thenIncompleteBillingRejectedWithoutStripeWave();
  });

  it('Scenario 4: revised billing address replaces prior values before payment', async () => {
    const revised = CheckoutBaseHelper.BILLING_REVISED;
    await helper.givenValidBillingAddressOnSession();
    await helper.whenCustomerEntersBillingAddressViaApi(revised);
    helper.thenRevisedBillingAddressReplacesPrior(revised);
  });

  it('Scenario 5: paid click-and-collect order includes captured billing address', async () => {
    const address = CheckoutBaseHelper.BILLING_REVISED;
    await helper.givenValidBillingAddressOnSession();
    await helper.whenCustomerEntersBillingAddressViaApi(address);
    await helper.givenPaymentMethodSelectedOnSession();
    await helper.givenStripeWaveWillReportSuccess();
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenPaidOrderIncludesBillingAddress(address);
  });
});

describe('Select Payment Method', () => {
  const helper = new CheckoutServerHelper();

  beforeEach(async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.givenValidBillingAddressOnSession();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: payment step presents card via StripeWave as only payment method', async () => {
    helper.thenPaymentStepPresentsCardViaStripeWaveOnly();
  });

  it('Scenario 2: card selection enables place order and records payment method on session', async () => {
    await helper.whenCustomerSelectsPaymentMethodViaApi();
    helper.thenPaymentMethodEnablesPlaceOrder();
  });

  it('Scenario 3: StripeWave blocked until payment method is selected', async () => {
    await helper.whenCustomerAttemptsProcessCardPaymentViaStripeWave();
    helper.thenStripeWaveBlockedWithoutPaymentMethod();
  });

  it('Scenario 4: non-card payment alternatives are not offered in this fixture', async () => {
    helper.thenNonCardPaymentAlternativesNotOffered();
  });

  it('Scenario 5: selected payment method passes card details to StripeWave on place order', async () => {
    await helper.givenPaymentMethodSelectedOnSession();
    await helper.givenStripeWaveWillReportSuccess();
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenStripeWaveReceivesChargeForOrderTotal(CheckoutBaseHelper.ORDER_TOTAL);
  });
});

describe('Process Card Payment via StripeWave', () => {
  const helper = new CheckoutServerHelper();

  beforeEach(async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.givenValidBillingAddressOnSession();
    await helper.givenPaymentMethodSelectedOnSession();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: valid prerequisites invoke StripeWave and wait for processor response', async () => {
    await helper.givenStripeWaveWillReportSuccess();
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenStripeWaveInvokedAndWaitsForResponse();
  });

  it('Scenario 2: StripeWave success creates paid order and clears shopping cart', async () => {
    await helper.givenStripeWaveWillReportSuccess();
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenPaidOrderCreatedAndCartCleared(
      CheckoutBaseHelper.ORDER_ID,
      CheckoutBaseHelper.STORE_DOWNTOWN,
    );
  });

  it('Scenario 3: StripeWave failure shows message without order or confirmation', async () => {
    await helper.givenStripeWaveWillReportFailure('card declined');
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenPaymentFailureWithoutOrderOrConfirmation('card declined');
  });

  it('Scenario 4: processing state prevents duplicate payment submission', async () => {
    await helper.givenStripeWaveWillReportSuccess();
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    await helper.whenCustomerAttemptsDuplicatePaymentSubmission();
    helper.thenDuplicatePaymentSubmissionPrevented();
  });

  it('Scenario 5: failed payment leaves shopping cart recoverable for retry', async () => {
    await helper.givenStripeWaveWillReportFailure('card declined');
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenFailedPaymentLeavesCartRecoverable();
  });
});

describe('Confirm Order and Send Confirmation Email', () => {
  const helper = new CheckoutServerHelper();

  beforeEach(async () => {
    await helper.givenShoppingCartForCustomerHasNonEmptyCart();
    await helper.givenGuestCheckoutSessionStarted();
    await helper.givenClickAndCollectStoreSelectedOnSession(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.givenValidBillingAddressOnSession();
    await helper.givenPaymentMethodSelectedOnSession();
    await helper.givenStripeWaveWillReportSuccess();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Scenario 1: payment success sends order confirmation email with pickup store', async () => {
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    await helper.whenOrderConfirmationRunsAfterPaymentSuccess();
    helper.thenOrderConfirmationEmailSentTo(
      CheckoutBaseHelper.GUEST_EMAIL,
      CheckoutBaseHelper.ORDER_ID,
      CheckoutBaseHelper.STORE_DOWNTOWN,
    );
  });

  it('Scenario 2: confirmation screen shows order summary with store and total', async () => {
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    await helper.whenOrderConfirmationRunsAfterPaymentSuccess();
    helper.thenConfirmationScreenShowsOrderSummary(
      CheckoutBaseHelper.ORDER_ID,
      CheckoutBaseHelper.STORE_DOWNTOWN,
      CheckoutBaseHelper.ORDER_TOTAL,
    );
  });

  it('Scenario 3: order confirmation withheld until StripeWave reports success', async () => {
    await helper.givenStripeWaveWillReportFailure('card declined');
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    helper.thenOrderConfirmationWithheldUntilStripeWaveSuccess();
  });

  it('Scenario 4: confirmed order exposes click-and-collect order to store fulfillment queue', async () => {
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    await helper.whenOrderConfirmationRunsAfterPaymentSuccess();
    await helper.thenOrderVisibleInFulfillmentQueue(
      CheckoutBaseHelper.ORDER_ID,
      CheckoutBaseHelper.STORE_DOWNTOWN,
    );
  });

  it('Scenario 5: customer continues shopping without editing placed order via cart', async () => {
    await helper.whenCustomerSubmitsProcessCardPaymentViaStripeWave();
    await helper.whenOrderConfirmationRunsAfterPaymentSuccess();
    helper.thenPlacedOrderNotEditableViaShoppingCart(CheckoutBaseHelper.ORDER_ID);
  });
});
