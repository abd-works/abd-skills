/** << ValueObject >> — buy-now signal derived from on-hand quantity. */
export class StockAvailabilityStatus {
  readonly label: 'available' | 'unavailable';

  private constructor(label: 'available' | 'unavailable') {
    this.label = label;
  }

  static available(): StockAvailabilityStatus {
    return new StockAvailabilityStatus('available');
  }

  static unavailable(): StockAvailabilityStatus {
    return new StockAvailabilityStatus('unavailable');
  }

  isAvailable(): boolean {
    return this.label === 'available';
  }

  isUnavailable(): boolean {
    return this.label === 'unavailable';
  }
}
