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
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: billing.id must be present (route gate: `!!customer?.billing?.id`)
  /** @invariant */
  abstract billingIdMustBePresentRouteGateCustomerBillingId(): void

  // TODO: rename — original: metadata.verified = true — Order has completed
  /** @invariant */
  abstract metadataVerifiedTrueOrderHasCompleted(): void

  // TODO: rename — original: switches active line in multi-subscription accounts
  /** @invariant */
  abstract switchesActiveLineInMultiSubscriptionAccounts(): void

  // TODO: rename — original: patchCustomer PATCH merges payload optimistically into customerAtom
  /** @invariant */
  abstract patchcustomerPatchMergesPayloadOptimisticallyIntoCustomeratom(): void

  // TODO: rename — original: porting an additional number onto the account
  /** @invariant */
  abstract portingAnAdditionalNumberOntoTheAccount(): void

  // TODO: rename — original: uses same FAC iframe mechanism as onboarding; afterPaymentGoToAtom routes back
  /** @invariant */
  abstract usesSameFacIframeMechanismAsOnboardingAfterpaymentgotoatomRoutesBack(): void

  // TODO: rename — original: settles current billing.balance via card charge
  /** @invariant */
  abstract settlesCurrentBillingBalanceViaCardCharge(): void

  //endregion

}
