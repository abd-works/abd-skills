// <ka-slug>.ts
//
// Source of truth for one Key Abstraction in this module at SPECIFICATION fidelity.
// Written by AI or human. Run `domain_graph_cli.py generate` only to bootstrap when
// no code exists; NEVER to overwrite. After bootstrap, all edits are made directly.
//
// Naming (mirrors <slug>-stories.ts):
//   File            <ka-slug>.ts       (e.g. customer.ts, cart.ts)
//   Class           PascalCase         (matches the KA name)
//   Property        camelCase          (real domain-language terms)
//   Operation       camelCase          (verb-noun; name IS the invariant when apt)
//   Invariant       camelCase method   (empty; name IS the rule per D24)
//   Interaction     camelCase method   (empty; name IS the summary per D24)
//
// Doc-comment tag dictionary (locked — see reference/concepts.md "Code format"):
//   @stereotype   on class     Entity | ValueObject | Service | Factory | Repository | DomainEvent | Boundary
//   @initialisation on class   constructor | internal | factoryMethod | factoryObject
//   @composition / @aggregation / @association on property
//   @invariant    on empty method   bare marker; name IS the rule
//   @interaction  on empty method   bare marker; name IS the summary
//
// Phase grouping uses //region … //endregion banners (D21).
// Anything the type system carries stays in types. Anything else that is a
// structural marker rides in doc comments. Free-text prose lives in
// sibling domain-context.md, NOT in doc comments (D1, D14).
//
// Evolution:
//   Model fidelity   (abd-domain-model)          → real types only; no @stereotype, no invariants, no @composition
//   Spec fidelity    (abd-domain-specification)  → this template; same file grows in place per D26

import type { EmailAddress, Password, Keyword, Identifier } from './scalars'
import type { Identity } from './identity'
import type { Address } from './address'
import type { Cart } from './cart'
import type { Subscription } from './subscription'
import type { Billing } from './billing'
import type { NumberOption } from './catalog'

// =============================================================================
// KA: KaName
// =============================================================================

/**
 * @stereotype Entity
 * @initialisation constructor
 */
export abstract class KaName {
  // ---------------------------------------------------------------------------
  // Properties
  // ---------------------------------------------------------------------------

  /** @composition */
  abstract identity: Identity

  /** @composition */
  abstract address: Address

  /** @composition */
  abstract cart: Cart

  /** @association */
  abstract billing: Billing

  abstract subscriptions: Subscription[]

  // ---------------------------------------------------------------------------
  // Constructor
  // ---------------------------------------------------------------------------

  constructor(email: EmailAddress, password: Password) {
    // Empty at the specification level. Concrete subclasses implement.
    void email
    void password
  }

  // ---------------------------------------------------------------------------
  // region Onboarding operations
  // ---------------------------------------------------------------------------

  abstract searchNumber(keyword: Keyword): NumberOption[]

  abstract selectNumber(phoneNumber: string): Cart

  abstract submitProfile(identity: Identity, address: Address): void

  // endregion

  // ---------------------------------------------------------------------------
  // region Self-care operations
  // ---------------------------------------------------------------------------

  abstract selectSubscription(subscriptionId: Identifier): Subscription

  abstract updateProfile(identity: Identity, address: Address): void

  abstract payOutstandingBalance(): void

  // endregion

  // ---------------------------------------------------------------------------
  // region Invariants — empty methods; the name IS the rule (D24)
  // ---------------------------------------------------------------------------

  /** @invariant */
  abstract keywordMustBeAtMostFiveCharacters(): void

  /** @invariant */
  abstract msisdnMustBeReservedBeforeCartAdvances(): void

  /** @invariant */
  abstract billingIdMustBePresentInSelfCare(): void

  // endregion

  // ---------------------------------------------------------------------------
  // region Interactions — empty methods; the name IS the summary (D24)
  //
  // Step-by-step narrative does NOT ride in doc comments. When the concrete
  // implementation carries the interaction, add step comments there. When
  // narrative must be preserved at the spec level, put it in
  // domain-context.md at the module folder root.
  // ---------------------------------------------------------------------------

  /** @interaction */
  abstract customerSearchesForNumberDuringOnboarding(): void

  /** @interaction */
  abstract customerCompletesActivationByPaying(): void

  // endregion
}

// =============================================================================
// KA subtype (delta only; parent members are inherited, not repeated)
// =============================================================================

/** @stereotype Entity */
export abstract class EnterpriseKaName extends KaName {
  // Delta properties only — inherited members from KaName are not restated.
  abstract organizationType: string
  abstract industry: string
}
