import type { Customer, ShoppingCart } from '@pawplace-mini/cart-shared';
import { EmptyCartCheckoutBlockedException } from './checkout-exceptions';
import type { BillingAddress } from './billing-address';
import type { PaymentMethod } from './payment-method';
import type { PickupStore } from './pickup-store';

/** << Entity >> — guest checkout session without account. */
export class GuestCheckout {
  readonly customer: Customer;
  readonly shoppingCart: ShoppingCart;
  email = '';
  guestOnlyLabel = true;
  clickAndCollectStore: PickupStore | null = null;
  billingAddress: BillingAddress | null = null;
  paymentMethod: PaymentMethod | null = null;
  processingPayment = false;
  paymentFailureMessage: string | null = null;

  constructor(customer: Customer, shoppingCart: ShoppingCart) {
    this.customer = customer;
    this.shoppingCart = shoppingCart;
  }

  static startFromNonEmptyShoppingCart(
    shoppingCart: ShoppingCart,
    customer: Customer,
  ): GuestCheckout {
    if (shoppingCart.isEmpty()) {
      GuestCheckout.blockCheckoutWhenShoppingCartEmpty(customer);
    }
    const session = new GuestCheckout(customer, shoppingCart);
    session.collectContactEmail('alex.rivera@example.com');
    return session;
  }

  static blockCheckoutWhenShoppingCartEmpty(customer: Customer): never {
    customer.directBackToCatalogOrCart();
    throw new EmptyCartCheckoutBlockedException();
  }

  collectContactEmail(email: string): void {
    this.email = email;
  }

  collectBillingAddressBeforePayment(billingAddress: BillingAddress): void {
    this.billingAddress = billingAddress;
  }

  collectPaymentMethodBeforeStripeWave(paymentMethod: PaymentMethod): void {
    this.paymentMethod = paymentMethod;
  }

  blockPaymentUntilPrerequisitesMet(): boolean {
    return (
      this.clickAndCollectStore != null &&
      (this.billingAddress?.isValid() ?? false) &&
      (this.paymentMethod?.isSelected() ?? false)
    );
  }

  showPaymentFailureWithoutOrder(failureReason: string): void {
    this.paymentFailureMessage = failureReason;
  }

  preventDuplicatePaymentSubmission(): boolean {
    return this.processingPayment;
  }

  setProcessingPayment(processing: boolean): void {
    this.processingPayment = processing;
  }
}
