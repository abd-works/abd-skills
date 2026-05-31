import { ALL_STORES, rankStoresForLocation } from '../shared/mockStores';
import type { CustomerLocation, StoreWithDistance } from '../shared/types';

export async function fetchStores(): Promise<StoreWithDistance[]> {
  return [...ALL_STORES];
}

export async function fetchStoresWithDistance(
  location: CustomerLocation,
): Promise<StoreWithDistance[]> {
  return rankStoresForLocation(location);
}

export function resolveBrowserLocation(): Promise<CustomerLocation> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation unavailable'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => reject(error),
    );
  });
}
