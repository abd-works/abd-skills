import type { CatalogProduct, ProductStockAtStore } from './catalog-types';

const PRODUCTS: CatalogProduct[] = [
  {
    catalogItemIdentity: 'Premium Salmon Kibble',
    description: 'grain-free salmon recipe for adult dogs',
    unitPrice: 24.99,
  },
  {
    catalogItemIdentity: 'Reflective Dog Leash',
    description: 'high-visibility leash for evening walks',
    unitPrice: 18.5,
  },
  {
    catalogItemIdentity: 'Limited Edition Cat Tree',
    description: 'multi-level climbing tower',
    unitPrice: 199.99,
  },
];

const stockByStore = new Map<string, Map<string, number>>();

function ensureStore(storeIdentity: string): Map<string, number> {
  let row = stockByStore.get(storeIdentity);
  if (!row) {
    row = new Map();
    stockByStore.set(storeIdentity, row);
  }
  return row;
}

export function seedDefaultStock(): void {
  stockByStore.clear();
  const downtown = ensureStore('Downtown PawPlace');
  downtown.set('Premium Salmon Kibble', 12);
  downtown.set('Reflective Dog Leash', 5);
  downtown.set('Limited Edition Cat Tree', 0);
  const westside = ensureStore('Westside PawPlace');
  westside.set('Premium Salmon Kibble', 8);
}

export function listProductsForStore(storeIdentity: string): CatalogProduct[] {
  if (!storeIdentity) return [];
  return PRODUCTS;
}

export function getProduct(catalogItemIdentity: string): CatalogProduct | undefined {
  return PRODUCTS.find((p) => p.catalogItemIdentity === catalogItemIdentity);
}

export function getRealTimeStock(
  storeIdentity: string,
  catalogItemIdentity: string,
): number {
  return ensureStore(storeIdentity).get(catalogItemIdentity) ?? 0;
}

export function setProductStockLevels(
  storeIdentity: string,
  catalogItemIdentity: string,
  levels: number,
): { ok: true } | { ok: false; message: string } {
  if (!Number.isFinite(levels) || levels < 0 || !Number.isInteger(levels)) {
    return { ok: false, message: 'validation message' };
  }
  ensureStore(storeIdentity).set(catalogItemIdentity, levels);
  return { ok: true };
}

export function listStockForStore(storeIdentity: string): ProductStockAtStore[] {
  return PRODUCTS.map((product) => ({
    storeIdentity,
    catalogItemIdentity: product.catalogItemIdentity,
    productStockLevels: getRealTimeStock(storeIdentity, product.catalogItemIdentity),
  }));
}

export function resetCatalogFixture(): void {
  seedDefaultStock();
}
