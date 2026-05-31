/** << Entity >> — confirmation gate before fulfillment queue exposure. */
export class OrderConfirmation {
  constructor(readonly confirmationComplete: boolean) {}

  isComplete(): boolean {
    return this.confirmationComplete;
  }
}
