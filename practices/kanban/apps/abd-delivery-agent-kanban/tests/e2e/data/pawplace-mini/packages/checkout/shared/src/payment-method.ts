import { UnsupportedPaymentMethodException } from './checkout-exceptions';
import type { GuestCheckout } from './guest-checkout';
import type { ClickAndCollectOrder } from './click-and-collect-order';
import type { Money } from '@pawplace-mini/cart-shared';
import type { StripeWave } from './stripe-wave';
import type { StripeWaveResult } from './stripe-wave-result';

/** << ValueObject >> — card via StripeWave payment method. */
export class PaymentMethod {
  readonly processorLabel: string;
  cardSelected = false;

  private constructor(processorLabel: string) {
    this.processorLabel = processorLabel;
  }

  static cardViaStripeWave(): PaymentMethod {
    return new PaymentMethod('Card via StripeWave');
  }

  recordCardChoiceOnCheckoutSession(guestCheckout: GuestCheckout): void {
    this.cardSelected = true;
    guestCheckout.paymentMethod = this;
  }

  static blockStripeWaveUntilMethodSelected(guestCheckout: GuestCheckout): boolean {
    return guestCheckout.paymentMethod != null && guestCheckout.paymentMethod.isSelected();
  }

  passDetailsToStripeWaveOnPlaceOrder(
    stripeWave: StripeWave,
    orderTotal: Money,
  ): StripeWaveResult {
    return stripeWave.processCardChargeForOrder(this, orderTotal);
  }

  attachToClickAndCollectOrderOnPay(order: ClickAndCollectOrder): void {
    order.paymentMethod = this;
  }

  isSelected(): boolean {
    return this.cardSelected;
  }

  static rejectNonCardPaymentAlternatives(method: string): void {
    if (method !== 'card') {
      throw new UnsupportedPaymentMethodException();
    }
  }
}
