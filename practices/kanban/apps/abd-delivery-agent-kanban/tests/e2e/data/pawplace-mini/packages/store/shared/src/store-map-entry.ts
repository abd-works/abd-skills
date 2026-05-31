import { Store } from './store';

/** << ValueObject >> — selectable map row without stock availability in Sprint 1. */
export class StoreMapEntry {
  constructor(
    readonly store: Store,
    readonly distanceToStoreKm: number | undefined,
    readonly stockAvailabilityShown: boolean,
  ) {}

  static fromStore(store: Store, distanceKm?: number): StoreMapEntry {
    return new StoreMapEntry(store, distanceKm, false);
  }
}
