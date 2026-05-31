import { layoutTokens } from '../../shared/layout-tokens';
import type { OrderConfirmationDto } from '../shared/src/checkout.types';

interface OrderConfirmationViewProps {
  confirmation: OrderConfirmationDto;
  onContinueShopping?(): void;
}

export function OrderConfirmationView({
  confirmation,
  onContinueShopping,
}: OrderConfirmationViewProps) {
  return (
    <main data-testid="order-confirmation">
      <h1 style={layoutTokens.display}>Order Confirmation</h1>
      <section aria-label="order summary" data-testid="order-summary">
        <dl>
          <dt>order id</dt>
          <dd data-testid="order-id">{confirmation.orderId}</dd>
          <dt>click-and-collect store</dt>
          <dd data-testid="order-store">{confirmation.clickAndCollectStore}</dd>
          <dt>total</dt>
          <dd data-testid="order-total">${confirmation.total.toFixed(2)}</dd>
          <dt>order confirmation</dt>
          <dd data-testid="order-confirmation-sent">
            {confirmation.orderConfirmationSent
              ? `order confirmation sent to ${confirmation.emailSentTo}`
              : 'pending'}
          </dd>
        </dl>
      </section>
      <button
        type="button"
        style={{ color: layoutTokens.accent }}
        onClick={onContinueShopping}
      >
        continue shopping
      </button>
    </main>
  );
}
