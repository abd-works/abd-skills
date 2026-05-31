import { Store } from './store';

/** << ValueObject >> — readable list row without stock availability in Sprint 1. */
export class StoreListRow {
  constructor(
    readonly store: Store,
    readonly distanceToStoreKm: number | undefined,
    readonly stockAvailabilityShown: boolean,
  ) {}

  static fromStore(store: Store, distanceKm?: number): StoreListRow {
    return new StoreListRow(store, distanceKm, false);
  }
}
