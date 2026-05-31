import { Customer } from '../shared/src/customer';
import { CustomerLocation } from '../shared/src/customer-location';
import type { CustomerLocation as CustomerLocationDto } from '../shared/types';

export interface StoreSessionRecord {
  customer: Customer;
  activeView: 'map' | 'list' | null;
}

/** In-memory store discovery session persistence. */
export class StoreRepository {
  private readonly sessions = new Map<string, StoreSessionRecord>();

  saveSession(sessionId: string, record: StoreSessionRecord): void {
    this.sessions.set(sessionId, record);
  }

  findSession(sessionId: string): StoreSessionRecord | undefined {
    return this.sessions.get(sessionId);
  }

  createDiscoverySession(
    sessionId: string,
    displayName: string,
    customerLocation?: CustomerLocationDto,
  ): StoreSessionRecord {
    const customer = new Customer(displayName);
    if (customerLocation) {
      customer.customerLocation = CustomerLocation.fromDto(customerLocation);
    }
    const record: StoreSessionRecord = { customer, activeView: null };
    this.saveSession(sessionId, record);
    return record;
  }

  reset(): void {
    this.sessions.clear();
  }
}
