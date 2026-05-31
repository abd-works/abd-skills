/** << ValueObject >> — unit price for catalog products. */
export class Money {
  readonly amount: number;
  readonly currency: string;

  constructor(amount: number, currency = 'USD') {
    this.amount = amount;
    this.currency = currency;
  }

  formatted(): string {
    return `$${this.amount.toFixed(2)}`;
  }
}
