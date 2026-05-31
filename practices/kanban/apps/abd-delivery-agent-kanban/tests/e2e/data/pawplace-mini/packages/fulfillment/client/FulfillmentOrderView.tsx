import { useState } from 'react';
import { layoutTokens } from '../../shared/layout-tokens';
import { EmployeeNav } from '../../inventory/client/EmployeeNav';
import type { FulfillmentOrderDetailDto } from '../shared/src/fulfillment.types';
import type { FulfillmentApi } from './fulfillment.api';
import { EMPLOYEE_ACCENT } from './fulfillment.api';

interface FulfillmentOrderViewProps {
  storeIdentity: string;
  orderId: string;
  fulfillmentApi: FulfillmentApi;
  onBackToQueue?(): void;
}

export function FulfillmentOrderView({
  storeIdentity,
  orderId,
  fulfillmentApi,
  onBackToQueue,
}: FulfillmentOrderViewProps) {
  const initial = fulfillmentApi.getOrder(orderId);
  const [order, setOrder] = useState<FulfillmentOrderDetailDto | null>(initial);
  const [warning, setWarning] = useState<string | null>(
    initial?.orderFulfillment === 'awaiting preparation'
      ? 'preparation is incomplete'
      : null,
  );

  const canFulfill = order?.orderFulfillment === 'ready for collection';
  const isComplete =
    order?.orderFulfillment === 'complete' ||
    order?.orderFulfillment === 'collected' ||
    order?.orderFulfillment === 'closed';

  async function fulfill(): Promise<void> {
    if (!order) return;
    if (order.orderFulfillment === 'awaiting preparation') {
      setWarning('preparation is incomplete');
      return;
    }
    if (isComplete) return;
    const next = fulfillmentApi.fulfillOrder(orderId);
    if (next) {
      setOrder({ ...next });
      setWarning(null);
    }
  }

  if (!order) {
    return (
      <main data-testid="fulfillment-order-missing">
        <p role="alert">order not found</p>
      </main>
    );
  }

  return (
    <main data-testid="fulfillment-order">
      <EmployeeNav storeIdentity={storeIdentity} activeSection="Fulfillment" />
      <h1 style={layoutTokens.display}>Fulfillment — Order</h1>
      <section aria-label="order detail" data-testid="order-detail">
        <dl>
          <dt>order id</dt>
          <dd>{order.orderId}</dd>
          <dt>click-and-collect store</dt>
          <dd>{order.clickAndCollectStore}</dd>
          <dt>order fulfillment</dt>
          <dd data-testid="order-fulfillment-status">{order.orderFulfillment}</dd>
        </dl>
        <ul aria-label="product lines">
          {order.cartLines.map((line) => (
            <li key={line.catalogItemIdentity}>
              {line.catalogItemIdentity} · cart quantity {line.cartQuantity}
            </li>
          ))}
        </ul>
      </section>
      {warning ? (
        <p role="alert" data-testid="preparation-warning" aria-describedby="fulfill-action">
          {warning}
        </p>
      ) : null}
      <div>
        <button type="button" onClick={onBackToQueue}>
          back to queue
        </button>
        <button
          id="fulfill-action"
          type="button"
          style={{ color: EMPLOYEE_ACCENT, marginLeft: layoutTokens.spacing[2] }}
          disabled={!canFulfill || isComplete}
          aria-disabled={!canFulfill || isComplete}
          onClick={() => void fulfill()}
        >
          fulfill click-and-collect order
        </button>
      </div>
      {isComplete ? (
        <p data-testid="order-collected">collected</p>
      ) : null}
    </main>
  );
}
