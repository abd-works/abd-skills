/**
 * Store pickup — client-tier helper.
 */
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect } from 'vitest';
import { RequireStoreEmployee } from '@pawplace-mini/inventory-client';
import {
  FulfillmentOrderView,
  FulfillmentOrdersView,
  InMemoryFulfillmentApi,
} from '@pawplace-mini/fulfillment-client';
import {
  FulfillmentBaseHelper,
  type ClickAndCollectOrderTestData,
  type ClickAndCollectStoreTestData,
} from './fulfillment.base';

export class FulfillmentClientHelper extends FulfillmentBaseHelper {
  private fulfillmentApi = new InMemoryFulfillmentApi();
  private container: HTMLElement | null = null;
  private isEmployee = true;

  async cleanup(): Promise<void> {
    this.container?.remove();
    this.container = null;
    this.fulfillmentApi.reset();
    this.isEmployee = true;
    this.employeeStore = FulfillmentBaseHelper.CLICK_AND_COLLECT_STORE_DOWNTOWN;
  }

  /** @deprecated use givenStoreEmployeeJordanKimBoundToDowntownPawPlace */
  async givenStoreEmployeeAtDowntown(): Promise<void> {
    await this.givenStoreEmployeeJordanKimBoundToDowntownPawPlace();
  }

  protected async seedEmployeeSessionAtStore(
    store: ClickAndCollectStoreTestData,
  ): Promise<void> {
    this.isEmployee = true;
    this.employeeStore = store;
    this.fulfillmentApi.reset();
    this.fulfillmentApi.seedOrders([
      {
        orderId: FulfillmentBaseHelper.ORDER_CNC_1042,
        clickAndCollectStore: FulfillmentBaseHelper.STORE_DOWNTOWN,
        orderFulfillment: 'awaiting preparation',
        customerContact: FulfillmentBaseHelper.CONTACT_ALEX,
        cartLines: [
          { catalogItemIdentity: 'Premium Salmon Kibble', cartQuantity: 1 },
          { catalogItemIdentity: 'Reflective Dog Leash', cartQuantity: 1 },
        ],
      },
      {
        orderId: FulfillmentBaseHelper.ORDER_CNC_1043,
        clickAndCollectStore: FulfillmentBaseHelper.STORE_WESTSIDE,
        orderFulfillment: 'awaiting preparation',
        customerContact: FulfillmentBaseHelper.CONTACT_SAM,
        cartLines: [{ catalogItemIdentity: 'Premium Salmon Kibble', cartQuantity: 1 }],
      },
    ]);
    this.fulfillmentApi.seedUnpaidOrder({
      orderId: FulfillmentBaseHelper.ORDER_CNC_1044,
      clickAndCollectStore: FulfillmentBaseHelper.STORE_DOWNTOWN,
      orderFulfillment: 'awaiting preparation',
      customerContact: FulfillmentBaseHelper.CONTACT_LEE,
      cartLines: [],
    });
  }

  protected async seedPaidOrder(order: ClickAndCollectOrderTestData): Promise<void> {
    this.fulfillmentApi.seedOrders([
      {
        orderId: order.orderId,
        clickAndCollectStore: order.clickAndCollectStore,
        orderFulfillment: order.orderFulfillment,
        customerContact: order.customerContact,
        cartLines: order.cartLines,
      },
    ]);
  }

  protected async seedUnpaidOrder(order: ClickAndCollectOrderTestData): Promise<void> {
    this.fulfillmentApi.seedUnpaidOrder({
      orderId: order.orderId,
      clickAndCollectStore: order.clickAndCollectStore,
      orderFulfillment: order.orderFulfillment,
      customerContact: order.customerContact,
      cartLines: order.cartLines,
    });
  }

  protected async seedCustomerSession(_displayName: string): Promise<void> {
    this.isEmployee = false;
  }

  async givenCustomerSession(): Promise<void> {
    await this.givenCustomerAlexRiveraSession();
  }

  async whenEmployeeOpensFulfillmentQueue(): Promise<void> {
    this.renderQueue();
  }

  async whenEmployeeMarksOrderPreparing(orderId: string): Promise<void> {
    this.renderQueue();
    await userEvent.click(
      withinRow(orderId).getByRole('button', { name: 'mark preparing' }),
    );
    this.renderQueue();
  }

  async whenEmployeeOpensOrderDetail(orderId: string): Promise<void> {
    this.renderOrderDetail(orderId);
  }

  async whenEmployeeAttemptsFulfill(orderId: string): Promise<void> {
    this.renderOrderDetail(orderId);
    const btn = screen.getByRole('button', { name: 'fulfill click-and-collect order' });
    if (!btn.hasAttribute('disabled')) {
      await userEvent.click(btn);
    }
    this.renderOrderDetail(orderId);
  }

  async whenCustomerAttemptsFulfillmentQueue(): Promise<void> {
    this.renderQueue();
  }

  thenUiListsOrderInQueue(orderId: string): void {
    expect(screen.getByTestId(`queue-row-${orderId}`)).toBeInTheDocument();
  }

  thenUiDoesNotListOrder(orderId: string): void {
    expect(screen.queryByTestId(`queue-row-${orderId}`)).not.toBeInTheDocument();
  }

  thenUiShowsStatus(orderId: string, status: string): void {
    expect(screen.getByTestId(`status-${orderId}`)).toHaveTextContent(status);
  }

  thenUiBlocksCustomerAccess(): void {
    expect(screen.getByTestId('employee-access-denied')).toBeInTheDocument();
  }

  thenUiShowsOrderLines(): void {
    expect(screen.getByText(/Premium Salmon Kibble/)).toBeInTheDocument();
    expect(screen.getByText(/Reflective Dog Leash/)).toBeInTheDocument();
  }

  thenUiShowsPreparationWarning(): void {
    expect(screen.getByTestId('preparation-warning')).toHaveTextContent(
      'preparation is incomplete',
    );
  }

  thenUiShowsOrderComplete(): void {
    expect(screen.getByTestId('order-fulfillment-status')).toHaveTextContent('complete');
    expect(screen.getByTestId('order-collected')).toBeInTheDocument();
  }

  private renderQueue(): void {
    this.container?.remove();
    const view = render(
      <RequireStoreEmployee
        isEmployee={this.isEmployee}
        fallback={
          <p data-testid="employee-access-denied" role="alert">
            fulfillment queue unavailable
          </p>
        }
      >
        <FulfillmentOrdersView
          storeIdentity={this.employeeStore.storeIdentity}
          fulfillmentApi={this.fulfillmentApi}
        />
      </RequireStoreEmployee>,
    );
    this.container = view.container;
  }

  private renderOrderDetail(orderId: string): void {
    this.container?.remove();
    const view = render(
      <RequireStoreEmployee isEmployee={this.isEmployee}>
        <FulfillmentOrderView
          storeIdentity={this.employeeStore.storeIdentity}
          orderId={orderId}
          fulfillmentApi={this.fulfillmentApi}
        />
      </RequireStoreEmployee>,
    );
    this.container = view.container;
  }
}

function withinRow(orderId: string) {
  const row = screen.getByTestId(`queue-row-${orderId}`);
  return {
    getByRole(role: 'button', options: { name: string }) {
      const buttons = row.querySelectorAll('button');
      for (const btn of buttons) {
        if (btn.textContent === options.name) return btn as HTMLButtonElement;
      }
      throw new Error(`button ${options.name} not found in row ${orderId}`);
    },
  };
}
