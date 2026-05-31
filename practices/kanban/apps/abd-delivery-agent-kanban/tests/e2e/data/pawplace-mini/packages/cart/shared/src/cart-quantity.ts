/** << ValueObject >> — positive whole number quantity on a cart line. */
export class CartQuantity {
  readonly value: number;

  constructor(value: number) {
    if (!Number.isInteger(value) || value < 0) {
      throw new Error('cart quantity must be a non-negative whole number');
    }
    this.value = value;
  }

  static one(): CartQuantity {
    return new CartQuantity(1);
  }

  increaseBy(amount: number): CartQuantity {
    return new CartQuantity(this.value + amount);
  }

  isPositiveWholeNumber(): boolean {
    return this.value > 0;
  }

  isZero(): boolean {
    return this.value === 0;
  }
}
