import type { CartRepository } from '@pawplace-mini/cart-server';
import {
  BillingAddress,
  DuplicatePaymentSubmissionException,
  EmptyCartCheckoutBlockedException,
  GuestCheckout,
  InvalidBillingAddressException,
  OrderConfirmation,
  PaymentMethod,
  PickupStore,
  ProcessCardPaymentViaStripeWave,
  SelectClickAndCollectStore,
  StripeWave,
  UnsupportedPaymentMethodException,
} from '@pawplace-mini/checkout-shared';
import type { CheckoutSessionDto, OrderConfirmationDto } from '@pawplace-mini/checkout-shared';
import type { FulfillmentRepository } from '../../fulfillment/server/fulfillment.repository';
import { CheckoutRepository, type CheckoutSessionRecord } from './checkout.repository';
import { toCheckoutSessionDto, toOrderConfirmationDto } from './checkout.mapper';

export class CheckoutService {
  private readonly processPayment = new ProcessCardPaymentViaStripeWave();

  constructor(
    private readonly checkoutRepository: CheckoutRepository,
    private readonly cartRepository: CartRepository,
    private readonly fulfillmentRepository?: FulfillmentRepository,
  ) {}

  resetFixture(): void {
    this.checkoutRepository.reset();
  }

  startGuestCheckout(sessionId: string): CheckoutSessionDto {
    const cartRecord = this.requireCartSession(sessionId);
    if (cartRecord.customer.shoppingCart.isEmpty()) {
      try {
        GuestCheckout.startFromNonEmptyShoppingCart(
          cartRecord.customer.shoppingCart,
          cartRecord.customer,
        );
      } catch (error) {
        if (error instanceof EmptyCartCheckoutBlockedException) {
          return this.emptyCartBlockedDto();
        }
        throw error;
      }
    }
    const guestCheckout = GuestCheckout.startFromNonEmptyShoppingCart(
      cartRecord.customer.shoppingCart,
      cartRecord.customer,
    );
    const record = {
      guestCheckout,
      stripeWave: new StripeWave(),
      placedOrder: null,
      orderConfirmation: null,
    };
    this.checkoutRepository.saveSession(sessionId, record);
    return toCheckoutSessionDto(record);
  }

  getCheckoutSession(sessionId: string): CheckoutSessionDto {
    const record = this.requireCheckoutSession(sessionId);
    return toCheckoutSessionDto(record);
  }

  selectClickAndCollectStore(
    sessionId: string,
    storeIdentity: string,
    storeAddress: string,
  ): CheckoutSessionDto {
    const record = this.requireCheckoutSession(sessionId);
    const store = new PickupStore(storeIdentity, storeAddress);
    store.bindToCheckoutSessionOnSelection(record.guestCheckout);
    return toCheckoutSessionDto(record);
  }

  enterBillingAddress(
    sessionId: string,
    fields: {
      name: string;
      street: string;
      city: string;
      postalCode: string;
      country: string;
    },
  ): CheckoutSessionDto {
    const record = this.requireCheckoutSession(sessionId);
    const billingAddress = new BillingAddress(
      fields.name,
      fields.street,
      fields.city,
      fields.postalCode,
      fields.country,
    );
    if (!billingAddress.isValid()) {
      record.guestCheckout.billingAddress = billingAddress;
      return toCheckoutSessionDto(record);
    }
    billingAddress.saveOnCheckoutSessionWhenValid(record.guestCheckout);
    return toCheckoutSessionDto(record);
  }

  selectPaymentMethod(sessionId: string, method = 'card'): CheckoutSessionDto {
    const record = this.requireCheckoutSession(sessionId);
    if (method !== 'card') {
      try {
        PaymentMethod.rejectNonCardPaymentAlternatives(method);
      } catch (error) {
        if (error instanceof UnsupportedPaymentMethodException) {
          return toCheckoutSessionDto(record);
        }
        throw error;
      }
    }
    const paymentMethod = PaymentMethod.cardViaStripeWave();
    paymentMethod.recordCardChoiceOnCheckoutSession(record.guestCheckout);
    return toCheckoutSessionDto(record);
  }

  configureStripeWaveOutcome(sessionId: string, outcome: string): void {
    const record = this.requireCheckoutSession(sessionId);
    record.stripeWave.configureOutcome(outcome === 'success' ? 'success' : outcome);
  }

  processCardPayment(sessionId: string): CheckoutSessionDto {
    const record = this.requireCheckoutSession(sessionId);
    const guest = record.guestCheckout;

    if (record.placedOrder) {
      return toCheckoutSessionDto(record);
    }

    if (!guest.clickAndCollectStore) {
      return toCheckoutSessionDto(record);
    }
    if (!guest.billingAddress?.isValid()) {
      return toCheckoutSessionDto(record);
    }
    if (!guest.paymentMethod?.isSelected()) {
      return toCheckoutSessionDto(record);
    }

    try {
      const result = this.processPayment.invokeStripeWaveWhenPrerequisitesMet(
        guest,
        record.stripeWave,
        guest.billingAddress!,
        guest.clickAndCollectStore,
        guest.paymentMethod!,
      );
      const chargeAmount = guest.shoppingCart.calculateOrderTotal().amount;
      this.checkoutRepository.recordStripeCharge(Math.round(chargeAmount * 100) / 100);

      if (result.isSuccess()) {
        record.placedOrder = this.processPayment.createPaidOrderOnProcessorSuccess(
          guest.shoppingCart,
          guest,
        );
        this.processPayment.clearShoppingCartAfterSuccessfulPay(guest.shoppingCart);
        guest.setProcessingPayment(false);

        const confirmation = new OrderConfirmation();
        confirmation.acknowledgePlacedClickAndCollectOrder(guest, record.stripeWave);
        confirmation.sendConfirmationEmailAfterSuccess(
          guest,
          record.placedOrder,
          guest.clickAndCollectStore,
        );
        confirmation.showOrderSummaryOnConfirmationScreen(
          record.placedOrder,
          guest.clickAndCollectStore,
        );
        record.orderConfirmation = confirmation;

        try {
          this.registerOrderForFulfillment(record);
        } catch {
          // Fulfillment registration must not block checkout success.
        }
      } else {
        this.processPayment.showFailureWithoutCreatingOrder(guest, result.failureReason());
      }
    } catch (error) {
      if (error instanceof DuplicatePaymentSubmissionException) {
        guest.setProcessingPayment(false);
        return toCheckoutSessionDto(record);
      }
      throw error;
    }

    return toCheckoutSessionDto(record);
  }

  getOrderConfirmation(sessionId: string): OrderConfirmationDto | null {
    const record = this.requireCheckoutSession(sessionId);
    return toOrderConfirmationDto(record);
  }

  getLastStripeChargeAmount(): number | null {
    return this.checkoutRepository.getLastStripeChargeAmount();
  }

  getPlacedOrderBilling(sessionId: string): BillingAddress | null {
    const record = this.requireCheckoutSession(sessionId);
    return record.placedOrder?.billingAddress ?? null;
  }

  private requireCartSession(sessionId: string) {
    const record = this.cartRepository.findSession(sessionId);
    if (!record) {
      throw new Error(`cart session not found: ${sessionId}`);
    }
    return record;
  }

  private requireCheckoutSession(sessionId: string) {
    const record = this.checkoutRepository.findSession(sessionId);
    if (!record) {
      throw new Error(`checkout session not found: ${sessionId}`);
    }
    return record;
  }

  private registerOrderForFulfillment(record: CheckoutSessionRecord): void {
    if (!this.fulfillmentRepository || !record.placedOrder) return;
    const order = record.placedOrder;
    const store = order.clickAndCollectStore;
    if (!store) return;
    this.fulfillmentRepository.seedOrder({
      orderId: order.orderId,
      customerContact: order.customerContact,
      clickAndCollectStore: store.storeIdentity,
      orderFulfillment: 'awaiting preparation',
      paid: true,
      cartLines: order.cartLines.map((line) => ({
        catalogItemIdentity: line.product.catalogItemIdentity,
        cartQuantity: line.cartQuantity.value,
      })),
    });
  }

  private emptyCartBlockedDto(): CheckoutSessionDto {
    return {
      guestOnlyLabel: true,
      eligibleStores: [],
      clickAndCollectStore: null,
      email: '',
      billingAddress: null,
      paymentMethodSelected: false,
      stripeWaveLabel: 'Card via StripeWave',
      placeOrderBlocked: true,
      placeOrderBlockedReason: 'shopping cart is empty',
      validationErrors: ['guest checkout blocked when shopping cart empty'],
      processingPayment: false,
      orderTotal: 0,
      paymentFailureMessage: null,
    };
  }
}
