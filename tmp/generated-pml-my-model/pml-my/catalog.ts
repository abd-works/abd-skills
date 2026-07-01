// =============================================================================
// KA: Catalog
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   Cart, Feature, FreeText, Identifier, Keyword, Money, PhoneNumber

export abstract class Catalog {
  abstract plans: Plan

  abstract fetch(): Plan
  abstract filter(arg1: Plan): Plan

}

export abstract class Plan {
  abstract id: Identifier
  abstract name: FreeText
  abstract description: FreeText
  abstract price: Money
  abstract fees: Money
  abstract totalPrice: Money
  abstract features: Feature
  abstract isSellable: boolean

}

export abstract class NumberOption {
  abstract msisdn: PhoneNumber

  abstract reserve(arg1: PhoneNumber): Cart
  abstract search(arg1: Keyword): NumberOption

}
