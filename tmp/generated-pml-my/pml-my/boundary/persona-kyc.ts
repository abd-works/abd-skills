// =============================================================================
// Boundary class: Persona KYC
// Owned by: pml-my
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   Identifier, InquiryId, PersonaDocument, VerifiedIdentityFields

export abstract class Persona KYC {
  abstract startInquiry(): InquiryId
  abstract onComplete(): VerifiedIdentityFields
  abstract fetchDocument(arg1: Identifier): PersonaDocument
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: inquiry must complete successfully before profile submission
  /** @invariant */
  abstract inquiryMustCompleteSuccessfullyBeforeProfileSubmission(): void

  // TODO: rename — original: retrieves ID document data for expiry date mapping
  /** @invariant */
  abstract retrievesIdDocumentDataForExpiryDateMapping(): void

  //endregion

}
