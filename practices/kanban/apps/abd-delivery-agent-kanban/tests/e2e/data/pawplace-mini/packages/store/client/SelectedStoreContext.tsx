import React, { createContext, useCallback, useContext, useMemo, useState } from 'react';
import type { StoreRecord } from '../shared/types';

interface SelectedStoreContextValue {
  selectedStore: StoreRecord | null;
  setSelectedStore: (store: StoreRecord | null) => void;
  onProceedToCatalog?: () => void;
}

const SelectedStoreContext = createContext<SelectedStoreContextValue | null>(null);

export interface SelectedStoreProviderProps {
  children: React.ReactNode;
  onProceedToCatalog?: () => void;
  initialSelectedStore?: StoreRecord | null;
}

export function SelectedStoreProvider({
  children,
  onProceedToCatalog,
  initialSelectedStore = null,
}: SelectedStoreProviderProps) {
  const [selectedStore, setSelectedStore] = useState<StoreRecord | null>(
    initialSelectedStore,
  );

  const value = useMemo(
    () => ({ selectedStore, setSelectedStore, onProceedToCatalog }),
    [selectedStore, onProceedToCatalog],
  );

  return (
    <SelectedStoreContext.Provider value={value}>{children}</SelectedStoreContext.Provider>
  );
}

export function useSelectedStore(): SelectedStoreContextValue {
  const ctx = useContext(SelectedStoreContext);
  if (!ctx) {
    throw new Error('useSelectedStore requires SelectedStoreProvider');
  }
  return ctx;
}

export function useConfirmSelectedStore() {
  const { selectedStore, onProceedToCatalog } = useSelectedStore();
  return useCallback(() => {
    if (selectedStore && onProceedToCatalog) {
      onProceedToCatalog();
    }
  }, [selectedStore, onProceedToCatalog]);
}
