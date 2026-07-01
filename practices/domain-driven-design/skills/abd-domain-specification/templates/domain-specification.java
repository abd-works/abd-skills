// <KaSlug>.java
//
// Source of truth for one Key Abstraction in this module at SPECIFICATION fidelity.
// Written by AI or human. Run `domain_graph_cli.py generate` only to bootstrap when
// no code exists; NEVER to overwrite. After bootstrap, all edits are made directly.
//
// Naming (mirrors <slug>-stories.ts):
//   File            <KaName>.java       (PascalCase, e.g. Customer.java, Cart.java)
//   Class           PascalCase          (matches the KA name)
//   Property        camelCase           (real domain-language terms)
//   Operation       camelCase           (verb-noun; name IS the invariant when apt)
//   Invariant       camelCase method    (empty; name IS the rule per D24)
//   Interaction     camelCase method    (empty; name IS the summary per D24)
//
// Doc-comment tag dictionary (locked — see reference/concepts.md "Code format"):
//   @stereotype   on class     Entity | ValueObject | Service | Factory | Repository | DomainEvent | Boundary
//   @initialisation on class   constructor | internal | factoryMethod | factoryObject
//   @composition / @aggregation / @association on field (in the field's Javadoc)
//   @invariant    on empty method   bare marker; name IS the rule
//   @interaction  on empty method   bare marker; name IS the summary
//
// Phase grouping uses "//region … //endregion" banners (D21 — IntelliJ / IDE convention).
// Anything the type system carries stays in types. Anything else that is a
// structural marker rides in Javadoc. Free-text prose lives in sibling
// domain-context.md, NOT in Javadoc (D1, D14).
//
// Evolution:
//   Model fidelity   (abd-domain-model)          real types only; no @stereotype, no invariants, no @composition
//   Spec fidelity    (abd-domain-specification)  this template; same file grows in place per D26

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

/**
 * @stereotype Entity
 * @initialisation constructor
 */
public abstract class KaName {

    // -------------------------------------------------------------------------
    // Properties
    // -------------------------------------------------------------------------

    /** @composition */
    protected Identity identity;

    /** @composition */
    protected Address address;

    /** @composition */
    protected Cart cart;

    /** @association */
    protected Billing billing;

    protected List<Subscription> subscriptions;

    // -------------------------------------------------------------------------
    // Constructor
    // -------------------------------------------------------------------------

    protected KaName(EmailAddress email, Password password) {
        // Empty at the specification level. Concrete subclasses complete init.
    }

    // -------------------------------------------------------------------------
    //region Onboarding operations
    // -------------------------------------------------------------------------

    public abstract List<NumberOption> searchNumber(Keyword keyword);

    public abstract Cart selectNumber(String phoneNumber);

    public abstract void submitProfile(Identity identity, Address address);

    //endregion

    // -------------------------------------------------------------------------
    //region Self-care operations
    // -------------------------------------------------------------------------

    public abstract Subscription selectSubscription(Identifier subscriptionId);

    public abstract void updateProfile(Identity identity, Address address);

    public abstract void payOutstandingBalance();

    //endregion

    // -------------------------------------------------------------------------
    //region Invariants — empty methods; the name IS the rule (D24)
    // -------------------------------------------------------------------------

    /** @invariant */
    public abstract void keywordMustBeAtMostFiveCharacters();

    /** @invariant */
    public abstract void msisdnMustBeReservedBeforeCartAdvances();

    /** @invariant */
    public abstract void billingIdMustBePresentInSelfCare();

    //endregion

    // -------------------------------------------------------------------------
    //region Interactions — empty methods; the name IS the summary (D24)
    //
    // Step-by-step narrative does NOT ride in Javadoc. When the concrete
    // implementation carries the interaction, add step comments there. When
    // narrative must be preserved at the spec level, put it in
    // domain-context.md at the module folder root.
    // -------------------------------------------------------------------------

    /** @interaction */
    public abstract void customerSearchesForNumberDuringOnboarding();

    /** @interaction */
    public abstract void customerCompletesActivationByPaying();

    //endregion
}
