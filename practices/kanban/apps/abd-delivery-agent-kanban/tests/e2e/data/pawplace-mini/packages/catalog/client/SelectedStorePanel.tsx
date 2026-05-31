import React from 'react';
import type { SelectedStoreState } from '../../shared/selected-store';
import { layoutTokens } from '../../shared/layout-tokens';

interface SelectedStorePanelProps {
  store: SelectedStoreState;
  onChangeStore?: () => void;
}

export function SelectedStorePanel({ store, onChangeStore }: SelectedStorePanelProps) {
  return (
    <aside
      data-testid="selected-store-panel"
      aria-label="selected store"
      style={{ padding: layoutTokens.spacing[2], background: layoutTokens.surfaceMuted }}
    >
      <p style={layoutTokens.body}>
        {store.storeIdentity} — {store.streetAddress}
      </p>
      <button type="button" onClick={onChangeStore}>
        change store
      </button>
    </aside>
  );
}
