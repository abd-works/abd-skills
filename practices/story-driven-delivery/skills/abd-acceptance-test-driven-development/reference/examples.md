# Acceptance Tests — Example and Shape

## Example: Place Order tests (Python/pytest)

```python
"""
Place Order Tests

Tests for 'Place Order' behavior — user selects items and submits an order.
Scenarios: order placed successfully, empty cart rejected, out-of-stock item blocked.
"""
import pytest
from pathlib import Path

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def given_cart_with_items(cart: Cart, products: list) -> Cart:
    for product in products:
        cart.add(product)
    return cart

def when_order_is_submitted(cart: Cart) -> Order:
    return cart.submit()

def then_order_is_confirmed(order: Order, expected_products: list) -> None:
    assert order.is_confirmed
    assert order.items == expected_products

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def workspace_root(tmp_path: Path) -> Path:
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    return workspace

@pytest.fixture
def empty_cart(workspace_root: Path) -> Cart:
    return Cart(workspace_root=workspace_root)

@pytest.fixture
def available_product(workspace_root: Path) -> Product:
    return Product(workspace_root=workspace_root, sku='item-a', stock=10)

# ============================================================================
# STORY: Place Order
# ============================================================================

class TestPlaceOrder:
    """Place Order — user submits a cart and receives a confirmed order."""

    def test_order_confirmed_for_available_items(self, empty_cart, available_product):
        # Given: cart contains available items
        cart = given_cart_with_items(empty_cart, [available_product])
        # When: order is submitted
        order = when_order_is_submitted(cart)
        # Then: order is confirmed with those items
        then_order_is_confirmed(order, [available_product])

    def test_empty_cart_is_rejected(self, empty_cart):
        # When / Then: submitting an empty cart raises EmptyCartError
        with pytest.raises(EmptyCartError):
            when_order_is_submitted(empty_cart)
```

## The shape of a good test file

```
test_<area_snake_case>.py
  Module docstring: area name + behaviors/stories covered
  Imports (stdlib → third-party → local)
  HELPER FUNCTIONS section
    given_*() / create_*() setup factories — parameterized, not duplicated
    when_*() actions
    then_*() / verify_*() assertions — parameterized, not duplicated
  FIXTURES section
    @pytest.fixture workspace_root (or domain equivalent)
  # STORY / BEHAVIOR: <Name> section comment
  class Test<BehaviorName>:
    def test_<outcome_snake_case>(self, workspace_root):
      # Given: <step text verbatim>
      # When: <step text verbatim>
      # Then: <step text verbatim>
  # STORY / BEHAVIOR: <Next Name> section comment
  class Test<NextBehaviorName>:
    ...

When helpers are shared across sub-epic files, extract them into:
  tests/<epic_name>/<epic_name>_helper.py
    class <EpicName>Helpers:
      given_*() / when_*() / then_*() methods only — no test_*() methods
  tests/<epic_name>/<sub_epic_name>/<sub_epic_name>.py
    class Test<Story>(<EpicName>Helpers): ...
```
