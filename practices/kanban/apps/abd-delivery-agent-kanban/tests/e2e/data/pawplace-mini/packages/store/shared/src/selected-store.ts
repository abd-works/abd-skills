import { GeographicPlacement } from './geographic-placement';
import { Store } from './store';

/** << Entity >> — active shopping context store from discovery selection. */
export class SelectedStore extends Store {
  readonly isActive: boolean;

  private constructor(store: Store, isActive: boolean) {
    super(store.id, store.retailLocationIdentity, store.geographicPlacement);
    this.isActive = isActive;
  }

  static unset(): SelectedStore {
    const placeholder = new Store(
      'unset',
      '',
      new GeographicPlacement('', 0, 0),
    );
    return new SelectedStore(placeholder, false);
  }

  static fromStore(store: Store): SelectedStore {
    return new SelectedStore(store, true);
  }

  setFromStoreMap(_customer: unknown, store: Store): SelectedStore {
    return SelectedStore.fromStore(store);
  }

  setFromStoreList(_customer: unknown, store: Store): SelectedStore {
    return SelectedStore.fromStore(store);
  }

  isUnset(): boolean {
    return !this.isActive;
  }

  scopesCatalogBrowse(): string {
    return this.retailLocationIdentity;
  }
}
