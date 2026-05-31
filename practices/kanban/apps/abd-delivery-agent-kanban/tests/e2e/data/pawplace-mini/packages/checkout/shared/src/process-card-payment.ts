import { CheckoutPrerequisitesIncompleteException, DuplicatePaymentSubmissionException } from './checkout-exceptions';
import type { GuestCheckout } from './guest-checkout';
import type { StripeWave } from './stripe-wave';
import type { BillingAddress } from './billing-address';
import type { PickupStore } from './pickup-store';
import type { PaymentMethod } from './payment-method';
import { ClickAndCollectOrder } from './click-and-collect-order';
import type { StripeWaveResult } from './stripe-wave-result';

/** << Service >> — process card payment via StripeWave. */
export class ProcessCardPaymentViaStripeWave {
  invokeStripeWaveWhenPrerequisitesMet(
    guestCheckout: GuestCheckout,
    stripeWave: StripeWave,
    _billingAddress: BillingAddress,
    _clickAndCollectStore: PickupStore,
    paymentMethod: PaymentMethod,
  ): StripeWaveResult {
    if (!guestCheckout.blockPaymentUntilPrerequisitesMet()) {
      return StripeWaveResult.fromProcessorResponse('checkout prerequisites incomplete');
    }
    if (guestCheckout.preventDuplicatePaymentSubmission()) {
      throw new DuplicatePaymentSubmissionException();
    }
    guestCheckout.setProcessingPayment(true);
    const orderTotal = guestCheckout.shoppingCart.calculateOrderTotal();
    const result = paymentMethod.passDetailsToStripeWaveOnPlaceOrder(stripeWave, orderTotal);
    stripeWave.returnSuccessOrFailureToGuestCheckout(guestCheckout, result);
    return result;
  }

  createPaidOrderOnProcessorSuccess(
    shoppingCart: GuestCheckout['shoppingCart'],
    guestCheckout: GuestCheckout,
  ): ClickAndCollectOrder {
    const placedOrder = ClickAndCollectOrder.originateFromCompletedGuestCheckout(
      guestCheckout,
      shoppingCart,
    );
    guestCheckout.clickAndCollectStore?.attachToPlacedOrderOnSuccess(placedOrder);
    guestCheckout.billingAddress?.attachToClickAndCollectOrderOnPay(placedOrder);
    guestCheckout.paymentMethod?.attachToClickAndCollectOrderOnPay(placedOrder);
    return placedOrder;
  }

  clearShoppingCartAfterSuccessfulPay(shoppingCart: GuestCheckout['shoppingCart']): void {
    shoppingCart.clearAllLinesAfterPayment();
  }

  showFailureWithoutCreatingOrder(guestCheckout: GuestCheckout, failureReason: string): void {
    guestCheckout.showPaymentFailureWithoutOrder(failureReason);
    guestCheckout.setProcessingPayment(false);
  }

  static preventDuplicatePaymentSubmission(guestCheckout: GuestCheckout): boolean {
    return guestCheckout.preventDuplicatePaymentSubmission();
  }
}
