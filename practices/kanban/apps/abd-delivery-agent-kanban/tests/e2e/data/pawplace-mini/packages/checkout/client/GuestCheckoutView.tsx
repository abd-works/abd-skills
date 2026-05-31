import { useState } from 'react';
import { layoutTokens } from '../../shared/layout-tokens';
import type { BillingAddressDto, CheckoutSessionDto } from '../shared/src/checkout.types';
import type { CheckoutApi } from './checkout.api';

interface GuestCheckoutViewProps {
  checkoutApi: CheckoutApi;
  initialSession: CheckoutSessionDto;
  onOrderPlaced?(orderId: string): void;
}

export function GuestCheckoutView({
  checkoutApi,
  initialSession,
  onOrderPlaced,
}: GuestCheckoutViewProps) {
  const [session, setSession] = useState(initialSession);
  const [billingDraft, setBillingDraft] = useState<BillingAddressDto>({
    name: '',
    street: '',
    city: '',
    postalCode: '',
    country: '',
  });

  async function refresh(next: CheckoutSessionDto): Promise<void> {
    setSession({ ...next });
  }

  async function selectStore(storeIdentity: string): Promise<void> {
    const next = await checkoutApi.selectClickAndCollectStore(storeIdentity);
    await refresh(next);
  }

  async function submitBilling(): Promise<void> {
    const next = await checkoutApi.enterBillingAddress(billingDraft);
    await refresh(next);
  }

  async function selectPayment(): Promise<void> {
    const next = await checkoutApi.selectPaymentMethod();
    await refresh(next);
  }

  async function placeOrder(): Promise<void> {
    if (session.placeOrderBlocked || session.processingPayment) return;
    setSession((prev) => ({ ...prev, processingPayment: true, validationErrors: [] }));
    const { session: after, confirmation } = await checkoutApi.placeOrder();
    await refresh(after);
    if (confirmation) {
      onOrderPlaced?.(confirmation.orderId);
    }
  }

  return (
    <main data-testid="guest-checkout">
      <h1 style={layoutTokens.display}>Checkout — Guest &amp; pickup</h1>
      {session.guestOnlyLabel ? (
        <p data-testid="guest-only-label">guest-only</p>
      ) : null}

      <section aria-label="pickup store">
        <h2 style={layoutTokens.label}>click-and-collect store</h2>
        <ul role="listbox" aria-label="click-and-collect store">
          {session.eligibleStores.map((store) => {
            const selected =
              session.clickAndCollectStore?.storeIdentity === store.storeIdentity;
            return (
              <li
                key={store.storeIdentity}
                role="option"
                aria-selected={selected}
                style={{
                  background: selected ? layoutTokens.surfaceMuted : layoutTokens.surface,
                  padding: layoutTokens.spacing[2],
                }}
              >
                <button type="button" onClick={() => void selectStore(store.storeIdentity)}>
                  {store.storeIdentity} · {store.storeAddress}
                </button>
              </li>
            );
          })}
        </ul>
        {session.clickAndCollectStore ? (
          <p data-testid="selected-pickup-store">
            {session.clickAndCollectStore.storeIdentity} ·{' '}
            {session.clickAndCollectStore.storeAddress}
          </p>
        ) : null}
      </section>

      <section aria-label="guest checkout">
        <h2 style={layoutTokens.label}>guest checkout</h2>
        <label style={layoutTokens.body}>
          email
          <input
            type="email"
            value={session.email}
            onChange={(e) => void checkoutApi.setGuestEmail(e.target.value).then(refresh)}
          />
        </label>
      </section>

      <section aria-label="billing address">
        <h2 style={layoutTokens.label}>billing address</h2>
        {(['name', 'street', 'city', 'postal code', 'country'] as const).map((field) => {
          const key =
            field === 'postal code'
              ? 'postalCode'
              : (field as keyof BillingAddressDto);
          return (
            <label key={field} style={layoutTokens.body}>
              {field}
              <input
                aria-label={field}
                value={billingDraft[key]}
                onChange={(e) =>
                  setBillingDraft((prev) => ({ ...prev, [key]: e.target.value }))
                }
              />
            </label>
          );
        })}
        <button type="button" onClick={() => void submitBilling()}>
          save billing address
        </button>
      </section>

      <section aria-label="payment method">
        <h2 style={layoutTokens.label}>payment method</h2>
        <p>{session.stripeWaveLabel}</p>
        <button type="button" onClick={() => void selectPayment()}>
          select card via StripeWave
        </button>
        {session.paymentMethodSelected ? (
          <span data-testid="payment-method-selected">payment method selected</span>
        ) : null}
      </section>

      {(session.validationErrors.length > 0 || session.paymentFailureMessage) && (
        <div
          data-testid="validation-error-area"
          role="alert"
          style={{ color: layoutTokens.danger }}
        >
          {session.validationErrors.join('; ')}
          {session.paymentFailureMessage}
        </div>
      )}

      <div style={{ marginTop: layoutTokens.spacing[2] }}>
        <button type="button">back to cart</button>
        <button
          type="button"
          style={{ color: layoutTokens.accent, marginLeft: layoutTokens.spacing[2] }}
          disabled={session.placeOrderBlocked || session.processingPayment}
          aria-disabled={session.placeOrderBlocked || session.processingPayment}
          aria-busy={session.processingPayment}
          onClick={() => void placeOrder()}
        >
          place order
        </button>
      </div>
    </main>
  );
}
