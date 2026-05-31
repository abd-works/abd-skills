import React, { useState } from 'react';
import { FindStoreLayout } from '@pawplace-mini/store-client/FindStoreLayout';
import { SelectedStoreProvider } from '@pawplace-mini/store-client/SelectedStoreContext';
import { StoreListView } from '@pawplace-mini/store-client/StoreListView';
import { StoreMapView } from '@pawplace-mini/store-client/StoreMapView';

export interface StoreLocatorPageProps {
  initialTab?: 'map' | 'list';
  onNavigate?: (path: string) => void;
}

export function StoreLocatorPage({
  initialTab = 'map',
  onNavigate,
}: StoreLocatorPageProps) {
  const [activeTab, setActiveTab] = useState<'map' | 'list'>(initialTab);

  const handleTabChange = (tab: 'map' | 'list') => {
    setActiveTab(tab);
    onNavigate?.(tab === 'map' ? '/stores/map' : '/stores/list');
  };

  return (
    <SelectedStoreProvider onProceedToCatalog={() => onNavigate?.('/catalog')}>
      <FindStoreLayout activeTab={activeTab} onTabChange={handleTabChange}>
        {activeTab === 'map' ? <StoreMapView /> : <StoreListView />}
      </FindStoreLayout>
    </SelectedStoreProvider>
  );
}
