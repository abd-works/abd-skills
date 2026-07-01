// <KaSlug>.java
//
// Source of truth for one Key Abstraction at MODEL fidelity.
// Written by AI or human. Run `domain_graph_cli.py generate` only to bootstrap
// when no code exists; NEVER to overwrite. After bootstrap, edit directly.
//
// Model fidelity is deliberately narrow (D26):
//   IN     real types on every property, operation signature, subtype
//   OUT    @stereotype, @composition/@aggregation/@association,
//          @initialisation, @invariant methods, @interaction methods,
//          phase grouping / region banners
//
// Same file evolves upward to specification fidelity by ADDING markers and
// empty invariant/interaction methods in place — a new file is not created.
// See ../../abd-domain-specification/templates/domain-specification.java for
// the higher-fidelity shape.
//
// Naming (mirrors <slug>-stories.ts):
//   File            <KaName>.java       (PascalCase, e.g. Customer.java)
//   Class           PascalCase          (matches the KA name)
//   Property        camelCase           (real domain-language terms)
//   Operation       camelCase           (verb-noun)

package com.example.<module_slug>.domain;

import java.util.List;

import com.example.<module_slug>.domain.scalars.EmailAddress;
import com.example.<module_slug>.domain.scalars.Password;
import com.example.<module_slug>.domain.scalars.Keyword;
import com.example.<module_slug>.domain.scalars.Identifier;
import com.example.<module_slug>.domain.identity.Identity;
import com.example.<module_slug>.domain.address.Address;
import com.example.<module_slug>.domain.cart.Cart;
import com.example.<module_slug>.domain.subscription.Subscription;
import com.example.<module_slug>.domain.billing.Billing;
import com.example.<module_slug>.domain.catalog.NumberOption;


// =============================================================================
// KA: KaName
// =============================================================================

public abstract class KaName {

    protected Identity identity;
    protected Address address;
    protected Cart cart;
    protected Billing billing;
    protected List<Subscription> subscriptions;

    protected KaName(EmailAddress email, Password password) {
    }

    public abstract List<NumberOption> searchNumber(Keyword keyword);
    public abstract Cart selectNumber(String phoneNumber);
    public abstract void submitProfile(Identity identity, Address address);

    public abstract Subscription selectSubscription(Identifier subscriptionId);
    public abstract void updateProfile(Identity identity, Address address);
    public abstract void payOutstandingBalance();
}
