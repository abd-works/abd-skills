/** << ValueObject >> — StripeWave processor outcome. */
export class StripeWaveResult {
  readonly outcome: string;

  private constructor(outcome: string) {
    this.outcome = outcome;
  }

  static fromProcessorResponse(outcome: string): StripeWaveResult {
    return new StripeWaveResult(outcome);
  }

  isSuccess(): boolean {
    return this.outcome === 'success';
  }

  isFailure(): boolean {
    return !this.isSuccess();
  }

  failureReason(): string {
    return this.outcome;
  }
}
