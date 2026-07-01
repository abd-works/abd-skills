// =============================================================================
// KA: Cart
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   CarrierName, CartSelection, Discount, FreeText, Identifier, OTPCode, PhoneNumber, Plan, SIMType, VoucherCode

export abstract class Cart {
  abstract id: Identifier
  abstract msisdn: PhoneNumber
  abstract bundle: Plan
  abstract simType: SIMType
  abstract iccid: Identifier
  abstract portability: Portability

  abstract patchNumber(arg1: PhoneNumber): Cart
  abstract patchPlan(arg1: Plan): Cart
  abstract patchSim(arg1: SIMType, arg2: Identifier): Cart
  abstract patch(arg1: CartSelection): Cart
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: writes msisdn from reserved NumberOption or verified Portability
  /** @invariant */
  abstract writesMsisdnFromReservedNumberoptionOrVerifiedPortability(): void

  // TODO: rename — original: extracts bundleId from Plan; merges with existing cart state
  /** @invariant */
  abstract extractsBundleidFromPlanMergesWithExistingCartState(): void

  // TODO: rename — original: pSIM requires valid iccid; eSIM ignores iccid
  /** @invariant */
  abstract psimRequiresValidIccidEsimIgnoresIccid(): void

  // TODO: rename — original: after Order creation, Cart is stale — selections superseded by Subscription
  /** @invariant */
  abstract afterOrderCreationCartIsStaleSelectionsSupersededBySubscription(): void

  //endregion

}

export abstract class Portability {
  abstract donorOperator: CarrierName
  abstract accountNumber: Identifier
  abstract portNumber: PhoneNumber
  abstract userType: FreeText
  abstract accountType: FreeText
  abstract device: FreeText
  abstract planSelected: FreeText
  abstract verified: boolean

  abstract submit(arg1: Portability): void
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: verified = true required before Cart can advance past LineNumber step
  /** @invariant */
  abstract verifiedTrueRequiredBeforeCartCanAdvancePastLinenumberStep(): void

  // TODO: rename — original: calls POST /portability with donor details
  /** @invariant */
  abstract callsPostPortabilityWithDonorDetails(): void

  //endregion

}

export abstract class PortabilityVerification {
  abstract verify(arg1: OTPCode): void
  abstract resend(): void
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: triggered only when PORTING_2FA flag is enabled; when disabled, Portability proceeds without SMS
  /** @invariant */
  abstract triggeredOnlyWhenPortingFaFlagIsEnabledWhenDisabled(): void

  // TODO: rename — original: re-sends verification code to the port number
  /** @invariant */
  abstract reSendsVerificationCodeToThePortNumber(): void

  //endregion

}

export abstract class Voucher {
  abstract code: VoucherCode
  abstract discount: Discount
  abstract valid: boolean

  abstract validate(arg1: VoucherCode): Voucher
  abstract apply(arg1: Cart): Cart
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: applies discount to Cart total at checkout; reverts on invalid
  /** @invariant */
  abstract appliesDiscountToCartTotalAtCheckoutRevertsOnInvalid(): void

  //endregion

}
