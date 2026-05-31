import { InvalidBillingAddressException } from './checkout-exceptions';
import type { GuestCheckout } from './guest-checkout';
import type { ClickAndCollectOrder } from './click-and-collect-order';

/** << ValueObject >> — billing address on guest checkout. */
export class BillingAddress {
  readonly name: string;
  readonly street: string;
  readonly city: string;
  readonly postalCode: string;
  readonly country: string;

  constructor(
    name: string,
    street: string,
    city: string,
    postalCode: string,
    country: string,
  ) {
    this.name = name;
    this.street = street;
    this.city = city;
    this.postalCode = postalCode;
    this.country = country;
  }

  isValid(): boolean {
    return (
      this.name.trim().length > 0 &&
      this.street.trim().length > 0 &&
      this.city.trim().length > 0 &&
      this.postalCode.trim().length > 0 &&
      this.country.trim().length > 0
    );
  }

  saveOnCheckoutSessionWhenValid(guestCheckout: GuestCheckout): void {
    if (!this.isValid()) {
      throw new InvalidBillingAddressException();
    }
    guestCheckout.billingAddress = this;
  }

  replacePriorValuesBeforePayment(
    guestCheckout: GuestCheckout,
    revised: BillingAddress,
  ): BillingAddress {
    guestCheckout.billingAddress = revised;
    return revised;
  }

  attachToClickAndCollectOrderOnPay(order: ClickAndCollectOrder): void {
    order.billingAddress = this;
  }

  equals(other: BillingAddress): boolean {
    return (
      this.name === other.name &&
      this.street === other.street &&
      this.city === other.city &&
      this.postalCode === other.postalCode &&
      this.country === other.country
    );
  }
}
