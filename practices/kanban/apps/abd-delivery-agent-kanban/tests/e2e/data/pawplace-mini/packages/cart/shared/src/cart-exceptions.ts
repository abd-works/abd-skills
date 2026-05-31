export class UnavailableProductException extends Error {
  readonly productIdentity: string;

  constructor(productIdentity: string) {
    super(`product unavailable: ${productIdentity}`);
    this.name = 'UnavailableProductException';
    this.productIdentity = productIdentity;
  }
}

export class ZeroQuantityRejectedException extends Error {
  readonly messageToCustomer: string;

  constructor() {
    super('cart quantity cannot be zero — use remove product from cart');
    this.name = 'ZeroQuantityRejectedException';
    this.messageToCustomer =
      'Update cart quantity must not leave a line with zero cart quantity. Run remove product from cart instead.';
  }
}
