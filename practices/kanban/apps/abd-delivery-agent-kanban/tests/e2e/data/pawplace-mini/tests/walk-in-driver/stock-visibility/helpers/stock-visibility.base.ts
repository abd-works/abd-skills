/**
 * Stock visibility — shared test data (Increment 1 Sprint 2).
 * Source: docs/increments/1-walk-in-driver/specification/interface-design.md
 */

export interface SelectedStoreTestData {
  storeIdentity: string;
  streetAddress: string;
}

export interface ProductTestData {
  catalogItemIdentity: string;
  description: string;
  unitPrice: number;
}

export const DOWNTOWN_STORE: SelectedStoreTestData = {
  storeIdentity: 'Downtown PawPlace',
  streetAddress: '100 Main Street',
};

export const WESTSIDE_STORE: SelectedStoreTestData = {
  storeIdentity: 'Westside PawPlace',
  streetAddress: '42 Oak Avenue',
};

export const PRODUCT_SALMON: ProductTestData = {
  catalogItemIdentity: 'Premium Salmon Kibble',
  description: 'grain-free salmon recipe for adult dogs',
  unitPrice: 24.99,
};

export const PRODUCT_LEASH: ProductTestData = {
  catalogItemIdentity: 'Reflective Dog Leash',
  description: 'high-visibility leash for evening walks',
  unitPrice: 18.5,
};

export const PRODUCT_CAT_TREE: ProductTestData = {
  catalogItemIdentity: 'Limited Edition Cat Tree',
  description: 'multi-level climbing tower',
  unitPrice: 199.99,
};
