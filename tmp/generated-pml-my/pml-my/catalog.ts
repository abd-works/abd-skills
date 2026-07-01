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
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: fetched once per session (staleTime: Infinity); unauthenticated; cached in TanStack Query
  /** @invariant */
  abstract fetchedOncePerSessionStaletimeInfinityUnauthenticatedCachedInTanstack(): void

  // TODO: rename — original: only Plans with price > 0 and name not containing ' PROMO' suffix are presented
  /** @invariant */
  abstract onlyPlansWithPriceAndNameNotContainingPromoSuffix(): void

  //endregion

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

  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: price > 0 and isSellable = true to appear in the Catalog
  /** @invariant */
  abstract priceAndIssellableTrueToAppearInTheCatalog(): void

  //endregion

}

export abstract class NumberOption {
  abstract msisdn: PhoneNumber

  abstract reserve(arg1: PhoneNumber): Cart
  abstract search(arg1: Keyword): NumberOption
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: POST to inventory/msisdn reserves the number; writes msisdn to Cart
  /** @invariant */
  abstract postToInventoryMsisdnReservesTheNumberWritesMsisdnTo(): void

  // TODO: rename — original: Keyword is up to 5 characters; searches available MSISDN inventory
  /** @invariant */
  abstract keywordIsUpToCharactersSearchesAvailableMsisdnInventory(): void

  //endregion

}
