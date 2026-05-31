import type { GuestCheckout } from '@pawplace-mini/checkout-shared';
import type { ClickAndCollectOrder } from '@pawplace-mini/checkout-shared';
import type { OrderConfirmation } from '@pawplace-mini/checkout-shared';
import type { StripeWave } from '@pawplace-mini/checkout-shared';

export interface CheckoutSessionRecord {
  guestCheckout: GuestCheckout;
  stripeWave: StripeWave;
  placedOrder: ClickAndCollectOrder | null;
  orderConfirmation: OrderConfirmation | null;
}

/** In-memory checkout session persistence. */
export class CheckoutRepository {
  private readonly sessions = new Map<string, CheckoutSessionRecord>();
  private lastStripeChargeAmount: number | null = null;

  saveSession(sessionId: string, record: CheckoutSessionRecord): void {
    this.sessions.set(sessionId, record);
  }

  findSession(sessionId: string): CheckoutSessionRecord | undefined {
    return this.sessions.get(sessionId);
  }

  deleteSession(sessionId: string): void {
    this.sessions.delete(sessionId);
  }

  recordStripeCharge(amount: number): void {
    this.lastStripeChargeAmount = amount;
  }

  getLastStripeChargeAmount(): number | null {
    return this.lastStripeChargeAmount;
  }

  reset(): void {
    this.sessions.clear();
    this.lastStripeChargeAmount = null;
  }
}
