/**
 * Store pickup — shared test data and abstract Given/When/Then steps.
 * Epic: Shop & Pay Online | Sub-epic: Store pickup | Increment 2 — Sprint 3
 * Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
 */

export interface StoreEmployeeTestData {
  displayName: string;
}

export interface ClickAndCollectStoreTestData {
  storeIdentity: string;
}

export interface ClickAndCollectOrderTestData {
  orderId: string;
  customerContact: string;
  clickAndCollectStore: string;
  orderFulfillment: 'awaiting preparation' | 'ready for collection' | 'complete';
  paid: boolean;
  cartLines: { catalogItemIdentity: string; cartQuantity: number }[];
}

export abstract class FulfillmentBaseHelper {
  static readonly STORE_DOWNTOWN = 'Downtown PawPlace';
  static readonly STORE_WESTSIDE = 'Westside PawPlace';
  static readonly ORDER_CNC_1042 = 'CNC-1042';
  static readonly ORDER_CNC_1043 = 'CNC-1043';
  static readonly ORDER_CNC_1044 = 'CNC-1044';
  static readonly CONTACT_ALEX = 'alex.rivera@example.com';
  static readonly CONTACT_SAM = 'sam.patel@example.com';
  static readonly CONTACT_LEE = 'lee.chen@example.com';

  static readonly STORE_EMPLOYEE_JORDAN_KIM: StoreEmployeeTestData = {
    displayName: 'Jordan Kim',
  };

  static readonly CLICK_AND_COLLECT_STORE_DOWNTOWN: ClickAndCollectStoreTestData = {
    storeIdentity: FulfillmentBaseHelper.STORE_DOWNTOWN,
  };

  static readonly ORDER_1042_PAID: ClickAndCollectOrderTestData = {
    orderId: FulfillmentBaseHelper.ORDER_CNC_1042,
    customerContact: FulfillmentBaseHelper.CONTACT_ALEX,
    clickAndCollectStore: FulfillmentBaseHelper.STORE_DOWNTOWN,
    orderFulfillment: 'awaiting preparation',
    paid: true,
    cartLines: [
      { catalogItemIdentity: 'Premium Salmon Kibble', cartQuantity: 1 },
      { catalogItemIdentity: 'Reflective Dog Leash', cartQuantity: 1 },
    ],
  };

  static readonly ORDER_1043_PAID_WESTSIDE: ClickAndCollectOrderTestData = {
    orderId: FulfillmentBaseHelper.ORDER_CNC_1043,
    customerContact: FulfillmentBaseHelper.CONTACT_SAM,
    clickAndCollectStore: FulfillmentBaseHelper.STORE_WESTSIDE,
    orderFulfillment: 'awaiting preparation',
    paid: true,
    cartLines: [{ catalogItemIdentity: 'Premium Salmon Kibble', cartQuantity: 1 }],
  };

  static readonly ORDER_1044_UNPAID: ClickAndCollectOrderTestData = {
    orderId: FulfillmentBaseHelper.ORDER_CNC_1044,
    customerContact: FulfillmentBaseHelper.CONTACT_LEE,
    clickAndCollectStore: FulfillmentBaseHelper.STORE_DOWNTOWN,
    orderFulfillment: 'awaiting preparation',
    paid: false,
    cartLines: [],
  };

  protected storeEmployee: StoreEmployeeTestData =
    FulfillmentBaseHelper.STORE_EMPLOYEE_JORDAN_KIM;
  protected employeeStore: ClickAndCollectStoreTestData =
    FulfillmentBaseHelper.CLICK_AND_COLLECT_STORE_DOWNTOWN;

  abstract cleanup(): Promise<void>;

  protected notImplemented(step: string): never {
    throw new Error(`RED — ${step} not implemented (awaiting abd-clean-code)`);
  }

  async givenStoreEmployeeJordanKimBoundToDowntownPawPlace(): Promise<void> {
    this.storeEmployee = FulfillmentBaseHelper.STORE_EMPLOYEE_JORDAN_KIM;
    this.employeeStore = FulfillmentBaseHelper.CLICK_AND_COLLECT_STORE_DOWNTOWN;
    await this.seedEmployeeSessionAtStore(this.employeeStore);
  }

  async givenSprint3BackgroundOrdersSeeded(): Promise<void> {
    await this.seedPaidOrder(FulfillmentBaseHelper.ORDER_1042_PAID);
    await this.seedPaidOrder(FulfillmentBaseHelper.ORDER_1043_PAID_WESTSIDE);
    await this.seedUnpaidOrder(FulfillmentBaseHelper.ORDER_1044_UNPAID);
  }

  async givenClickAndCollectOrderAwaitingPreparation(
    order: ClickAndCollectOrderTestData,
  ): Promise<void> {
    await this.seedPaidOrder({ ...order, orderFulfillment: 'awaiting preparation' });
  }

  async givenClickAndCollectOrderReadyForCollection(
    order: ClickAndCollectOrderTestData,
  ): Promise<void> {
    await this.seedPaidOrder({ ...order, orderFulfillment: 'ready for collection' });
  }

  async givenClickAndCollectOrderFulfillmentComplete(
    order: ClickAndCollectOrderTestData,
  ): Promise<void> {
    await this.seedPaidOrder({ ...order, orderFulfillment: 'complete' });
  }

  async givenCustomerAlexRiveraSession(): Promise<void> {
    await this.seedCustomerSession('Alex Rivera');
  }

  protected abstract seedEmployeeSessionAtStore(
    store: ClickAndCollectStoreTestData,
  ): Promise<void>;
  protected abstract seedPaidOrder(order: ClickAndCollectOrderTestData): Promise<void>;
  protected abstract seedUnpaidOrder(order: ClickAndCollectOrderTestData): Promise<void>;
  protected abstract seedCustomerSession(displayName: string): Promise<void>;
}
