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

}
