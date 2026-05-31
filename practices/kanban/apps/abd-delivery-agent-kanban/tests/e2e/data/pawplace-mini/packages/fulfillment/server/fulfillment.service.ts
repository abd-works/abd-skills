import type {
  FulfillmentOrderDetailDto,
  FulfillmentQueueRowDto,
} from '../shared/src/fulfillment.types';
import { ClickAndCollectOrder } from '../shared/src/click-and-collect-order';
import { FulfillClickAndCollectOrder } from '../shared/src/fulfill-click-and-collect-order';
import { PreparationIncompleteException } from '../shared/src/fulfillment-exceptions';
import { PrepareClickAndCollectOrdersForPickup } from '../shared/src/prepare-click-and-collect-orders-for-pickup';
import {
  FulfillmentRepository,
  type SeedOrderInput,
} from './fulfillment.repository';

export interface FulfillmentOrderResponse {
  order: FulfillmentOrderDetailDto;
  canFulfill: boolean;
}

export interface FulfillmentActionResponse {
  order: FulfillmentOrderDetailDto;
  blocked?: boolean;
  warning?: string;
  customerReceivedLines?: boolean;
}

export class FulfillmentService {
  private readonly prepareService = new PrepareClickAndCollectOrdersForPickup();
  private readonly fulfillService = new FulfillClickAndCollectOrder();

  constructor(private readonly repository: FulfillmentRepository) {}

  resetFixture(): void {
    this.repository.reset();
  }

  bindEmployeeSession(
    sessionId: string,
    displayName: string,
    storeIdentity: string,
  ): void {
    this.repository.bindEmployeeSession(sessionId, displayName, storeIdentity);
  }

  bindCustomerSession(sessionId: string): void {
    this.repository.bindCustomerSession(sessionId);
  }

  seedPaidOrder(input: SeedOrderInput): void {
    this.repository.seedOrder({ ...input, paid: true });
  }

  seedUnpaidOrder(input: SeedOrderInput): void {
    this.repository.seedOrder({ ...input, paid: false });
  }

  listQueue(
    staffToken: string | undefined,
    sessionId: string,
    storeIdentity: string,
  ): FulfillmentQueueRowDto[] {
    this.requireEmployeeAccess(staffToken, sessionId);
    const queue = this.repository.buildQueueForStore(storeIdentity);
    return this.prepareService.openQueueForClickAndCollectStore(
      queue,
      this.requireEmployee(sessionId),
      queue.clickAndCollectStore,
    );
  }

  getOrderDetail(
    staffToken: string | undefined,
    sessionId: string,
    orderId: string,
  ): FulfillmentOrderResponse {
    this.requireEmployeeAccess(staffToken, sessionId);
    const record = this.requireOrderRecord(orderId);
    return {
      order: this.toOrderDto(record.order),
      canFulfill: this.fulfillService.enableHandoffWhenPreparationComplete(
        record.order.orderFulfillment,
      ),
    };
  }

  markPreparing(
    staffToken: string | undefined,
    sessionId: string,
    orderId: string,
    storeIdentity: string,
  ): FulfillmentOrderDetailDto {
    this.requireEmployeeAccess(staffToken, sessionId);
    const record = this.requireOrderRecord(orderId);
    this.prepareService.updateStatusToReadyForCollection(
      record.order,
      record.order.orderFulfillment,
    );
    this.prepareService.keepOrderScopedToItsClickAndCollectStore(
      record.order.clickAndCollectStore,
      record.order,
    );
    return this.toOrderDto(record.order);
  }

  fulfillOrder(
    staffToken: string | undefined,
    sessionId: string,
    orderId: string,
  ): FulfillmentActionResponse {
    this.requireEmployeeAccess(staffToken, sessionId);
    const record = this.requireOrderRecord(orderId);

    if (record.order.orderFulfillment.isClosedAgainstRepeatPickup()) {
      return {
        order: this.toOrderDto(record.order),
        blocked: true,
        warning: 'order already collected or closed',
      };
    }

    if (record.order.orderFulfillment.blockPrematureCompletionBeforePrepare()) {
      return {
        order: this.toOrderDto(record.order),
        blocked: true,
        warning: 'preparation is incomplete',
      };
    }

    try {
      const queue = this.repository.buildQueueForStore(
        record.order.clickAndCollectStore.storeIdentity,
      );
      this.fulfillService.confirmHandoffAtPickup(
        record.order,
        record.order.orderFulfillment,
        queue,
        this.requireEmployee(sessionId),
        record.customer,
      );
      return {
        order: this.toOrderDto(record.order),
        customerReceivedLines: record.customer.collectedLines.length > 0,
      };
    } catch (error) {
      if (error instanceof PreparationIncompleteException) {
        return {
          order: this.toOrderDto(record.order),
          blocked: true,
          warning: 'preparation is incomplete',
        };
      }
      throw error;
    }
  }

  assertCustomerCannotAccessFulfillment(
    staffToken: string | undefined,
    sessionId: string,
  ): void {
    const session = this.repository.findSession(sessionId);
    if (session?.isCustomer || staffToken !== 'store-employee') {
      throw new Error('fulfillment queue unavailable to customer role');
    }
  }

  getDeliveredLines(orderId: string) {
    const record = this.repository.findOrder(orderId);
    return record?.customer.collectedLines ?? [];
  }

  private toOrderDto(order: ClickAndCollectOrder): FulfillmentOrderDetailDto {
    return {
      orderId: order.orderId,
      clickAndCollectStore: order.clickAndCollectStore.storeIdentity,
      orderFulfillment: order.orderFulfillment.currentStatus,
      cartLines: order.showLinesForHandoffDetail(),
      customerContact: order.customerContact,
    };
  }

  private requireOrderRecord(orderId: string) {
    const record = this.repository.findOrder(orderId);
    if (!record) {
      throw new Error(`click-and-collect order not found: ${orderId}`);
    }
    return record;
  }

  private requireEmployee(sessionId: string) {
    const session = this.repository.findSession(sessionId);
    if (!session?.storeEmployee) {
      throw new Error('store employee session required');
    }
    return session.storeEmployee;
  }

  private requireEmployeeAccess(
    staffToken: string | undefined,
    sessionId: string,
  ): void {
    const session = this.repository.findSession(sessionId);
    if (session?.isCustomer) {
      throw new Error('fulfillment queue unavailable to customer role');
    }
    this.requireStaffToken(staffToken);
  }

  private requireStaffToken(staffToken: string | undefined): void {
    if (staffToken !== 'store-employee') {
      throw new Error('employee access denied');
    }
  }
}
