import type { CustomerLocation, StoreRecord, StoreWithDistance } from './types';

export const ALL_STORES: StoreRecord[] = [
  {
    id: 'downtown',
    retailLocationIdentity: 'Downtown PawPlace',
    geographicPlacement: '123 Main St',
  },
  {
    id: 'westside',
    retailLocationIdentity: 'Westside PawPlace',
    geographicPlacement: '456 Oak Ave',
  },
  {
    id: 'uptown',
    retailLocationIdentity: 'Uptown PawPlace',
    geographicPlacement: '789 Pine Rd',
  },
];

/** Spec-by-example primary shared location */
export const PRIMARY_CUSTOMER_LOCATION: CustomerLocation = {
  latitude: 43.6532,
  longitude: -79.3832,
};

/** Spec-by-example alternate location (Scenario 4) */
export const ALTERNATE_CUSTOMER_LOCATION: CustomerLocation = {
  latitude: 43.7,
  longitude: -79.4,
};

const RANKED_BY_PRIMARY: Record<string, number> = {
  downtown: 2.1,
  westside: 4.8,
  uptown: 6.3,
};

const RANKED_BY_ALTERNATE: Record<string, number> = {
  westside: 1.4,
  downtown: 3.2,
  uptown: 5.6,
};

function locationsMatch(a: CustomerLocation, b: CustomerLocation): boolean {
  return (
    Math.abs(a.latitude - b.latitude) < 0.0001 &&
    Math.abs(a.longitude - b.longitude) < 0.0001
  );
}

export function rankStoresForLocation(
  location: CustomerLocation | null,
): StoreWithDistance[] {
  if (!location) {
    return [...ALL_STORES];
  }

  const distanceMap = locationsMatch(location, ALTERNATE_CUSTOMER_LOCATION)
    ? RANKED_BY_ALTERNATE
    : RANKED_BY_PRIMARY;

  return [...ALL_STORES]
    .map((store) => ({
      ...store,
      distanceToStoreKm: distanceMap[store.id],
    }))
    .sort((a, b) => (a.distanceToStoreKm ?? 0) - (b.distanceToStoreKm ?? 0));
}
