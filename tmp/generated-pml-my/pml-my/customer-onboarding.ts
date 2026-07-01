// =============================================================================
// KA: Customer (Onboarding)
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   AccountType, Billing, Cart, CountryCode, EmailAddress, FreeText, Identifier, IdentityDocumentType, OnboardProgress, Order, PersonName, PhoneNumber, Plan, Portability, PostalCode, SIMType, SelfCareCustomer

export abstract class OnboardingCustomer {
  abstract identity: Identity
  abstract address: Address
  abstract cart: Cart
  abstract metadata: Metadata
  abstract billing: Billing

  abstract selectNumber(arg1: PhoneNumber): Cart
  abstract selectPlan(arg1: Plan): Cart
  abstract selectSim(arg1: SIMType): Cart
  abstract submitProfile(arg1: Identity, arg2: Address): void
  abstract submitPayment(): Order
  abstract activate(arg1: Order): SelfCareCustomer
  abstract portNumber(arg1: Portability): Cart
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: metadata.verified = false — no Order has completed
  /** @invariant */
  abstract metadataVerifiedFalseNoOrderHasCompleted(): void

  // TODO: rename — original: pSIM requires a valid ICCID; eSIM does not
  /** @invariant */
  abstract psimRequiresAValidIccidEsimDoesNot(): void

  // TODO: rename — original: portability.verified = true required before Cart can advance
  /** @invariant */
  abstract portabilityVerifiedTrueRequiredBeforeCartCanAdvance(): void

  // TODO: rename — original: MSISDN must be reserved from inventory before Cart advances
  /** @invariant */
  abstract msisdnMustBeReservedFromInventoryBeforeCartAdvances(): void

  // TODO: rename — original: only Plans with price > 0 and isSellable = true are selectable
  /** @invariant */
  abstract onlyPlansWithPriceAndIssellableTrueAreSelectable(): void

  // TODO: rename — original: Persona KYC inquiry must complete successfully before profile submission
  /** @invariant */
  abstract personaKycInquiryMustCompleteSuccessfullyBeforeProfileSubmission(): void

  // TODO: rename — original: card data never passes through the application
  /** @invariant */
  abstract cardDataNeverPassesThroughTheApplication(): void

  // TODO: rename — original: requires a completed Transaction and an existing Billing account before activation
  /** @invariant */
  abstract requiresACompletedTransactionAndAnExistingBillingAccountBefore(): void

  //endregion

}

export abstract class Identity {
  abstract email: EmailAddress
  abstract name: PersonName
  abstract lastName: PersonName
  abstract fullName: PersonName
  abstract preferredName: PersonName
  abstract dateOfBirth: Date
  abstract idNumber: Identifier
  abstract idType: IdentityDocumentType
  abstract idNationality: CountryCode
  abstract expiryDate: Date
  abstract otherPhoneNumber: PhoneNumber

  abstract update(arg1: Identity): void
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: when account type is Enterprise, identity intersects with EnterpriseIdentity
  /** @invariant */
  abstract whenAccountTypeIsEnterpriseIdentityIntersectsWithEnterpriseidentity(): void

  //endregion

}

export abstract class EnterpriseIdentity extends Identity {
  abstract headOffice: FreeText
  abstract industry: FreeText
  abstract organizationType: FreeText
  abstract status: FreeText

}

export abstract class Address {
  abstract street: FreeText
  abstract complement: FreeText
  abstract city: FreeText
  abstract parish: FreeText
  abstract postalCode: PostalCode
  abstract country: CountryCode

  abstract update(arg1: Address): void
}

export abstract class Metadata {
  abstract id: Identifier
  abstract verified: boolean
  abstract type: AccountType
  abstract onboard: OnboardProgress

  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: verified = false means no Order has completed; route gate checks billing.id
  /** @invariant */
  abstract verifiedFalseMeansNoOrderHasCompletedRouteGateChecks(): void

  //endregion

}
