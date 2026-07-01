// =============================================================================
// Boundary class: FAC Payment Iframe
// Owned by: pml-my
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   IframeHtml

export abstract class FAC Payment Iframe {
  abstract load(): IframeHtml
  abstract submitForm(): void
  abstract onSuccess(): void
  abstract onError(): void
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: GET /payment/auth returns HTML rendered as iframe srcdoc
  /** @invariant */
  abstract getPaymentAuthReturnsHtmlRenderedAsIframeSrcdoc(): void

  // TODO: rename — original: parent sends postMessage('submitForm', '*'); no origin restriction
  /** @invariant */
  abstract parentSendsPostmessageSubmitformNoOriginRestriction(): void

  // TODO: rename — original: card data never leaves the FAC iframe; application never handles raw card numbers
  /** @invariant */
  abstract cardDataNeverLeavesTheFacIframeApplicationNeverHandles(): void

  //endregion

}
