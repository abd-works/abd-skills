// =============================================================================
// KA: Payment
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   FreeText, Identifier, IframeHtml, IframeReply, SelfCareCustomer, TransactionStatus

export abstract class Payment {
  abstract loadIframe(): IframeHtml
  abstract submit(): void
  abstract onIframeReply(arg1: IframeReply): void
  abstract createOrder(): SelfCareCustomer

}

export abstract class Transaction {
  abstract transactionId: Identifier
  abstract status: TransactionStatus
  abstract reason: FreeText

  abstract pollStatus(): TransactionStatus

}

export abstract class PaymentAttempt {
  abstract count: number
  abstract maxAttempts: number

  abstract increment(): void
  abstract retry(): void
  abstract handleMaxReached(): void

}
