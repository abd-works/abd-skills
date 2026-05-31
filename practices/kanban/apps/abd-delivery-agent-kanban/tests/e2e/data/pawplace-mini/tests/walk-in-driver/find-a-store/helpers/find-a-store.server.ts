/**

 * Find a store — server-tier helper (Supertest + StoreService / StoreApi).

 */

import assert from 'node:assert/strict';

import type { Express } from 'express';

import request from 'supertest';

import { createAppServer } from '@pawplace-mini/app-server';

import type { StoreService } from '@pawplace-mini/store-server';

import type {

  DiscoverySessionDto,

  StoreListViewDto,

  StoreMapViewDto,

} from '@pawplace-mini/store-shared';

import {

  FindAStoreBaseHelper,

  type StoreTestData,

} from './find-a-store.base';



export class FindAStoreServerHelper extends FindAStoreBaseHelper {

  private readonly app: Express;

  private readonly service: StoreService;

  private readonly sessionId = 'find-a-store-session';

  private lastMap!: StoreMapViewDto;

  private lastList!: StoreListViewDto;

  private lastSession!: DiscoverySessionDto;

  private lastSelect!: { catalogScope: string; selectedStore: StoreTestData };



  constructor() {

    super();

    const server = createAppServer();

    this.app = server.app;

    this.service = server.storeService;

  }



  async cleanup(): Promise<void> {

    this.service.resetFixture();

    this.lastMap = undefined as unknown as StoreMapViewDto;

    this.lastList = undefined as unknown as StoreListViewDto;

    this.lastSession = undefined as unknown as DiscoverySessionDto;

    this.lastSelect = undefined as unknown as typeof this.lastSelect;

  }



  protected async seedDiscoverySessionWithoutSelectedStore(): Promise<void> {

    const response = await request(this.app)

      .post('/api/v1/store-discovery/sessions')

      .set('x-session-id', this.sessionId)

      .send({ displayName: this.customer.displayName });

    assert.equal(response.status, 201);

    this.lastSession = response.body.session;

  }



  protected async seedDiscoverySessionWithSharedLocation(

    latitude: number,

    longitude: number,

  ): Promise<void> {

    const response = await request(this.app)

      .post('/api/v1/store-discovery/sessions')

      .set('x-session-id', this.sessionId)

      .send({

        displayName: this.customer.displayName,

        customerLocation: { latitude, longitude },

      });

    assert.equal(response.status, 201);

    this.lastSession = response.body.session;

  }



  async whenCustomerOpensStoreMapViaApi(): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .get('/api/v1/stores/map')

      .set('x-session-id', this.sessionId);

    assert.equal(response.status, 200);

    this.lastMap = response.body;

  }



  async whenCustomerOpensStoreListViaApi(): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .get('/api/v1/stores/list')

      .set('x-session-id', this.sessionId);

    assert.equal(response.status, 200);

    this.lastList = response.body;

  }



  async whenCustomerSelectsStoreOnMapViaApi(store: StoreTestData): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .post('/api/v1/stores/map/select')

      .set('x-session-id', this.sessionId)

      .send({ storeId: store.id });

    assert.equal(response.status, 200);

    this.lastSelect = response.body;

    this.onSelectedStoreChange(store);

  }



  async whenCustomerSelectsStoreOnListViaApi(store: StoreTestData): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .post('/api/v1/stores/list/select')

      .set('x-session-id', this.sessionId)

      .send({ storeId: store.id });

    assert.equal(response.status, 200);

    this.lastSelect = response.body;

    this.onSelectedStoreChange(store);

  }



  async whenCustomerSharesLocationViaApi(latitude: number, longitude: number): Promise<void> {

    await this.ensureSession();

    const response = await request(this.app)

      .post('/api/v1/stores/location')

      .set('x-session-id', this.sessionId)

      .send({ latitude, longitude });

    assert.equal(response.status, 200);

    this.lastList = response.body;

  }



  async whenCustomerSwitchesToMapViewViaApi(): Promise<void> {

    await this.whenCustomerOpensStoreMapViaApi();

  }



  thenStoreMapShowsEveryStoreAsSelectable(): void {

    assert.equal(this.lastMap.entries.length, 3);

    for (const store of FindAStoreBaseHelper.STORES) {

      assert.ok(

        this.lastMap.entries.some(

          (entry) => entry.retailLocationIdentity === store.retailLocationIdentity,

        ),

      );

    }

  }



  thenSelectedStoreIs(store: StoreTestData): void {

    assert.equal(this.lastSelect.selectedStore.retailLocationIdentity, store.retailLocationIdentity);

    assert.equal(this.getSelectedStore()?.retailLocationIdentity, store.retailLocationIdentity);

  }



  thenStoreMapOmitsStockAvailability(): void {

    assert.equal(this.lastMap.stockAvailabilityShown, false);

    assert.ok(this.lastMap.entries.every((entry) => !entry.stockAvailabilityShown));

  }



  thenStoresPresentedWithoutSearchOrFilter(): void {

    assert.equal(this.lastMap.allStoresPresentedWithoutSearchOrFilter, true);

    this.thenStoreMapShowsEveryStoreAsSelectable();

  }



  thenStoreListShowsAlternativeToMap(): void {

    assert.equal(this.lastList.alternativeToMap, true);

    assert.equal(this.lastList.rows.length, 3);

    for (const store of FindAStoreBaseHelper.STORES) {

      const row = this.lastList.rows.find(

        (entry) => entry.retailLocationIdentity === store.retailLocationIdentity,

      );

      assert.ok(row);

      assert.equal(row!.geographicPlacement, store.geographicPlacement);

    }

  }



  thenCustomerCanProceedToCatalogScopedTo(store: StoreTestData): void {

    assert.equal(this.lastSelect.catalogScope, store.retailLocationIdentity);

    this.onProceedToCatalog();

  }



  thenMapSwitchPreservesDiscoveryContext(): void {

    assert.equal(this.lastMap.entries.length, 3);

    this.thenStoreMapShowsEveryStoreAsSelectable();

  }



  thenStoreListOmitsStockAvailability(): void {

    assert.equal(this.lastList.stockAvailabilityShown, false);

    assert.ok(this.lastList.rows.every((row) => !row.stockAvailabilityShown));

  }



  thenStoresRankedNearestFirst(expectedOrder: string[], distancesKm: number[]): void {

    const names = this.lastList.rows.map((row) => row.retailLocationIdentity);

    assert.deepEqual(names, expectedOrder);

    for (let index = 0; index < expectedOrder.length; index += 1) {

      assert.equal(this.lastList.rows[index]!.distanceToStoreKm, distancesKm[index]);

    }

  }



  thenNoDistanceValuesOnMapOrList(): void {

    const mapDistances = this.lastMap?.entries ?? [];

    const listDistances = this.lastList?.rows ?? [];

    for (const entry of [...mapDistances, ...listDistances]) {
      assert.ok(entry.distanceToStoreKm == null);
    }

  }



  thenFirstStoreRowIs(storeName: string, km: number): void {

    assert.equal(this.lastList.rows[0]!.retailLocationIdentity, storeName);

    assert.equal(this.lastList.rows[0]!.distanceToStoreKm, km);

  }



  thenDistanceRankingRecalculatedForAlternateLocation(): void {

    assert.notEqual(

      this.lastList.rows[0]!.retailLocationIdentity,

      'Downtown PawPlace',

    );

  }



  private async ensureSession(): Promise<void> {

    if (this.lastSession) return;

    await this.seedDiscoverySessionWithoutSelectedStore();

  }

}

