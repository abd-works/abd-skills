import { Money } from './money';
import { Product } from './product';
import type { SelectedStoreContext } from './selected-store-context';

/** << ValueObject >> — composite key for stock by product and store. */
class ProductStoreKey {
  constructor(
    readonly productIdentity: string,
    readonly storeIdentity: string,
  ) {}

  static forProduct(product: Product, store: SelectedStoreContext): ProductStoreKey {
    return new ProductStoreKey(product.catalogItemIdentity, store.storeIdentity);
  }

  static fromIdentities(storeIdentity: string, productIdentity: string): ProductStoreKey {
    return new ProductStoreKey(productIdentity, storeIdentity);
  }

  toStorageKey(): string {
    return `${this.storeIdentity}::${this.productIdentity}`;
  }
}

/** << Entity >> — employee-maintained on-hand counts per store. */
export class ProductStockLevels {
  private levelsByProductAndStore = new Map<string, number>();
  private pendingEdits = new Map<string, number>();
  lastValidationMessage: string | null = null;

  static withDefaultFixture(): ProductStockLevels {
    const levels = new ProductStockLevels();
    levels.seedDefaultFixture();
    return levels;
  }

  seedDefaultFixture(): void {
    this.levelsByProductAndStore.clear();
    this.setLevel('Downtown PawPlace', 'Premium Salmon Kibble', 12);
    this.setLevel('Downtown PawPlace', 'Reflective Dog Leash', 5);
    this.setLevel('Downtown PawPlace', 'Limited Edition Cat Tree', 0);
    this.setLevel('Westside PawPlace', 'Premium Salmon Kibble', 8);
  }

  resetFixture(): void {
    this.pendingEdits.clear();
    this.lastValidationMessage = null;
    this.seedDefaultFixture();
  }

  onHandCountFor(product: Product, store: SelectedStoreContext): number {
    return this.levelsByProductAndStore.get(this.key(product, store)) ?? 0;
  }

  hasLevelFor(product: Product, store: SelectedStoreContext): boolean {
    return this.levelsByProductAndStore.has(this.key(product, store));
  }

  editQuantity(
    product: Product,
    store: SelectedStoreContext,
    proposedQuantity: number,
  ): void {
    this.pendingEdits.set(this.key(product, store), proposedQuantity);
  }

  persistValidUpdate(product: Product, store: SelectedStoreContext): number {
    const key = this.key(product, store);
    const proposedQuantity = this.pendingEdits.get(key);
    if (proposedQuantity === undefined) {
      return this.onHandCountFor(product, store);
    }
    if (!Number.isFinite(proposedQuantity) || proposedQuantity < 0 || !Number.isInteger(proposedQuantity)) {
      this.lastValidationMessage = 'validation message';
      return this.onHandCountFor(product, store);
    }
    this.levelsByProductAndStore.set(key, proposedQuantity);
    this.pendingEdits.delete(key);
    this.lastValidationMessage = null;
    return proposedQuantity;
  }

  private setLevel(storeIdentity: string, productIdentity: string, quantity: number): void {
    const storageKey = ProductStoreKey.fromIdentities(storeIdentity, productIdentity).toStorageKey();
    this.levelsByProductAndStore.set(storageKey, quantity);
  }

  private key(product: Product, store: SelectedStoreContext): string {
    return ProductStoreKey.forProduct(product, store).toStorageKey();
  }
}

export { ProductStoreKey };
