/**
 * Checkout & pay — client acceptance tests (Increment 2 Sprint 2).
 */
import { describe, it, beforeEach, afterEach, expect } from 'vitest';
import { screen } from '@testing-library/react';
import { CheckoutClientHelper } from './helpers/checkout.client';
import { CheckoutBaseHelper } from './helpers/checkout.base';

describe('Select Click-and-Collect Store — client', () => {
  const helper = new CheckoutClientHelper();

  beforeEach(async () => {
    await helper.givenGuestCheckoutFromNonEmptyCart();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Select Click-and-Collect Store — AC 1: all stores selectable', async () => {
    await helper.whenCustomerOpensGuestCheckout();
    helper.thenUiShowsAllEligibleStores();
  });

  it('Select Click-and-Collect Store — AC 2: bind shows identity address', async () => {
    await helper.whenCustomerSelectsClickAndCollectStore(CheckoutBaseHelper.STORE_DOWNTOWN);
    helper.thenUiShowsBoundStore(CheckoutBaseHelper.STORE_DOWNTOWN);
  });

  it('Select Click-and-Collect Store — AC 3: payment blocked without store', async () => {
    await helper.givenNoClickAndCollectStoreSelected();
    await helper.whenCustomerOpensGuestCheckout();
    helper.thenUiBlocksPlaceOrder();
  });
});

describe('Check Out as Guest — client', () => {
  const helper = new CheckoutClientHelper();

  beforeEach(async () => {
    await helper.givenGuestCheckoutFromNonEmptyCart();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Check Out as Guest — AC 1: guest checkout no sign-in', async () => {
    await helper.whenCustomerOpensGuestCheckout();
    helper.thenUiShowsGuestOnlyLabel();
  });
});

describe('Enter Billing Address — client', () => {
  const helper = new CheckoutClientHelper();

  beforeEach(async () => {
    await helper.givenGuestCheckoutFromNonEmptyCart();
    await helper.givenClickAndCollectStoreSelected(CheckoutBaseHelper.STORE_DOWNTOWN);
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Enter Billing Address — AC 3: incomplete rejects no stripewave', async () => {
    await helper.whenCustomerOpensGuestCheckout();
    await helper.whenCustomerEntersBillingAddress({
      ...CheckoutBaseHelper.BILLING_VALID,
      postalCode: '',
    });
    helper.thenUiBlocksPlaceOrder();
    helper.thenUiShowsBillingFieldErrors();
  });
});

describe('Select Payment Method — client', () => {
  const helper = new CheckoutClientHelper();

  beforeEach(async () => {
    await helper.givenGuestCheckoutFromNonEmptyCart();
    await helper.givenValidBillingAndPaymentSelected(CheckoutBaseHelper.STORE_DOWNTOWN);
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Select Payment Method — AC 2: card enables place order', async () => {
    await helper.whenCustomerOpensGuestCheckout();
    helper.thenUiShowsPaymentMethodSelected();
    expect(screen.getByRole('button', { name: 'place order' })).not.toBeDisabled();
  });
});

describe('Process Card Payment via StripeWave — client', () => {
  const helper = new CheckoutClientHelper();

  beforeEach(async () => {
    await helper.givenGuestCheckoutFromNonEmptyCart();
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Process Card Payment via StripeWave — AC 3: failure no order', async () => {
    await helper.givenValidBillingAndPaymentSelected(CheckoutBaseHelper.STORE_DOWNTOWN);
    await helper.givenStripeWaveWillDecline();
    await helper.whenCustomerClicksPlaceOrder();
    helper.thenUiShowsPaymentFailure();
  });
});

describe('Confirm Order and Send Confirmation Email — client', () => {
  const helper = new CheckoutClientHelper();

  beforeEach(async () => {
    await helper.givenGuestCheckoutFromNonEmptyCart();
    await helper.givenValidBillingAndPaymentSelected(CheckoutBaseHelper.STORE_DOWNTOWN);
  });
  afterEach(async () => {
    await helper.cleanup();
  });

  it('Confirm Order and Send Confirmation Email — AC 2: summary on screen', async () => {
    await helper.whenCustomerClicksPlaceOrder();
    await helper.whenCustomerViewsOrderConfirmation();
    helper.thenUiShowsOrderConfirmation(
      'CNC-1042',
      CheckoutBaseHelper.STORE_DOWNTOWN,
      '$43.49',
    );
  });
});
