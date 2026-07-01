// =============================================================================
// KA: Billing
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   CardBrand, CardDigits, Identifier, InvoiceStatus, Money, PaymentMethodStatus, SelfCareCustomer, Transaction, TransactionId

export abstract class Billing {
  abstract id: Identifier
  abstract balance: Money
  abstract invoices: Invoice
  abstract defaultPayment: PaymentMethod
  abstract transactions: Transaction

  abstract create(arg1: TransactionId): Billing
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: a Billing account exists if and only if at least one Order has been successfully created
  /** @invariant */
  abstract aBillingAccountExistsIfAndOnlyIfAtLeast(): void

  // TODO: rename — original: POST /billing with transactionId; creates billing.id — the route gate for Self-Care access
  /** @invariant */
  abstract postBillingWithTransactionidCreatesBillingIdTheRouteGate(): void

  //endregion

}

export abstract class Invoice {
  abstract invoiceId: Identifier
  abstract billDate: Date
  abstract dueDate: Date
  abstract dueAmount: Money
  abstract status: InvoiceStatus

}

export abstract class PaymentMethod {
  abstract id: Identifier
  abstract brand: CardBrand
  abstract lastFourDigits: CardDigits
  abstract status: PaymentMethodStatus

  abstract update(): PaymentMethod
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: must be present before recurring charges can be collected
  /** @invariant */
  abstract mustBePresentBeforeRecurringChargesCanBeCollected(): void

  // TODO: rename — original: uses same iframe mechanism as onboarding Payment; afterPaymentGoToAtom routes back
  /** @invariant */
  abstract usesSameIframeMechanismAsOnboardingPaymentAfterpaymentgotoatomRoutesBack(): void

  //endregion

}

export abstract class Order {
  abstract verified: boolean
  abstract payUpFront: boolean

  abstract create(arg1: Transaction, arg2: Billing): SelfCareCustomer
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: requires a completed Transaction and existing Billing account
  /** @invariant */
  abstract requiresACompletedTransactionAndExistingBillingAccount(): void

  //endregion

}
