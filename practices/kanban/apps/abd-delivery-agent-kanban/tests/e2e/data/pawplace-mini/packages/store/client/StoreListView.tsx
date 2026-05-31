import React, { useCallback, useEffect, useState } from 'react';
import { tokens } from '../../shared/layout-tokens';
import type { CustomerLocation, StoreRecord, StoreWithDistance } from '../shared/types';
import { useConfirmSelectedStore, useSelectedStore } from './SelectedStoreContext';
import { fetchStores, fetchStoresWithDistance, resolveBrowserLocation } from './store.api';

export interface StoreListViewProps {
  initialLocation?: CustomerLocation | null;
}

export function StoreListView({ initialLocation = null }: StoreListViewProps) {
  const { selectedStore, setSelectedStore } = useSelectedStore();
  const confirmSelection = useConfirmSelectedStore();
  const [stores, setStores] = useState<StoreWithDistance[]>([]);
  const [customerLocation, setCustomerLocation] = useState<CustomerLocation | null>(
    initialLocation,
  );
  const [locationError, setLocationError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadStores = useCallback(async (location: CustomerLocation | null) => {
    setLoading(true);
    const data = location
      ? await fetchStoresWithDistance(location)
      : await fetchStores();
    setStores(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    void loadStores(customerLocation);
  }, [customerLocation, loadStores]);

  const handleUseMyLocation = async () => {
    setLocationError(null);
    try {
      const location = await resolveBrowserLocation();
      setCustomerLocation(location);
    } catch {
      setLocationError('Could not access location. Try again or browse stores without distance.');
    }
  };

  if (loading) {
    return <p>Loading stores…</p>;
  }

  return (
    <section aria-label="Find Store — List" data-testid="store-list-view">
      <table
        data-testid="store-list"
        style={{ width: '100%', borderCollapse: 'collapse', ...tokens.body }}
      >
        <thead>
          <tr>
            <th scope="col" style={tokens.label}>
              store
            </th>
            <th scope="col" style={tokens.label}>
              address
            </th>
            <th scope="col" style={tokens.label}>
              distance to store
            </th>
          </tr>
        </thead>
        <tbody>
          {stores.map((store) => {
            const isSelected = selectedStore?.id === store.id;
            return (
              <tr
                key={store.id}
                data-testid="store-list-entry"
                onClick={() => setSelectedStore(store)}
                style={{
                  background: isSelected ? tokens.surfaceMuted : tokens.surface,
                  cursor: 'pointer',
                }}
              >
                <td>{store.retailLocationIdentity}</td>
                <td>{store.geographicPlacement}</td>
                <td data-testid="distance-to-store">
                  {store.distanceToStoreKm !== undefined
                    ? `${store.distanceToStoreKm.toFixed(1)} km`
                    : ''}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <div
        role="toolbar"
        aria-label="store list actions"
        style={{ marginTop: tokens.spacing.lg, display: 'flex', gap: tokens.spacing.md }}
      >
        <button type="button" onClick={() => void handleUseMyLocation()}>
          use my location
        </button>
        <button
          type="button"
          disabled={!selectedStore}
          onClick={confirmSelection}
          style={{
            background: tokens.accent,
            color: tokens.surface,
            border: 'none',
            padding: `${tokens.spacing.sm}px ${tokens.spacing.md}px`,
            cursor: selectedStore ? 'pointer' : 'not-allowed',
          }}
        >
          select store
        </button>
      </div>

      {locationError && (
        <p role="alert" style={{ color: tokens.accent, marginTop: tokens.spacing.sm }}>
          {locationError}
        </p>
      )}
    </section>
  );
}

export type { StoreRecord };
