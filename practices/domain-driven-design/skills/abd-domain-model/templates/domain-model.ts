// <ka-slug>.ts
//
// Source of truth for one Key Abstraction at MODEL fidelity.
// Written by AI or human. Run `domain_graph_cli.py generate` only to bootstrap
// when no code exists; NEVER to overwrite. After bootstrap, edit directly.
//
// Model fidelity is deliberately narrow (D26):
//   IN         real types on every property, operation signature, subtype
//   OUT        @stereotype, @composition/@aggregation/@association,
//              @initialisation, @invariant methods, @interaction methods,
//              phase grouping / region banners
//
// Same file evolves upward to specification fidelity by ADDING markers and
// empty invariant/interaction methods in place — a new file is not created.
// See ../../abd-domain-specification/templates/domain-specification.ts for the
// higher-fidelity shape.
//
// Naming (mirrors <slug>-stories.ts):
//   File            <ka-slug>.ts       (e.g. customer.ts, cart.ts)
//   Class           PascalCase         (matches the KA name)
//   Property        camelCase          (real domain-language terms)
//   Operation       camelCase          (verb-noun)

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

export abstract class KaName {
  abstract identity: Identity
  abstract address: Address
  abstract cart: Cart
  abstract billing: Billing
  abstract subscriptions: Subscription[]

  constructor(email: EmailAddress, password: Password) {
    void email
    void password
  }

  abstract searchNumber(keyword: Keyword): NumberOption[]
  abstract selectNumber(phoneNumber: string): Cart
  abstract submitProfile(identity: Identity, address: Address): void

  abstract selectSubscription(subscriptionId: Identifier): Subscription
  abstract updateProfile(identity: Identity, address: Address): void
  abstract payOutstandingBalance(): void
}

// =============================================================================
// KA subtype (delta only)
// =============================================================================

export abstract class EnterpriseKaName extends KaName {
  abstract organizationType: string
  abstract industry: string
}
