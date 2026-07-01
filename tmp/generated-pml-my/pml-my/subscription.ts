// =============================================================================
// KA: Subscription
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   Feature, FreeText, Identifier, Money, PhoneNumber, SIMType, SubscriptionStatus, UsageDimension

export abstract class Subscription {
  abstract id: Identifier
  abstract msisdn: PhoneNumber
  abstract bundle: Bundle
  abstract simType: SIMType
  abstract status: SubscriptionStatus
  abstract usage: Usage

  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: status ≠ active means Usage is inaccessible
  /** @invariant */
  abstract statusActiveMeansUsageIsInaccessible(): void

  //endregion

}

export abstract class Bundle {
  abstract id: Identifier
  abstract name: FreeText
  abstract description: FreeText
  abstract price: Money
  abstract fees: Money
  abstract totalPrice: Money
  abstract features: Feature

}

export abstract class Usage {
  abstract local: UsageDimension
  abstract roaming: UsageDimension

}
