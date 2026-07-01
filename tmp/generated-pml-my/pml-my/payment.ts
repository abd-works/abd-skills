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
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: on 'success' reply, triggers Transaction status poll; on 'error', increments attempt count
  /** @invariant */
  abstract onSuccessReplyTriggersTransactionStatusPollOnErrorIncrements(): void

  // TODO: rename — original: sequential: POST /billing → POST /order; both must succeed for activation
  /** @invariant */
  abstract sequentialPostBillingPostOrderBothMustSucceedForActivation(): void

  //endregion

}

export abstract class Transaction {
  abstract transactionId: Identifier
  abstract status: TransactionStatus
  abstract reason: FreeText

  abstract pollStatus(): TransactionStatus
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: GET /payment/status/:transactionId; completed is precondition for Order creation
  /** @invariant */
  abstract getPaymentStatusTransactionidCompletedIsPreconditionForOrderCreation(): void

  //endregion

}

export abstract class PaymentAttempt {
  abstract count: number
  abstract maxAttempts: number

  abstract increment(): void
  abstract retry(): void
  abstract handleMaxReached(): void
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: maxAttempts controlled by GrowthBook PAYMENT_ATTEMPTS flag; default 3
  /** @invariant */
  abstract maxattemptsControlledByGrowthbookPaymentAttemptsFlagDefault(): void

  // TODO: rename — original: reloads FAC iframe for another attempt
  /** @invariant */
  abstract reloadsFacIframeForAnotherAttempt(): void

  // TODO: rename — original: POST /payment/failed; navigates to Done with failure state; no further retries permitted
  /** @invariant */
  abstract postPaymentFailedNavigatesToDoneWithFailureStateNo(): void

  //endregion

}
