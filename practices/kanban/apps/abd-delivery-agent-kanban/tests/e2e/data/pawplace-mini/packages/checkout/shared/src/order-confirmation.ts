import { PaymentNotConfirmedException } from './checkout-exceptions';
import type { GuestCheckout } from './guest-checkout';
import type { ClickAndCollectOrder } from './click-and-collect-order';
import type { PickupStore } from './pickup-store';
import type { StripeWave } from './stripe-wave';

/** << Entity >> — order confirmation after successful payment. */
export class OrderConfirmation {
  orderId = '';
  emailSentTo = '';
  confirmationComplete = false;
  confirmationScreenSummary = '';

  acknowledgePlacedClickAndCollectOrder(
    guestCheckout: GuestCheckout,
    stripeWave: StripeWave,
  ): OrderConfirmation {
    if (!stripeWave.reportedSuccess()) {
      throw new PaymentNotConfirmedException();
    }
    this.confirmationComplete = true;
    return this;
  }

  sendConfirmationEmailAfterSuccess(
    guestCheckout: GuestCheckout,
    clickAndCollectOrder: ClickAndCollectOrder,
    _clickAndCollectStore: PickupStore,
  ): void {
    this.emailSentTo = guestCheckout.email;
    this.orderId = clickAndCollectOrder.orderId;
  }

  showOrderSummaryOnConfirmationScreen(
    clickAndCollectOrder: ClickAndCollectOrder,
    clickAndCollectStore: PickupStore,
  ): string {
    this.confirmationScreenSummary = `${clickAndCollectOrder.orderId} — ${clickAndCollectStore.storeIdentity} — ${clickAndCollectOrder.orderTotal.amount}`;
    return this.confirmationScreenSummary;
  }

  isComplete(): boolean {
    return this.confirmationComplete;
  }

  static withholdUntilStripeWaveSuccess(stripeWave: StripeWave): boolean {
    return stripeWave.reportedSuccess();
  }
}
