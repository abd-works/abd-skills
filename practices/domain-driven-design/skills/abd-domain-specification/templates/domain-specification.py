"""
<ka-slug>.py

Source of truth for one Key Abstraction in this module at SPECIFICATION fidelity.
Written by AI or human. Run `domain_graph_cli.py generate` only to bootstrap when
no code exists; NEVER to overwrite. After bootstrap, all edits are made directly.

Naming (mirrors <slug>-stories.ts):
    File            <ka_slug>.py         (snake_case, e.g. customer.py, cart.py)
    Class           PascalCase           (matches the KA name)
    Property        snake_case           (real domain-language terms)
    Operation       snake_case           (verb-noun; name IS the invariant when apt)
    Invariant       snake_case method    (empty; name IS the rule per D24)
    Interaction     snake_case method    (empty; name IS the summary per D24)

Doc-comment tag dictionary (locked — see reference/concepts.md "Code format"):
    @stereotype   on class     Entity | ValueObject | Service | Factory | Repository | DomainEvent | Boundary
    @initialisation on class   constructor | internal | factoryMethod | factoryObject
    @composition / @aggregation / @association on property (in the property's docstring)
    @invariant    on empty method   bare marker; name IS the rule
    @interaction  on empty method   bare marker; name IS the summary

Phase grouping uses "# region … # endregion" banners (D21 — VS Code convention).
Anything the type system carries stays in types. Anything else that is a
structural marker rides in docstrings. Free-text prose lives in sibling
domain-context.md, NOT in docstrings (D1, D14).

Evolution:
    Model fidelity   (abd-domain-model)          real types only; no @stereotype, no invariants, no @composition
    Spec fidelity    (abd-domain-specification)  this template; same file grows in place per D26
"""

from __future__ import annotations
from abc import ABC, abstractmethod

from .scalars import EmailAddress, Password, Keyword, Identifier
from .identity import Identity
from .address import Address
from .cart import Cart
from .subscription import Subscription
from .billing import Billing
from .catalog import NumberOption


# =============================================================================
# KA: KaName
# =============================================================================


class KaName(ABC):
    """
    @stereotype Entity
    @initialisation constructor
    """

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    identity: Identity
    """@composition"""

    address: Address
    """@composition"""

    cart: Cart
    """@composition"""

    billing: Billing
    """@association"""

    subscriptions: list[Subscription]

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    @abstractmethod
    def __init__(self, email: EmailAddress, password: Password) -> None:
        """Bootstrap a KaName. Concrete subclasses implement."""
        ...

    # -------------------------------------------------------------------------
    # region Onboarding operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def search_number(self, keyword: Keyword) -> list[NumberOption]:
        ...

    @abstractmethod
    def select_number(self, phone_number: str) -> Cart:
        ...

    @abstractmethod
    def submit_profile(self, identity: Identity, address: Address) -> None:
        ...

    # endregion

    # -------------------------------------------------------------------------
    # region Self-care operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def select_subscription(self, subscription_id: Identifier) -> Subscription:
        ...

    @abstractmethod
    def update_profile(self, identity: Identity, address: Address) -> None:
        ...

    @abstractmethod
    def pay_outstanding_balance(self) -> None:
        ...

    # endregion

    # -------------------------------------------------------------------------
    # region Invariants — empty methods; the name IS the rule (D24)
    # -------------------------------------------------------------------------

    @abstractmethod
    def keyword_must_be_at_most_five_characters(self) -> None:
        """@invariant"""
        ...

    @abstractmethod
    def msisdn_must_be_reserved_before_cart_advances(self) -> None:
        """@invariant"""
        ...

    @abstractmethod
    def billing_id_must_be_present_in_self_care(self) -> None:
        """@invariant"""
        ...

    # endregion

    # -------------------------------------------------------------------------
    # region Interactions — empty methods; the name IS the summary (D24)
    #
    # Step-by-step narrative does NOT ride in docstrings. When the concrete
    # implementation carries the interaction, add step comments there. When
    # narrative must be preserved at the spec level, put it in
    # domain-context.md at the module folder root.
    # -------------------------------------------------------------------------

    @abstractmethod
    def customer_searches_for_number_during_onboarding(self) -> None:
        """@interaction"""
        ...

    @abstractmethod
    def customer_completes_activation_by_paying(self) -> None:
        """@interaction"""
        ...

    # endregion


# =============================================================================
# KA subtype (delta only; parent members are inherited, not repeated)
# =============================================================================


class EnterpriseKaName(KaName):
    """@stereotype Entity"""

    organization_type: str
    industry: str
