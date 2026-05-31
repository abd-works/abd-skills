import type {
  CatalogBrowseView,
  ProductDetailView,
  StockMaintenanceViewDto,
  SaveStockLevelsResponseDto,
} from '../shared/src/catalog.schema';
import { StoreEmployee, WalkInCustomer, type Product } from '../shared/src/index';
import type { StoreRepository } from '../../store/server/store.repository';
import { CatalogRepository } from './catalog.repository';

export class CatalogService {
  constructor(
    private readonly repository: CatalogRepository,
    private readonly storeRepository: StoreRepository,
  ) {}

  resetFixture(): void {
    this.repository.reset();
    this.storeRepository.reset();
  }

  getCatalogBrowse(sessionId: string): CatalogBrowseView {
    const selectedStore = this.resolveSelectedStore(sessionId);
    const customer = new WalkInCustomer('Alex Rivera', selectedStore);
    return customer.browseCatalogAfterSelectedStore(
      this.repository.catalog,
      this.repository.products,
      this.repository.productStockLevels,
    );
  }

  getProductDetail(sessionId: string, catalogItemIdentity: string): ProductDetailView {
    const selectedStore = this.requireSelectedStore(sessionId);
    const product = this.requireProduct(catalogItemIdentity);
    const customer = new WalkInCustomer('Alex Rivera', selectedStore);
    return customer.openProductDetailFromCatalog(
      product,
      this.repository.catalog,
      this.repository.realTimeStock,
      this.repository.stockAvailability,
      this.repository.productStockLevels,
    );
  }

  getStockMaintenance(staffToken: string | undefined, storeIdentity: string): StockMaintenanceViewDto {
    this.requireStaffToken(staffToken);
    const store = this.repository.selectedStoreFromIdentity(storeIdentity);
    const rows = this.repository.products.everyCatalogProduct.map((product) => ({
      storeIdentity,
      catalogItemIdentity: product.catalogItemIdentity,
      productStockLevels: this.repository.productStockLevels.onHandCountFor(
        product,
        store,
      ),
      editable: true,
    }));
    return { storeIdentity, rows };
  }

  saveStockLevels(
    staffToken: string | undefined,
    storeIdentity: string,
    updates: { catalogItemIdentity: string; productStockLevels: number }[],
  ): SaveStockLevelsResponseDto {
    this.requireStaffToken(staffToken);
    const store = this.repository.selectedStoreFromIdentity(storeIdentity);
    const employee = new StoreEmployee('Jordan Lee', storeIdentity);

    for (const update of updates) {
      const product = this.requireProduct(update.catalogItemIdentity);
      employee.saveProductStockLevels(
        product,
        store,
        update.productStockLevels,
        this.repository.productStockLevels,
      );
      if (this.repository.productStockLevels.lastValidationMessage) {
        return {
          ok: false,
          message: this.repository.productStockLevels.lastValidationMessage,
        };
      }
    }

    return { ok: true };
  }

  getRealTimeStockAtStore(storeIdentity: string, catalogItemIdentity: string): number {
    const store = this.repository.selectedStoreFromIdentity(storeIdentity);
    const product = this.requireProduct(catalogItemIdentity);
    return this.repository.realTimeStock.showOnHandQuantityAtStore(
      product,
      store,
      this.repository.productStockLevels,
    );
  }

  private resolveSelectedStore(sessionId: string): ReturnType<CatalogRepository['selectedStoreFromIdentity']> {
    const session = this.storeRepository.findSession(sessionId);
    if (!session || session.customer.selectedStore.isUnset()) {
      return this.repository.selectedStoreFromIdentity('');
    }
    return this.repository.selectedStoreFromIdentity(
      session.customer.selectedStore.retailLocationIdentity,
    );
  }

  private requireSelectedStore(sessionId: string) {
    const selectedStore = this.resolveSelectedStore(sessionId);
    if (selectedStore.isUnset()) {
      throw new Error('selected store required');
    }
    return selectedStore;
  }

  private requireProduct(catalogItemIdentity: string): Product {
    const product = this.repository.products.everyCatalogProduct.find(
      (entry) => entry.catalogItemIdentity === catalogItemIdentity,
    );
    if (!product) {
      throw new Error(`product not found: ${catalogItemIdentity}`);
    }
    return product;
  }

  private requireStaffToken(staffToken: string | undefined): void {
    if (staffToken !== 'store-employee') {
      throw new Error('employee access denied');
    }
  }
}
