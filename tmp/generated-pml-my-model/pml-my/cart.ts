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

}

export abstract class PortabilityVerification {
  abstract verify(arg1: OTPCode): void
  abstract resend(): void

}

export abstract class Voucher {
  abstract code: VoucherCode
  abstract discount: Discount
  abstract valid: boolean

  abstract validate(arg1: VoucherCode): Voucher
  abstract apply(arg1: Cart): Cart

}
