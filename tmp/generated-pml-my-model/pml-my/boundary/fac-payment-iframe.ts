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

}
