"""
<ka_slug>.py

Source of truth for one Key Abstraction at MODEL fidelity.
Written by AI or human. Run `domain_graph_cli.py generate` only to bootstrap
when no code exists; NEVER to overwrite. After bootstrap, edit directly.

Model fidelity is deliberately narrow (D26):
    IN     real types on every property, operation signature, subtype
    OUT    @stereotype, @composition/@aggregation/@association,
           @initialisation, @invariant methods, @interaction methods,
           phase grouping / region banners

Same file evolves upward to specification fidelity by ADDING markers and empty
invariant/interaction methods in place — a new file is not created. See
../../abd-domain-specification/templates/domain-specification.py for the
higher-fidelity shape.

Naming (mirrors <slug>-stories.ts):
    File            <ka_slug>.py         (snake_case, e.g. customer.py)
    Class           PascalCase           (matches the KA name)
    Property        snake_case           (real domain-language terms)
    Operation       snake_case           (verb-noun)
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
    identity: Identity
    address: Address
    cart: Cart
    billing: Billing
    subscriptions: list[Subscription]

    @abstractmethod
    def __init__(self, email: EmailAddress, password: Password) -> None:
        ...

    @abstractmethod
    def search_number(self, keyword: Keyword) -> list[NumberOption]: ...

    @abstractmethod
    def select_number(self, phone_number: str) -> Cart: ...

    @abstractmethod
    def submit_profile(self, identity: Identity, address: Address) -> None: ...

    @abstractmethod
    def select_subscription(self, subscription_id: Identifier) -> Subscription: ...

    @abstractmethod
    def update_profile(self, identity: Identity, address: Address) -> None: ...

    @abstractmethod
    def pay_outstanding_balance(self) -> None: ...


# =============================================================================
# KA subtype (delta only)
# =============================================================================


class EnterpriseKaName(KaName):
    organization_type: str
    industry: str
