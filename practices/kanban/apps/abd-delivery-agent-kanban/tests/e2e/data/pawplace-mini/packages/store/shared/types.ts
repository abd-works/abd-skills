export interface StoreRecord {
  id: string;
  retailLocationIdentity: string;
  geographicPlacement: string;
}

export interface StoreWithDistance extends StoreRecord {
  distanceToStoreKm?: number;
}

export interface CustomerLocation {
  latitude: number;
  longitude: number;
}
