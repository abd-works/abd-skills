export class EmptyCartCheckoutBlockedException extends Error {
  constructor() {
    super('guest checkout blocked when shopping cart empty');
    this.name = 'EmptyCartCheckoutBlockedException';
  }
}

export class InvalidBillingAddressException extends Error {
  constructor() {
    super('invalid billing address');
    this.name = 'InvalidBillingAddressException';
  }
}

export class UnsupportedPaymentMethodException extends Error {
  constructor() {
    super('unsupported payment method');
    this.name = 'UnsupportedPaymentMethodException';
  }
}

export class CheckoutPrerequisitesIncompleteException extends Error {
  constructor() {
    super('checkout prerequisites incomplete');
    this.name = 'CheckoutPrerequisitesIncompleteException';
  }
}

export class PaymentNotConfirmedException extends Error {
  constructor() {
    super('payment not confirmed');
    this.name = 'PaymentNotConfirmedException';
  }
}

export class DuplicatePaymentSubmissionException extends Error {
  constructor() {
    super('duplicate payment submission prevented');
    this.name = 'DuplicatePaymentSubmissionException';
  }
}
