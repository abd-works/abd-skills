const DEFAULT_CURRENCY = 'USD';

/** << ValueObject >> — monetary amount with currency. */
export class Money {
  readonly amount: number;
  readonly currency: string;

  constructor(amount: number, currency: string = DEFAULT_CURRENCY) {
    this.amount = amount;
    this.currency = currency;
  }

  multiplyBy(cartQuantity: number): Money {
    return new Money(this.amount * cartQuantity, this.currency);
  }

  add(other: Money): Money {
    return new Money(this.amount + other.amount, this.currency);
  }

  static zero(currency: string = DEFAULT_CURRENCY): Money {
    return new Money(0, currency);
  }
}
