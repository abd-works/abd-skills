// =============================================================================
// KA: Customer (Self-Care)
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   Address, Billing, Cart, Identifier, Identity, Metadata, Order, PaymentMethod, Plan, Portability, Subscription

export abstract class SelfCareCustomer {
  abstract identity: Identity
  abstract address: Address
  abstract subscriptions: Subscription
  abstract billing: Billing
  abstract metadata: Metadata
  abstract cart: Cart

  abstract selectSubscription(arg1: Identifier): Subscription
  abstract changePlan(arg1: Plan): Order
  abstract updateProfile(arg1: Identity, arg2: Address): void
  abstract updatePaymentMethod(): PaymentMethod
  abstract payOutstandingBalance(): void
  abstract submitPortability(arg1: Portability): void

}
