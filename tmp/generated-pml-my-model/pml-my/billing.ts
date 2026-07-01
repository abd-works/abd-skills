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

}

export abstract class Order {
  abstract verified: boolean
  abstract payUpFront: boolean

  abstract create(arg1: Transaction, arg2: Billing): SelfCareCustomer

}
