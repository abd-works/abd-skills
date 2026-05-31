import { Customer } from '../shared/src/customer';
import { SelectedStore } from '../shared/src/selected-store';
import { StockAvailability } from '../shared/src/stock-availability';

export interface CartSessionRecord {
  customer: Customer;
  stockAvailability: StockAvailability;
}

/** In-memory cart session persistence for guest checkout flows. */
export class CartRepository {
  private readonly sessions = new Map<string, CartSessionRecord>();

  saveSession(sessionId: string, record: CartSessionRecord): void {
    this.sessions.set(sessionId, record);
  }

  findSession(sessionId: string): CartSessionRecord | undefined {
    return this.sessions.get(sessionId);
  }

  deleteSession(sessionId: string): void {
    this.sessions.delete(sessionId);
  }

  createGuestSession(
    sessionId: string,
    displayName: string,
    storeIdentity: string,
  ): CartSessionRecord {
    const selectedStore = new SelectedStore(storeIdentity);
    const record: CartSessionRecord = {
      customer: new Customer(displayName, selectedStore),
      stockAvailability: new StockAvailability(),
    };
    this.saveSession(sessionId, record);
    return record;
  }

  reset(): void {
    this.sessions.clear();
  }
}
