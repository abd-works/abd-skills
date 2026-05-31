import type { Money } from '@pawplace-mini/cart-shared';
import type { PaymentMethod } from './payment-method';
import { StripeWaveResult } from './stripe-wave-result';
import type { GuestCheckout } from './guest-checkout';
import type { OrderConfirmation } from './order-confirmation';

/** << Service >> — external StripeWave payment port. */
export class StripeWave {
  lastResult: StripeWaveResult | null = null;
  private configuredOutcome: string = 'success';

  configureOutcome(outcome: string): void {
    this.configuredOutcome = outcome;
  }

  processCardChargeForOrder(
    _paymentMethod: PaymentMethod,
    _orderTotal: Money,
  ): StripeWaveResult {
    this.lastResult = StripeWaveResult.fromProcessorResponse(this.configuredOutcome);
    return this.lastResult;
  }

  returnSuccessOrFailureToGuestCheckout(
    guestCheckout: GuestCheckout,
    result: StripeWaveResult,
  ): StripeWaveResult {
    if (result.isFailure()) {
      guestCheckout.showPaymentFailureWithoutOrder(result.failureReason());
    }
    return result;
  }

  withholdOrderConfirmationOnFailure(result: StripeWaveResult): boolean {
    return result.isSuccess();
  }

  reportedSuccess(): boolean {
    return this.lastResult?.isSuccess() ?? false;
  }

  static withholdConfirmationUntilSuccess(
    orderConfirmation: OrderConfirmation,
    guestCheckout: GuestCheckout,
    stripeWave: StripeWave,
  ): OrderConfirmation {
    if (!stripeWave.reportedSuccess()) {
      throw new Error('payment not confirmed');
    }
    return orderConfirmation.acknowledgePlacedClickAndCollectOrder(guestCheckout, stripeWave);
  }
}
