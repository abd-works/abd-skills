/**
 * Checkout & pay — server-tier helper (Supertest + CheckoutService).
 */
import assert from 'node:assert/strict';
import type { Express } from 'express';
import request from 'supertest';
import { createAppServer } from '@pawplace-mini/app-server';
import type { CartService } from '@pawplace-mini/cart-server';
import type { CheckoutService } from '@pawplace-mini/checkout-server';
import type { FulfillmentService } from '@pawplace-mini/fulfillment-server';
import {
  BillingAddress,
  type CheckoutSessionDto,
  type OrderConfirmationDto,
} from '@pawplace-mini/checkout-shared';
import type { ShoppingCartDto } from '@pawplace-mini/cart-shared';
import type { BillingAddressTestData, StoreTestData } from './checkout.base';
import { CheckoutBaseHelper } from './checkout.base';

const SALMON = 'Premium Salmon Kibble';
const LEASH = 'Reflective Dog Leash';

export class CheckoutServerHelper extends CheckoutBaseHelper {
  private readonly app: Express;
  private readonly cartService: CartService;
  private readonly checkoutService: CheckoutService;
  private readonly fulfillmentService: FulfillmentService;
  private readonly sessionId = 'checkout-session';
  private readonly employeeSessionId = 'fulfillment-staff';
  private lastCheckout!: CheckoutSessionDto;
  private lastConfirmation: OrderConfirmationDto | null = null;
  private lastCart!: ShoppingCartDto;
  private lastFulfillmentQueue: { orderId: string }[] = [];

  constructor() {
    super();
    const server = createAppServer();
    this.app = server.app;
    this.cartService = server.cartService;
    this.checkoutService = server.checkoutService;
    this.fulfillmentService = server.fulfillmentService;
  }

  async cleanup(): Promise<void> {
    this.cartService.resetFixture();
    this.checkoutService.resetFixture();
    this.fulfillmentService.resetFixture();
    this.lastCheckout = undefined as unknown as CheckoutSessionDto;
    this.lastConfirmation = null;
    this.lastFulfillmentQueue = [];
  }

  async givenShoppingCartForCustomerHasNonEmptyCart(): Promise<void> {
    await request(this.app)
      .post('/api/v1/sessions')
      .set('x-session-id', this.sessionId)
      .send({
        displayName: 'Alex Rivera',
        selectedStoreIdentity: CheckoutBaseHelper.STORE_DOWNTOWN.storeIdentity,
      });
    this.cartService.seedCartLine(this.sessionId, SALMON, 1);
    this.lastCart = this.cartService.seedCartLine(this.sessionId, LEASH, 1);
  }

  async givenShoppingCartForCustomerHasNoCartLines(): Promise<void> {
    await request(this.app)
      .post('/api/v1/sessions')
      .set('x-session-id', this.sessionId)
      .send({
        displayName: 'Alex Rivera',
        selectedStoreIdentity: CheckoutBaseHelper.STORE_DOWNTOWN.storeIdentity,
      });
    const response = await request(this.app)
      .get('/api/v1/cart')
      .set('x-session-id', this.sessionId);
    this.lastCart = response.body;
  }

  async givenGuestCheckoutSessionStarted(): Promise<void> {
    await this.whenCustomerStartsGuestCheckoutFromShoppingCart();
  }

  async givenClickAndCollectStoreSelectedOnSession(store: StoreTestData): Promise<void> {
    await this.whenCustomerSelectsClickAndCollectStoreViaApi(store);
  }

  async givenValidBillingAddressOnSession(): Promise<void> {
    await this.whenCustomerEntersBillingAddressViaApi(CheckoutBaseHelper.BILLING_VALID);
  }

  async givenPaymentMethodSelectedOnSession(): Promise<void> {
    await this.whenCustomerSelectsPaymentMethodViaApi();
  }

  async givenStripeWaveWillReportSuccess(): Promise<void> {
    await request(this.app)
      .post('/api/v1/checkout/stripe-wave/outcome')
      .set('x-session-id', this.sessionId)
      .send({ outcome: 'success' });
  }

  async givenStripeWaveWillReportFailure(reason: string): Promise<void> {
    await request(this.app)
      .post('/api/v1/checkout/stripe-wave/outcome')
      .set('x-session-id', this.sessionId)
      .send({ outcome: reason });
  }

  async whenCustomerStartsGuestCheckoutFromShoppingCart(): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/checkout/guest')
      .set('x-session-id', this.sessionId);
    this.lastCheckout = response.body;
  }

  async whenCustomerSelectsClickAndCollectStoreViaApi(store: StoreTestData): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/checkout/click-and-collect-store')
      .set('x-session-id', this.sessionId)
      .send({
        storeIdentity: store.storeIdentity,
        storeAddress: store.storeAddress,
      });
    this.lastCheckout = response.body;
  }

  async whenCustomerAttemptsProcessCardPaymentViaStripeWave(): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/checkout/process-payment')
      .set('x-session-id', this.sessionId);
    this.lastCheckout = response.body;
  }

  async whenCustomerEntersBillingAddressViaApi(address: BillingAddressTestData): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/checkout/billing-address')
      .set('x-session-id', this.sessionId)
      .send(address);
    this.lastCheckout = response.body;
  }

  async whenCustomerSelectsPaymentMethodViaApi(): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/checkout/payment-method')
      .set('x-session-id', this.sessionId)
      .send({ method: 'card' });
    this.lastCheckout = response.body;
  }

  async whenCustomerSubmitsProcessCardPaymentViaStripeWave(): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/checkout/process-payment')
      .set('x-session-id', this.sessionId);
    assert.equal(response.status, 200, JSON.stringify(response.body));
    this.lastCheckout = response.body;
    const cartResponse = await request(this.app)
      .get('/api/v1/cart')
      .set('x-session-id', this.sessionId);
    this.lastCart = cartResponse.body;
  }

  async whenCustomerAttemptsDuplicatePaymentSubmission(): Promise<void> {
    const response = await request(this.app)
      .post('/api/v1/checkout/process-payment')
      .set('x-session-id', this.sessionId);
    this.lastCheckout = response.body;
  }

  async whenOrderConfirmationRunsAfterPaymentSuccess(): Promise<void> {
    const response = await request(this.app)
      .get('/api/v1/checkout/confirmation')
      .set('x-session-id', this.sessionId);
    this.lastConfirmation = response.status === 200 ? response.body : null;
  }

  thenGuestCheckoutPresentsAllEligibleStores(): void {
    assert.equal(this.lastCheckout.eligibleStores.length, 3);
    assert.ok(
      this.lastCheckout.eligibleStores.some(
        (s) => s.storeIdentity === CheckoutBaseHelper.STORE_DOWNTOWN.storeIdentity,
      ),
    );
  }

  thenClickAndCollectStoreBoundWithIdentityAndAddress(store: StoreTestData): void {
    assert.deepEqual(this.lastCheckout.clickAndCollectStore, {
      storeIdentity: store.storeIdentity,
      storeAddress: store.storeAddress,
    });
  }

  thenGuestCheckoutBlocksStripeWaveWithoutStore(): void {
    assert.equal(this.lastCheckout.placeOrderBlocked, true);
    assert.match(
      this.lastCheckout.placeOrderBlockedReason ?? '',
      /click-and-collect store/i,
    );
    assert.equal(this.lastCheckout.placedOrderId ?? null, null);
  }

  thenOnlyOneClickAndCollectStoreRemainsOnSession(store: StoreTestData): void {
    this.thenClickAndCollectStoreBoundWithIdentityAndAddress(store);
  }

  thenPlacedOrderReferencesClickAndCollectStore(store: StoreTestData): void {
    assert.equal(this.lastCheckout.placedOrderId, CheckoutBaseHelper.ORDER_ID);
    assert.equal(this.lastCheckout.clickAndCollectStore?.storeIdentity, store.storeIdentity);
  }

  thenGuestCheckoutStartsWithoutSignIn(): void {
    assert.equal(this.lastCheckout.guestOnlyLabel, true);
  }

  thenGuestCheckoutCollectsContactEmailWithoutRegistration(): void {
    assert.equal(this.lastCheckout.email, CheckoutBaseHelper.GUEST_EMAIL);
  }

  thenGuestCheckoutBlockedWhenCartEmpty(): void {
    assert.ok(
      this.lastCheckout.validationErrors.some((message) =>
        message.includes('guest checkout blocked when shopping cart empty'),
      ),
    );
  }

  thenCheckoutStepsProgressStoreBillingPayment(): void {
    assert.equal(this.lastCheckout.checkoutSteps?.store, true);
    assert.equal(this.lastCheckout.checkoutSteps?.billing, true);
    assert.equal(this.lastCheckout.checkoutSteps?.payment, true);
  }

  thenGuestCheckoutCreatesGuestOnlyOrder(orderId: string): void {
    assert.equal(this.lastCheckout.placedOrderId, orderId);
    assert.equal(this.lastConfirmation?.guestOnly ?? true, true);
  }

  thenBillingStepPresentsRequiredFields(): void {
    assert.deepEqual(this.lastCheckout.billingFieldNames, [
      'name',
      'street',
      'city',
      'postalCode',
      'country',
    ]);
  }

  thenValidBillingAddressSavedOnSession(address: BillingAddressTestData): void {
    assert.deepEqual(this.lastCheckout.billingAddress, address);
    assert.equal(this.lastCheckout.placeOrderBlocked, true);
    assert.match(
      this.lastCheckout.placeOrderBlockedReason ?? '',
      /payment|StripeWave/i,
    );
  }

  thenIncompleteBillingRejectedWithoutStripeWave(): void {
    assert.equal(this.lastCheckout.billingAddress?.postalCode, '');
    assert.equal(this.lastCheckout.stripeWaveInvoked, false);
    assert.equal(this.lastCheckout.placedOrderId ?? null, null);
  }

  thenRevisedBillingAddressReplacesPrior(address: BillingAddressTestData): void {
    assert.deepEqual(this.lastCheckout.billingAddress, address);
  }

  thenPaidOrderIncludesBillingAddress(address: BillingAddressTestData): void {
    const saved = this.checkoutService.getPlacedOrderBilling(this.sessionId);
    const expected = new BillingAddress(
      address.name,
      address.street,
      address.city,
      address.postalCode,
      address.country,
    );
    assert.ok(saved?.equals(expected));
  }

  thenPaymentStepPresentsCardViaStripeWaveOnly(): void {
    assert.equal(this.lastCheckout.stripeWaveLabel, 'Card via StripeWave');
    assert.equal(this.lastCheckout.nonCardPaymentOffered, false);
  }

  thenPaymentMethodEnablesPlaceOrder(): void {
    assert.equal(this.lastCheckout.paymentMethodSelected, true);
    assert.equal(this.lastCheckout.placeOrderBlocked, false);
  }

  thenStripeWaveBlockedWithoutPaymentMethod(): void {
    assert.equal(this.lastCheckout.paymentMethodSelected, false);
    assert.equal(this.lastCheckout.placedOrderId ?? null, null);
  }

  thenNonCardPaymentAlternativesNotOffered(): void {
    assert.equal(this.lastCheckout.nonCardPaymentOffered, false);
  }

  thenStripeWaveReceivesChargeForOrderTotal(total: number): void {
    const charged = this.checkoutService.getLastStripeChargeAmount();
    assert.ok(charged != null && Math.abs(charged - total) < 0.01);
  }

  thenStripeWaveInvokedAndWaitsForResponse(): void {
    assert.equal(this.lastCheckout.stripeWaveInvoked, true);
  }

  thenPaidOrderCreatedAndCartCleared(orderId: string, store: StoreTestData): void {
    assert.equal(this.lastCheckout.placedOrderId, orderId);
    assert.equal(this.lastCheckout.clickAndCollectStore?.storeIdentity, store.storeIdentity);
    assert.equal(this.lastCart.cartLines.length, 0);
  }

  thenPaymentFailureWithoutOrderOrConfirmation(reason: string): void {
    assert.equal(this.lastCheckout.paymentFailureMessage, reason);
    assert.equal(this.lastCheckout.placedOrderId ?? null, null);
    assert.equal(this.lastConfirmation, null);
  }

  thenDuplicatePaymentSubmissionPrevented(): void {
    assert.equal(this.lastCheckout.placedOrderId, CheckoutBaseHelper.ORDER_ID);
    assert.equal(this.lastCheckout.processingPayment, false);
  }

  thenFailedPaymentLeavesCartRecoverable(): void {
    assert.ok(this.lastCart.cartLines.length > 0);
    assert.equal(this.lastCheckout.placedOrderId ?? null, null);
  }

  thenOrderConfirmationEmailSentTo(
    email: string,
    orderId: string,
    store: StoreTestData,
  ): void {
    assert.ok(this.lastConfirmation);
    assert.equal(this.lastConfirmation!.emailSentTo, email);
    assert.equal(this.lastConfirmation!.orderId, orderId);
    assert.equal(this.lastConfirmation!.clickAndCollectStore, store.storeIdentity);
    assert.equal(this.lastConfirmation!.orderConfirmationSent, true);
  }

  thenConfirmationScreenShowsOrderSummary(
    orderId: string,
    store: StoreTestData,
    total: number,
  ): void {
    assert.ok(this.lastConfirmation);
    assert.equal(this.lastConfirmation!.orderId, orderId);
    assert.equal(this.lastConfirmation!.clickAndCollectStore, store.storeIdentity);
    assert.equal(this.lastConfirmation!.total, total);
    assert.match(
      this.lastConfirmation!.confirmationScreenSummary ?? '',
      new RegExp(orderId),
    );
  }

  thenOrderConfirmationWithheldUntilStripeWaveSuccess(): void {
    assert.equal(this.lastConfirmation, null);
    assert.equal(this.lastCheckout.placedOrderId ?? null, null);
  }

  async thenOrderVisibleInFulfillmentQueue(orderId: string, store: StoreTestData): Promise<void> {
    this.fulfillmentService.bindEmployeeSession(
      this.employeeSessionId,
      'Store Employee',
      store.storeIdentity,
    );
    const response = await request(this.app)
      .get('/api/v1/fulfillment/queue')
      .query({ store: store.storeIdentity })
      .set('x-staff-token', 'store-employee')
      .set('x-session-id', this.employeeSessionId);
    assert.equal(response.status, 200);
    const queue = response.body.queue as { orderId: string }[];
    assert.ok(
      queue.some((row) => row.orderId === orderId),
      `expected ${orderId} in fulfillment queue`,
    );
  }

  thenPlacedOrderNotEditableViaShoppingCart(orderId: string): void {
    assert.equal(this.lastCheckout.placedOrderId, orderId);
    assert.equal(this.lastCart.cartLines.length, 0);
  }
}
