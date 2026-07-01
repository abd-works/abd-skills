// =============================================================================
// Boundary class: Midtier API
// Owned by: pml-my
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   Address, Billing, Cart, CartSelection, Identifier, Identity, Keyword, NumberOption, OTPCode, OnboardingCustomer, OrderResult, PhoneNumber, Plan, Portability, TransactionStatus

export abstract class Midtier API {
  abstract getCustomer(): OnboardingCustomer
  abstract patchCustomer(arg1: Identity, arg2: Address): void
  abstract createCustomer(): OnboardingCustomer
  abstract patchCart(arg1: CartSelection): Cart
  abstract postBilling(arg1: Identifier): Billing
  abstract postOrder(): OrderResult
  abstract getPaymentStatus(arg1: Identifier): TransactionStatus
  abstract postPaymentFailed(arg1: Identifier): void
  abstract getCatalog(): Plan
  abstract getMsisdnInventory(): NumberOption
  abstract reserveMsisdn(arg1: PhoneNumber): NumberOption
  abstract searchMsisdn(arg1: Keyword): NumberOption
  abstract changePlan(arg1: Identifier, arg2: Identifier): void
  abstract postPortability(arg1: Portability): void
  abstract verifyPortability(arg1: OTPCode): void

}
