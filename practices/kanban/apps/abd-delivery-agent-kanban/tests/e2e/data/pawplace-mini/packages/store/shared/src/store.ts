import type { StoreRecord } from '../types';
import { GeographicPlacement } from './geographic-placement';

/** << Entity >> — physical PawPlace retail location. */
export class Store {
  constructor(
    readonly id: string,
    readonly retailLocationIdentity: string,
    readonly geographicPlacement: GeographicPlacement,
  ) {}

  static fromRecord(record: StoreRecord): Store {
    return new Store(
      record.id,
      record.retailLocationIdentity,
      new GeographicPlacement(record.geographicPlacement, 0, 0),
    );
  }
}
