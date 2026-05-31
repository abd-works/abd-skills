/** << Entity >> — browsing context from Increment 1. */
export class SelectedStore {
  readonly storeIdentity: string;

  constructor(storeIdentity: string) {
    this.storeIdentity = storeIdentity;
  }

  scopesCatalogBrowse(): string {
    return this.storeIdentity;
  }
}
