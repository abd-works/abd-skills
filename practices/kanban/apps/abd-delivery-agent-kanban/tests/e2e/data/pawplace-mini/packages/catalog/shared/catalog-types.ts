export interface CatalogProduct {
  catalogItemIdentity: string;
  description: string;
  unitPrice: number;
}

export interface ProductStockAtStore {
  storeIdentity: string;
  catalogItemIdentity: string;
  productStockLevels: number;
}

export function stockAvailabilityFromLevels(levels: number): 'available' | 'unavailable' {
  return levels > 0 ? 'available' : 'unavailable';
}
