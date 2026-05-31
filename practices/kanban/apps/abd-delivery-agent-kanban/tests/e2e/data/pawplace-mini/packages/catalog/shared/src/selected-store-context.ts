/** << ValueObject >> — selected store context for catalog scope. */
export class SelectedStoreContext {
  readonly storeIdentity: string;
  readonly streetAddress: string;
  readonly active: boolean;

  private constructor(storeIdentity: string, streetAddress: string, active: boolean) {
    this.storeIdentity = storeIdentity;
    this.streetAddress = streetAddress;
    this.active = active;
  }

  static unset(): SelectedStoreContext {
    return new SelectedStoreContext('', '', false);
  }

  static fromStore(storeIdentity: string, streetAddress: string): SelectedStoreContext {
    return new SelectedStoreContext(storeIdentity, streetAddress, true);
  }

  isUnset(): boolean {
    return !this.active;
  }
}
