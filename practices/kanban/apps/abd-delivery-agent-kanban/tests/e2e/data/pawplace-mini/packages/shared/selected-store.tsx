import React, { createContext, useCallback, useContext, useMemo, useState } from 'react';

export interface SelectedStoreState {
  storeIdentity: string;
  streetAddress: string;
}

interface SelectedStoreContextValue {
  selectedStore: SelectedStoreState | null;
  setSelectedStore: (store: SelectedStoreState | null) => void;
  clearSelectedStore: () => void;
}

const SelectedStoreContext = createContext<SelectedStoreContextValue | null>(null);

export function SelectedStoreProvider({
  initialStore = null,
  children,
}: {
  initialStore?: SelectedStoreState | null;
  children: React.ReactNode;
}) {
  const [selectedStore, setSelectedStore] = useState<SelectedStoreState | null>(initialStore);
  const clearSelectedStore = useCallback(() => setSelectedStore(null), []);
  const value = useMemo(
    () => ({ selectedStore, setSelectedStore, clearSelectedStore }),
    [selectedStore, clearSelectedStore],
  );
  return (
    <SelectedStoreContext.Provider value={value}>{children}</SelectedStoreContext.Provider>
  );
}

export function useSelectedStore(): SelectedStoreContextValue {
  const ctx = useContext(SelectedStoreContext);
  if (!ctx) {
    throw new Error('useSelectedStore must be used within SelectedStoreProvider');
  }
  return ctx;
}
