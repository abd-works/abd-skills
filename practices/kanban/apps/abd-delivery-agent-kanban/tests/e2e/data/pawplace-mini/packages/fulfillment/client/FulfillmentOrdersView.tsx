import { useState } from 'react';
import { layoutTokens } from '../../shared/layout-tokens';
import { EmployeeNav } from '../../inventory/client/EmployeeNav';
import type { FulfillmentApi } from './fulfillment.api';
import { EMPLOYEE_ACCENT } from './fulfillment.api';

interface FulfillmentOrdersViewProps {
  storeIdentity: string;
  fulfillmentApi: FulfillmentApi;
  onOpenOrder?(orderId: string): void;
}

export function FulfillmentOrdersView({
  storeIdentity,
  fulfillmentApi,
  onOpenOrder,
}: FulfillmentOrdersViewProps) {
  const [rows, setRows] = useState(() => fulfillmentApi.listQueue(storeIdentity));

  function refresh(): void {
    setRows([...fulfillmentApi.listQueue(storeIdentity)]);
  }

  async function markPreparing(orderId: string): Promise<void> {
    fulfillmentApi.markPreparing(orderId);
    refresh();
  }

  return (
    <main data-testid="fulfillment-orders">
      <EmployeeNav storeIdentity={storeIdentity} activeSection="Fulfillment" />
      <h1 style={layoutTokens.display}>Fulfillment — Orders</h1>
      {rows.length === 0 ? (
        <p data-testid="empty-queue">no orders in fulfillment queue</p>
      ) : (
        <table aria-label="order queue" data-testid="order-queue">
          <thead>
            <tr>
              <th scope="col">order id</th>
              <th scope="col">customer</th>
              <th scope="col">status</th>
              <th scope="col">pickup time</th>
              <th scope="col">
                <span className="sr-only">actions</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.orderId} data-testid={`queue-row-${row.orderId}`}>
                <td>{row.orderId}</td>
                <td>{row.customerContact}</td>
                <td data-testid={`status-${row.orderId}`}>{row.orderFulfillment}</td>
                <td>{row.pickupTime}</td>
                <td>
                  <button type="button" onClick={() => onOpenOrder?.(row.orderId)}>
                    open order
                  </button>
                  <button
                    type="button"
                    style={{ color: EMPLOYEE_ACCENT, marginLeft: layoutTokens.spacing[1] }}
                    onClick={() => void markPreparing(row.orderId)}
                  >
                    mark preparing
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
