/**
 * Checkout & pay — client-tier helper.
 */
import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect } from 'vitest';
import {
  GuestCheckoutView,
  InMemoryCheckoutApi,
  OrderConfirmationView,
} from '@pawplace-mini/checkout-client';
import type { BillingAddressTestData, StoreTestData } from './checkout.base';
import { CheckoutBaseHelper } from './checkout.base';

export class CheckoutClientHelper extends CheckoutBaseHelper {
  private checkoutApi = new InMemoryCheckoutApi();
  private container: HTMLElement | null = null;
  private lastOrderId: string | null = null;

  async cleanup(): Promise<void> {
    this.container?.remove();
    this.container = null;
    this.checkoutApi.reset();
    this.lastOrderId = null;
  }

  async givenGuestCheckoutFromNonEmptyCart(): Promise<void> {
    this.checkoutApi.reset(43.49);
  }

  async givenNoClickAndCollectStoreSelected(): Promise<void> {
    // default session has no store
  }

  async givenClickAndCollectStoreSelected(store: StoreTestData): Promise<void> {
    await this.checkoutApi.selectClickAndCollectStore(store.storeIdentity);
  }

  async givenValidBillingAndPaymentSelected(store: StoreTestData): Promise<void> {
    await this.checkoutApi.selectClickAndCollectStore(store.storeIdentity);
    await this.checkoutApi.setGuestEmail(CheckoutBaseHelper.GUEST_EMAIL);
    await this.checkoutApi.enterBillingAddress(CheckoutBaseHelper.BILLING_VALID);
    await this.checkoutApi.selectPaymentMethod();
  }

  async givenStripeWaveWillDecline(): Promise<void> {
    this.checkoutApi.setStripeWaveOutcome('card declined');
  }

  async whenCustomerOpensGuestCheckout(): Promise<void> {
    this.renderCheckout(this.checkoutApi.getSession());
  }

  async whenCustomerSelectsClickAndCollectStore(store: StoreTestData): Promise<void> {
    this.renderCheckout(this.checkoutApi.getSession());
    await userEvent.click(
      screen.getByRole('button', {
        name: new RegExp(store.storeIdentity),
      }),
    );
    this.renderCheckout(this.checkoutApi.getSession());
  }

  async whenCustomerEntersBillingAddress(address: BillingAddressTestData): Promise<void> {
    this.renderCheckout(this.checkoutApi.getSession());
    fireEvent.change(screen.getByLabelText('name'), { target: { value: address.name } });
    fireEvent.change(screen.getByLabelText('street'), { target: { value: address.street } });
    fireEvent.change(screen.getByLabelText('city'), { target: { value: address.city } });
    fireEvent.change(screen.getByLabelText('postal code'), {
      target: { value: address.postalCode },
    });
    fireEvent.change(screen.getByLabelText('country'), { target: { value: address.country } });
    await userEvent.click(screen.getByRole('button', { name: 'save billing address' }));
    await this.checkoutApi.enterBillingAddress(address);
    this.renderCheckout(this.checkoutApi.getSession());
  }

  async whenCustomerSelectsPaymentMethod(): Promise<void> {
    this.renderCheckout(this.checkoutApi.getSession());
    await userEvent.click(screen.getByRole('button', { name: 'select card via StripeWave' }));
    this.renderCheckout(this.checkoutApi.getSession());
  }

  async whenCustomerClicksPlaceOrder(): Promise<void> {
    this.renderCheckout(this.checkoutApi.getSession());
    const btn = screen.getByRole('button', { name: 'place order' });
    if (!btn.hasAttribute('disabled')) {
      await userEvent.click(btn);
    }
    this.renderCheckout(this.checkoutApi.getSession());
  }

  async whenCustomerViewsOrderConfirmation(): Promise<void> {
    const confirmation = this.checkoutApi.getLastConfirmation();
    if (!confirmation) throw new Error('no confirmation');
    this.container?.remove();
    const view = render(<OrderConfirmationView confirmation={confirmation} />);
    this.container = view.container;
  }

  thenUiShowsAllEligibleStores(): void {
    expect(screen.getByRole('listbox', { name: 'click-and-collect store' })).toBeInTheDocument();
    expect(screen.getByText(/Downtown PawPlace/)).toBeInTheDocument();
    expect(screen.getByText(/Westside PawPlace/)).toBeInTheDocument();
    expect(screen.getByText(/Uptown PawPlace/)).toBeInTheDocument();
  }

  thenUiShowsBoundStore(store: StoreTestData): void {
    const selected = screen.getByTestId('selected-pickup-store');
    expect(selected.textContent).toContain(store.storeIdentity);
    expect(selected.textContent).toContain(store.storeAddress);
  }

  thenUiBlocksPlaceOrder(): void {
    expect(screen.getByRole('button', { name: 'place order' })).toBeDisabled();
  }

  thenUiShowsGuestOnlyLabel(): void {
    expect(screen.getByTestId('guest-only-label')).toHaveTextContent('guest-only');
  }

  thenUiShowsBillingFieldErrors(): void {
    expect(screen.getByTestId('validation-error-area')).toBeInTheDocument();
  }

  thenUiShowsPaymentMethodSelected(): void {
    expect(screen.getByTestId('payment-method-selected')).toBeInTheDocument();
  }

  thenUiShowsPaymentFailure(): void {
    expect(screen.getByTestId('validation-error-area').textContent).toContain('card declined');
  }

  thenUiShowsOrderConfirmation(orderId: string, store: StoreTestData, total: string): void {
    expect(screen.getByTestId('order-id')).toHaveTextContent(orderId);
    expect(screen.getByTestId('order-store')).toHaveTextContent(store.storeIdentity);
    expect(screen.getByTestId('order-total')).toHaveTextContent(total);
    expect(screen.getByTestId('order-confirmation-sent').textContent).toContain(
      CheckoutBaseHelper.GUEST_EMAIL,
    );
  }

  private renderCheckout(session: ReturnType<InMemoryCheckoutApi['getSession']>): void {
    this.container?.remove();
    const view = render(
      <GuestCheckoutView
        checkoutApi={this.checkoutApi}
        initialSession={session}
        onOrderPlaced={(id) => {
          this.lastOrderId = id;
        }}
      />,
    );
    this.container = view.container;
  }
}
