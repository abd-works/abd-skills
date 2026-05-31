import React from 'react';
import { render, screen, fireEvent, within, waitFor } from '@testing-library/react';
import { vi, expect } from 'vitest';
import {
  FindStoreLayout,
  SelectedStoreProvider,
  StoreListView,
  StoreMapView,
} from '@pawplace-mini/store-client';
import * as storeApi from '@pawplace-mini/store-client';
import {
  ALTERNATE_CUSTOMER_LOCATION,
  FindAStoreBaseHelper,
  PRIMARY_CUSTOMER_LOCATION,
  type StoreTestData,
} from './find-a-store.base';

type ActiveView = 'map' | 'list';

export class FindAStoreClientHelper extends FindAStoreBaseHelper {
  private activeView: ActiveView = 'map';

  async cleanup(): Promise<void> {
    vi.restoreAllMocks();
    this.selectedStore = null;
    this.catalogNavigationCount = 0;
  }

  protected async seedDiscoverySessionWithoutSelectedStore(): Promise<void> {
    return;
  }

  protected async seedDiscoverySessionWithSharedLocation(
    latitude: number,
    longitude: number,
  ): Promise<void> {
    this.mockGeolocation({ latitude, longitude });
  }

  private renderShell(view: ActiveView, initialLocation: typeof PRIMARY_CUSTOMER_LOCATION | null = null) {
    this.activeView = view;
    const helper = this;
    const onProceedToCatalog = () => {
      helper.onProceedToCatalog();
    };

    function TestHarness() {
      const [activeTab, setActiveTab] = React.useState(view);
      return (
        <SelectedStoreProvider onProceedToCatalog={onProceedToCatalog}>
          <FindStoreLayout activeTab={activeTab} onTabChange={setActiveTab}>
            {activeTab === 'map' ? (
              <StoreMapView initialLocation={initialLocation} />
            ) : (
              <StoreListView initialLocation={initialLocation} />
            )}
          </FindStoreLayout>
        </SelectedStoreProvider>
      );
    }

    render(<TestHarness />);
  }

  mockGeolocation(location: { latitude: number; longitude: number }): void {
    Object.defineProperty(globalThis.navigator, 'geolocation', {
      configurable: true,
      writable: true,
      value: {
        getCurrentPosition(success: PositionCallback): void {
          success({
            coords: {
              latitude: location.latitude,
              longitude: location.longitude,
              accuracy: 10,
              altitude: null,
              altitudeAccuracy: null,
              heading: null,
              speed: null,
            },
            timestamp: Date.now(),
          } as GeolocationPosition);
        },
        watchPosition: vi.fn(),
        clearWatch: vi.fn(),
      },
    });
  }

  async whenCustomerOpensStoreMap(): Promise<void> {
    this.renderShell('map');
    await waitFor(() => screen.getByTestId('store-map-view'));
  }

  async whenCustomerOpensStoreList(): Promise<void> {
    this.renderShell('list');
    await waitFor(() => screen.getByTestId('store-list-view'));
  }

  async whenCustomerOpensStoreListWithLocation(): Promise<void> {
    this.mockGeolocation(PRIMARY_CUSTOMER_LOCATION);
    this.renderShell('list', PRIMARY_CUSTOMER_LOCATION);
    await waitFor(() => screen.getByTestId('store-list-view'));
  }

  async whenCustomerSelectsStoreOnMap(storeName: string): Promise<void> {
    const listbox = screen.getByTestId('store-map-listbox');
    fireEvent.click(within(listbox).getByText(storeName, { exact: false }));
    await waitFor(() => screen.getByTestId('selected-store-detail'));
    this.onSelectedStoreChange(
      FindAStoreBaseHelper.STORES.find((s) => s.retailLocationIdentity === storeName) ?? null,
    );
  }

  async whenCustomerSelectsStoreOnList(storeName: string): Promise<void> {
    const row = screen.getAllByTestId('store-list-entry').find((entry) =>
      within(entry).queryByText(storeName),
    );
    if (!row) throw new Error(`No list row for ${storeName}`);
    fireEvent.click(row);
    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'select store' })).not.toBeDisabled();
    });
    this.onSelectedStoreChange(
      FindAStoreBaseHelper.STORES.find((s) => s.retailLocationIdentity === storeName) ?? null,
    );
  }

  async whenCustomerClicksSelectStore(): Promise<void> {
    fireEvent.click(screen.getByRole('button', { name: 'select store' }));
  }

  async whenCustomerClicksUseMyLocation(): Promise<void> {
    fireEvent.click(screen.getByRole('button', { name: 'use my location' }));
    await waitFor(() => {
      expect(screen.getAllByTestId('store-list-entry')).toHaveLength(3);
      const distances = screen.queryAllByTestId('distance-to-store');
      expect(distances.length).toBe(3);
      expect(distances[0].textContent).toMatch(/km/);
    });
  }

  async whenCustomerSharesAlternateLocation(): Promise<void> {
    this.mockGeolocation(ALTERNATE_CUSTOMER_LOCATION);
    vi.spyOn(storeApi, 'resolveBrowserLocation').mockResolvedValue(ALTERNATE_CUSTOMER_LOCATION);
    await this.whenCustomerClicksUseMyLocation();
  }

  async whenCustomerSwitchesToMapTab(): Promise<void> {
    fireEvent.click(screen.getByRole('tab', { name: 'Map' }));
    await waitFor(() => screen.getByTestId('store-map-view'));
    this.activeView = 'map';
  }

  async whenCustomerSwitchesToListTab(): Promise<void> {
    fireEvent.click(screen.getByRole('tab', { name: 'List' }));
    await waitFor(() => screen.getByTestId('store-list-view'));
    this.activeView = 'list';
  }

  thenEveryStoreVisibleOnMap(): void {
    const entries = screen.getAllByTestId('store-map-entry');
    expect(entries).toHaveLength(3);
    for (const store of FindAStoreBaseHelper.STORES) {
      expect(screen.getByText(store.retailLocationIdentity)).toBeInTheDocument();
    }
  }

  thenStoresPresentedWithoutSearchOrFilter(): void {
    this.thenEveryStoreVisibleOnMap();
    this.thenNoSearchOrFilterAffordance();
  }

  thenSelectedStoreDetailVisible(storeName: string, address: string): void {
    const detail = screen.getByTestId('selected-store-detail');
    expect(within(detail).getByText(storeName)).toBeInTheDocument();
    expect(within(detail).getByText(address)).toBeInTheDocument();
  }

  thenNoStockAvailabilityOnMap(): void {
    expect(screen.queryByText(/stock availability/i)).not.toBeInTheDocument();
  }

  thenNoSearchOrFilterAffordance(): void {
    expect(screen.queryByPlaceholderText(/search/i)).not.toBeInTheDocument();
    expect(screen.queryByRole('searchbox')).not.toBeInTheDocument();
  }

  thenStoreListShowsAllStores(): void {
    expect(screen.getAllByTestId('store-list-entry')).toHaveLength(3);
  }

  thenListRowShowsStoreDetails(storeName: string, address: string): void {
    const row = screen
      .getAllByTestId('store-list-entry')
      .find((entry) => within(entry).queryByText(storeName));
    expect(row).toBeDefined();
    expect(within(row!).getByText(address)).toBeInTheDocument();
  }

  thenNavigatedToCatalogScopedTo(store: StoreTestData): void {
    expect(this.catalogNavigationCount).toBe(1);
    expect(this.selectedStore?.retailLocationIdentity).toBe(store.retailLocationIdentity);
  }

  thenMapTabPreservesStoreSet(): void {
    this.thenEveryStoreVisibleOnMap();
  }

  thenStoreListOmitsStockAvailability(): void {
    expect(screen.queryByText(/stock availability/i)).not.toBeInTheDocument();
  }

  thenNoDistanceValuesShown(): void {
    const distances = screen.queryAllByTestId('distance-to-store');
    for (const cell of distances) {
      expect(cell.textContent?.trim() ?? '').toBe('');
    }
  }

  thenStoresRankedNearestFirst(expectedOrder: string[]): void {
    const entries = screen.getAllByTestId('store-list-entry');
    const names = entries.map((entry) => within(entry).getAllByRole('cell')[0].textContent);
    expect(names).toEqual(expectedOrder);
  }

  thenDistanceShownForStore(storeName: string, km: number): void {
    const row = screen
      .getAllByTestId('store-list-entry')
      .find((entry) => within(entry).queryByText(storeName));
    expect(row).toBeDefined();
    expect(within(row!).getByTestId('distance-to-store')).toHaveTextContent(`${km.toFixed(1)} km`);
  }

  thenFirstListRowIs(storeName: string, km: number): void {
    const first = screen.getAllByTestId('store-list-entry')[0];
    expect(within(first).getByText(storeName)).toBeInTheDocument();
    expect(within(first).getByTestId('distance-to-store')).toHaveTextContent(`${km.toFixed(1)} km`);
  }
}
