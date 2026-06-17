---
name: abd-acceptance-test-driven-development
catalog_garden_tier: practice
catalog_garden_order: 50
catalogue_one_liner: >-
  Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR).
description: >-
  Write tests first, then drive code to pass them. Creates executable test files in
  the target language and framework from any behavioral context — spec-by-example
  scenarios (ideal), acceptance criteria, stories, notes, or rough descriptions.
  Orchestrator pattern: Given-When-Then test methods call helper functions; one class
  (or equivalent) per behavior, one test per scenario. Covers TDD cycle
  (RED-GREEN-REFACTOR), domain language, API design through failing tests, and
  production code rules. Use when writing acceptance tests, turning behavioral
  context into test code, or driving implementation with tests.
---
# abd-acceptance-test-driven-development

## Purpose

**Write tests first. Write code to pass them.**

This skill creates **executable test files** — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should do. The output is real test code that runs, fails, and drives what gets built.

The workflow is **test-driven**: write a test that expresses the expected behavior, run it to confirm it fails (RED), then rely on a  downstream skill or agent to develop the production code skill to implement until the test passes (GREEN). Each test is a precise, runnable statement of what the system must do —  test methods show the Given-When-Then flow and helper functions do the work.

The skill covers the full test quality bar: domain language in names, observable-behavior assertions, coverage of normal and failure paths, helper reuse, and clean production code that makes tests easy to write.

## When to use this skill

Load this skill when **any** of the following apply:

- You have **specification scenarios**, acceptance criteria, stories, or informal notes and want to turn them into executable tests.
- You want to drive **production code design** by writing tests first (TDD — RED phase before GREEN phase).
- You are reviewing test code for quality: domain language, observability, coverage, helper structure.
- An agent is asked to "write tests", "generate test code", "implement test cases", "write acceptance tests", or "turn scenarios into tests."
- You have only a rough description of behavior and need to derive tests from it (start from whatever context exists).
- You need to fix a bug and want the correct **test-first** workflow.

---

## Output file

**Where to write the test files (`<tests-folder>` resolution):**

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the project already keeps tests.** Look at the workspace; if a `tests/`, `test/`, `spec/`, or language-conventional test folder exists, put new test files in the appropriate subdirectory there.
3. **The workspace root.** If neither applies (e.g. brand-new project), write to the workspace root or a sensible language-default location (`tests/` for Python, `src/test/java/...` for Java, `__tests__/` or `*.test.ts` co-located for JS/TS).

Do **not** invent a predetermined folder name. Tests follow the host project's conventions, not this skill's. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**.

**File names:** Use the target language's test-discovery convention (`test_<scenario>.py`, `<Scenario>Test.java`, `*.test.ts`, etc.). The file body is generated from the bundled templates in `templates/` (`acceptance-tests.py`, `acceptance-tests.java`, `acceptance-tests.js`). Add a `<name>-` or feature prefix only when project conventions ask for it — bare scenario or story names are the default.

---

## Agent Instructions

0. **Verify test structure first (Priority 1)** — Trace the story hierarchy, declare file / class / method before writing any code. See **Test organization** in Core concepts.
1. **Confirm language and framework** — If not stated, ask. Defaults: pytest (Python), `node:test` (JS/TS), JUnit 5 (Java).
2. **Pick the matching template** from `templates/` — `acceptance-tests.py`, `.js`, or `.java`. Emit code only; omit the `## Instructions` block.
3. **Build** — One file per area, one class per story, one method per scenario. Name helpers with GWT language (`given_*`, `when_*`, `then_*`) matching step text verbatim. Parameterize helpers to prevent sprawl. Extract shared helpers to `tests/<epic_name>/<epic_name>_helper.py` when reused across files. See **Orchestrator pattern** and **The shape of a good test file** below.
4. **Validate** — Peer-review against the Rules section; 
5. **Assembling this skill** — Reassemble with `bundle_rules_into_skill_md.py` after editing `rules/` or `templates/`.

---

## What is acceptance test-driven development?

**Acceptance test-driven development (ATDD)** is a practice where **automated tests** are written from behavioral context — in whatever form is available — before (or alongside) production code. Tests validate that the system does what the behavior says it should do — from the outside, through observable outcomes.

The richer the input, the more direct the translation: **spec-by-example scenarios** give you Given/When/Then steps to encode directly; **acceptance criteria** give you WHEN/THEN pairs to convert; **stories with notes** give you intent to derive from; **unstructured context** gives you behaviors to discover and make concrete.

In this skill's approach:
- **Tests drive design** — tests are written against the real expected API first; they must fail before implementation begins.
- **RED before GREEN** — a test that passes immediately proves nothing; a failing test defines exactly what to build.
- **Orchestrator pattern** — test methods show the Given-When-Then flow by calling helper functions; helpers handle the detail.
- **Domain language** — test and called class names, method names, and helper names use the same vocabulary as the domain context being tested.
- **Any context works** — the quality of the output scales with the specificity of the input, but the practice applies regardless.

---

## Core concepts

### Test organization

Tests mirror the story hierarchy as a folder structure. You navigate down through epics and sub-epics as nested folders until you reach the lowest-level sub-epic — that becomes the **file**. The story inside it becomes the **class**. Each scenario on that story becomes a **method**.

```
tests/
  <epic>/
    <epic>_helper.py              ← shared Given/When/Then helpers for this epic
    <sub_epic>/
      <sub_epic>/
        ...
          <lowest_sub_epic>/
            <lowest_sub_epic>.py  ← FILE  (named after the lowest-level sub-epic)
              class Test<Story>   ← CLASS (named after the story)
                def test_<scenario>  ← METHOD (named after the scenario)
```

The epic-level helper file (`<epic>_helper.py`) sits at the epic folder that is the parent of all children epics that will inherit that common logic, and contains only reusable `given_*` / `when_*` / `then_*` helper methods — no test methods. Sub-epic test files inherit from it when they share helpers.

**The most common mistake** is naming the file after the story instead of the lowest-level sub-epic that contains it. The story is always the class, never the file.

**Before writing any code, declare the structure explicitly:**
- Story Path: `[Epic] → [Sub-Epic] → ... → [Lowest Sub-Epic] → [Story]`
- File: `tests/<epic>/.../  <lowest_sub_epic>/<lowest_sub_epic>.py`
- Class: `Test<ExactStoryName>`
- Method: `test_<scenario_outcome_snake_case>`
- Existing: yes / no — add to existing file; do not create a duplicate

### Orchestrator pattern

Test methods **orchestrate** the flow; **helper functions** handle the details.

- Test method: under 20 lines, shows Given/When/Then structure by calling helpers.
- Helper function: under 20 lines, reusable setup/action/assertion logic.
- Test class: under 300 lines, one class per story.

Use Helper functions whhen test methods can to be shared, test cmethod code is complex or long. 
**Helper naming** — name helpers using the step vocabulary: `given_cart_with_items(...)`, `when_order_is_submitted(...)`, `then_order_is_confirmed(...)`. Test methods read as executable scenarios.

**Helper discipline** — parameterize to prevent sprawl. If `create_order_pending` and `create_order_confirmed` appear side by side, merge them into `create_order(status)`. When helpers are shared across multiple sub-epic test files, extract them into an epic-level base class in `tests/<epic_name>/<epic_name>_helper.py` and inherit from it.




### TDD cycle

**RED → GREEN → REFACTOR.** Write a failing test first (RED). Implement the minimal code to make it pass (GREEN). Improve code quality while keeping tests green (REFACTOR). Tests must fail before any production code exists — a test that passes immediately proves nothing.

### Domain language

Use the same vocabulary as the domain model, stories, and acceptance criteria in:
- Class names → domain entities (`GatherContextAction`, `BotConfig`)
- Method names → domain responsibilities (`inject_questions_and_evidence`, `load_trigger_words`)
- Test names → observable behavior (`test_agent_loads_configuration_when_file_exists`)

---

## Example

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


---

<!-- execute_rules:bundle_rules:begin -->
﻿---
scanner: full_result_assertions_scanner.py
---

### Rule: Assert Full Results

Assert **complete domain objects** (state dictionaries, dataclasses, graph objects, log records) rather than cherry-picking a single field. Single-field assertions miss structural regressions and leave most of the domain object unverified.

#### DO

- Compare the full result against a named standard fixture.
- Define standard data sets as module-level constants or helper factories.

```python
STANDARD_STATE = {
    'behavior': 'shape',
    'action': 'clarify',
    'phase': 'exploration',
    'context': {},
}

def test_bot_starts_in_standard_state(self, workspace_root):
    # Given
    helper = BotTestHelper(workspace_root)

    # When
    helper.set_state('shape', 'clarify')

    # Then — assert full state object
    assert helper.get_state() == STANDARD_STATE
```

#### DON'T

- Assert only one field from a complex domain result.
- Assert a count instead of the underlying records.

```python
# WRONG: cherry-picking a single field
assert helper.get_state()['behavior'] == 'shape'

# WRONG: asserting count when the records matter
assert len(result.stories) == 3
```

﻿---
scanner: bug_fix_test_first_scanner.py
---

### Rule: Bug-Fix Test First

When production code breaks, follow the **RED → GREEN → PRODUCTION** workflow. Write a failing test that reproduces the bug before touching any production code. Never fix bugs without a failing test first — a fix without a test may be incomplete and will not prevent regression.

#### DO

1. Write a test that reproduces the bug (RED — test fails).
2. Run the test to confirm it fails for the right reason.
3. Fix the minimal production code to make the test pass (GREEN).
4. Run the full suite to confirm nothing regressed.

```python
# Step 1 — RED: reproduce the bug
def test_mcp_tool_initializes_bot(self, workspace_root):
    # This test fails before the fix
    bot = MCPTool(workspace_root=workspace_root)
    bot.initialize()
    assert bot.is_ready  # fails here

# Step 2 — fix the production code until test is GREEN
# Step 3 — run full suite
```

#### DON'T

- Edit production code without first writing a test that fails because of the bug.
- Deploy a fix and assume it works without a passing test.

```python
# WRONG: edit production code first
# def initialize(self):
#     self._ready = True   ← fix here without a failing test
```

### Rule: Call Production Code Directly

Call production code **directly** in tests. Let tests fail naturally when the code does not exist or has bugs. Do not comment out production code calls, mock the class under test, or fabricate state to make tests pass. A `NameError` or `AttributeError` is the test driving the implementation — not a problem to hide.

#### DO

- Call the real class and method.
- Let the test fail with a clear error if the code is not yet implemented.

```python
def test_agent_loads_config(self, workspace_root):
    # Given
    config_file = create_config_file(workspace_root, 'story_bot')

    # When — call real production code directly
    agent = Agent(workspace_root=workspace_root)
    agent.initialize()

    # Then
    assert agent.is_initialized
```

#### DON'T

- Mock the class under test.
- Comment out the call because the code does not exist.
- Fake state by writing to private attributes.

```python
# WRONG: mocking the class under test
agent = Mock(spec=Agent)

# WRONG: commenting out the real call
# agent.initialize()  # TODO: implement
result = None  # placeholder

# WRONG: setting private state to make the test pass
agent._initialized = True
```

﻿---
scanner: class_based_organization_scanner.py
---

### Rule: Class-Based Test Organization

Organize test files around **behavior clusters** from the source context — stories, flows, or feature areas. The test **file** is named after the grouping that contains the behaviors (flow, sub-epic, feature area), the test **class** is named after the specific behavior, and the test **method** is named after the specific scenario or condition. Getting this wrong requires deleting and recreating files. Before writing any test code, state the file name, class name, and method name explicitly from the source material.

#### DO

- **Before writing code**, state the structure explicitly:
  - Source: `[Flow / Area] → [Behavior] → [Scenario]`
  - File: `test_<area_snake_case>.py`
  - Class: `Test<ExactBehaviorName>` (PascalCase of full behavior name from source)
  - Method: `test_<scenario_outcome_snake_case>`
- Name the file after the **grouping** that contains the behaviors — not the behavior itself.
- Name the class using the **exact behavior name** from the source — no abbreviation, no summarisation.
- Add to an existing area file rather than creating a new one when the file already exists.

```python
# Area: 'Manage Orders'  →  File: test_manage_orders.py
# Behavior: 'Place Order'  →  Class: TestPlaceOrder
# Scenario: 'Order confirmed for available items'
#   →  Method: test_order_confirmed_for_available_items

class TestPlaceOrder:
    def test_order_confirmed_for_available_items(self, workspace_root):
        ...

    def test_empty_cart_is_rejected(self, workspace_root):
        ...
```

#### DON'T

- Name the file after the individual behavior — use the parent grouping.
- Abbreviate or genericise the class name.

```python
# WRONG: file named after the individual behavior
# File: test_place_order.py

# WRONG: abbreviated or generic class names
class TestOrder:          # abbreviated — exact behavior is 'Place Order'
class TestOrderHandling:  # invented topic, not in source

# CORRECT: exact name from source context
class TestPlaceOrder:
    ...
```

﻿---
scanner: consistent_vocabulary_scanner.py
---

### Rule: Consistent Vocabulary

Use **one word per concept** across the entire codebase. Pick a verb and stick to it: `create` (not `build`/`make`/`construct`), `verify` (not `check`/`assert`/`validate`), `load` (not `fetch`/`get`/`retrieve`). Document the vocabulary at the top of the test file when it helps reviewers.

#### DO

- Use the same verb for the same operation everywhere.

```python
# Consistent vocabulary: create / verify / load
def create_agent(name: str, workspace: Path) -> Agent: ...
def create_config(workspace: Path, name: str) -> Path: ...
def create_workspace(tmp_path: Path) -> Path: ...

def verify_agent_initialized(agent: Agent) -> None: ...
def verify_config_valid(config: dict) -> None: ...

def load_config(path: Path) -> dict: ...
```

#### DON'T

- Mix synonyms for the same concept.

```python
# WRONG: three verbs for creation
def create_agent(...): ...
def build_config(...):   # should be create_config
def make_workspace(...): # should be create_workspace
```

﻿---
scanner: cover_all_paths_scanner.py
---

### Rule: Cover All Behavior Paths

Every story needs tests for the **normal (happy) path**, **edge cases**, and **failure paths**. Each distinct behavior gets its own focused, independent test. Tests must be deterministic (same result every run) and independent of execution order.

#### DO

- Write separate tests for normal, edge, and failure scenarios.
- Make every test independent — no shared mutable state across test methods.

```python
def test_loads_valid_configuration(self, workspace_root):     # normal path
    ...

def test_loads_empty_configuration(self, workspace_root):     # edge case
    ...

def test_raises_error_when_config_missing(self, workspace_root):  # failure path
    with pytest.raises(FileNotFoundError):
        Agent(config_path=workspace_root / 'missing.json')
```

#### DON'T

- Test only the happy path and leave edge and failure behavior unspecified.
- Combine multiple behaviors in one test method.

```python
# WRONG: single test for both success and failure
def test_loads_config(self, workspace_root):
    # Tests valid case AND missing file in same method
    ...
```

### Rule: Create Parameterized Tests for Scenarios

When specification scenarios include an **Examples table**, create **parameterized tests** using `@pytest.mark.parametrize`. Each row in the Examples table becomes a separate test case. Do not write a single test that only exercises one example, and do not duplicate test methods per row.

#### DO

- Map each Examples column to a `parametrize` parameter.
- Name the combined test so the parameter values appear in the test ID.

```python
@pytest.mark.parametrize('input_paths,expected_count', [
    (['path/a', 'path/b'], 2),
    (['path/c'],            1),
    ([],                    0),
])
def test_loader_counts_paths(self, workspace_root, input_paths, expected_count):
    # Given
    loader = create_loader(workspace_root, input_paths)

    # When
    result = loader.count()

    # Then
    assert result == expected_count
```

#### DON'T

- Hardcode a single example when the specification has a table.
- Create one test method per row.

```python
# WRONG: separate method per row
def test_with_two_paths(self): ...
def test_with_one_path(self):  ...

# WRONG: single hardcoded example from a multi-row table
def test_loader_counts_paths(self):
    loader = create_loader(workspace_root, ['path/a', 'path/b'])
    assert loader.count() == 2  # only one of several rows tested
```

﻿---
scanner: fixture_placement_scanner.py
---

### Rule: Define Fixtures in Test File

Define **pytest fixtures in the same test file** that uses them, not in a separate `conftest.py`. Only truly cross-cutting fixtures (generic filesystem helpers, shared infrastructure) belong in a base `conftest.py`. Story-specific fixtures stay local.

#### DO

- Declare fixtures at the top of the test file, after helpers.
- Keep them focused on what the tests in that file need.

```python
# In test_edit_story_graph.py

@pytest.fixture
def workspace_root(tmp_path: Path) -> Path:
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    return workspace

@pytest.fixture
def story_graph(workspace_root: Path) -> StoryGraph:
    return create_story_graph(workspace_root)
```

#### DON'T

- Create a new `conftest.py` for agent- or sub-epic-specific fixtures.
- Create shared files before there is an explicit, demonstrated need.

```python
# WRONG: story-specific fixture in conftest.py
# conftest.py
@pytest.fixture
def story_graph(tmp_path):  # belongs in test_edit_story_graph.py, not here
    ...
```

﻿---
scanner: failing_test_api_scanner.py
---

### Rule: Design API Through Failing Tests

Write tests against the **real expected API before** implementing the code. The test **must fail initially** (RED phase). The failure message — `ImportError`, `AttributeError`, `TypeError` — reveals the complete API design: class names, constructor parameters, methods, return types. This is how tests drive implementation rather than simply verify it.

#### DO

- Call the real expected class and method even when they do not exist yet.
- Set up real test data (real files, real paths via `tmp_path`) rather than mock objects.
- Assert real expected behavior so the test verifies something meaningful once implemented.

```python
def test_project_initializes_with_agent_config(self, tmp_path):
    # Given: real config file (tmp_path)
    agent_config_path = tmp_path / 'agents' / 'base' / 'agent.json'
    agent_config_path.parent.mkdir(parents=True)
    agent_config_path.write_text('{"name": "story_bot", "behaviors": ["shape"]}')

    # When: call REAL expected API (doesn't exist yet — will fail)
    from agile_bot.project import Project
    project = Project(
        project_path=tmp_path / 'projects' / 'test-project',
        agent_config_path=agent_config_path,
    )
    project.initialize()

    # Then: verify real behavior
    assert project.agent.name == 'story_bot'
    assert project.is_initialized is True
    # Test fails with ImportError/AttributeError until implemented — that's correct (RED)
```

#### DON'T

- Use placeholder values (`None`, `'TODO'`, `{}`) that hide the real API.
- Skip the RED phase by implementing first, then writing a test that passes.
- Write vacuous tests that assert nothing meaningful.

```python
# WRONG: placeholders hide the API
project = None        # placeholder — reveals nothing
agent = 'TODO'        # placeholder — reveals nothing
assert project is None  # useless assertion

# WRONG: test passes immediately (GREEN before RED)
def test_something():
    assert True       # proves nothing
```

### Rule: Domain-Oriented Test Inheritance

**At small scale**, a single test class covering multiple domain objects in the same sub-epic is fine. **As domain objects develop distinct behavior**, extract them into domain-specific test classes with a shared abstract base class for common operations. Share fixtures and parameter data only when there is obvious shared logic — do not create shared infrastructure pre-emptively.

#### DO

- At small scale: keep related tests together in one class.
- At scale: use abstract base classes for shared assertion logic; place shared base files at the appropriate hierarchy level (sub-epic or epic).

```python
# Small scale — fine
class TestPaymentOperations:
    def test_creates_wire_payment(self): ...
    def test_creates_ach_payment(self): ...

# At scale — domain-specific classes with shared base
class PaymentTestBase:
    def verify_payment_persisted(self, payment): ...

class TestWirePayment(PaymentTestBase):
    def test_creates_wire_payment(self): ...

class TestACHPayment(PaymentTestBase):
    def test_creates_ach_payment(self): ...
```

#### DON'T

- Copy assertion logic across classes instead of using a base class.
- Create shared files before there is an explicit, demonstrated need.
- Group tests by operation layer or technology rather than domain object.

```python
# WRONG: duplicated assertion logic
class TestWirePayment:
    def test_creates_payment(self):
        assert payment.status == 'pending'   # duplicated
        assert payment.rail == 'wire'        # duplicated

class TestACHPayment:
    def test_creates_payment(self):
        assert payment.status == 'pending'   # same assertion copied
        assert payment.rail == 'ach'
```

﻿---
scanner: helper_extraction_scanner.py
---

### Rule: Helper Extraction and Reuse

Extract **duplicate test setup** into reusable helper functions. Keep test method bodies focused on the scenario behavior, not on building infrastructure. Group helpers by purpose: `create_*` for factories, `verify_*` for assertions, `load_*` for data loading.

#### DO

- Extract any setup or verification that appears in two or more tests.
- Name helpers after their domain purpose (see **consistent-vocabulary**).

```python
def create_agent_with_config(name: str, workspace: Path) -> Agent:
    """Helper: Create fully initialized agent."""
    config = create_config_file(workspace, name)
    agent = Agent(agent_name=name, workspace_root=workspace)
    agent.initialize()
    return agent

# Tests reuse the helper — no duplication
def test_agent_reports_correct_name(self, workspace_root):
    agent = create_agent_with_config('story_bot', workspace_root)
    assert agent.name == 'story_bot'

def test_agent_is_initialized(self, workspace_root):
    agent = create_agent_with_config('story_bot', workspace_root)
    assert agent.is_initialized
```

#### DON'T

- Copy the same 10 lines of setup into every test method.

```python
# WRONG: duplicated setup in every test
def test_agent_reports_name(self):
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    config_dir = workspace / 'agents' / 'base'
    config_dir.mkdir(parents=True)
    config_file = config_dir / 'agent.json'
    config_file.write_text('{"name": "story_bot"}')
    agent = Agent('story_bot', workspace)
    agent.initialize()
    assert agent.name == 'story_bot'

def test_agent_is_initialized(self):
    # ... same 10 lines again ...
```

﻿---
scanner: specification_match_scanner.py
---

### Rule: Match Specification Scenarios

Tests must match the corresponding **specification scenarios exactly**. Use the same terminology, variable names, and steps that the scenario states. Assertions verify exactly what the scenario's THEN conditions specify — nothing more, nothing less.

#### DO

- Use exact variable names from the specification (`agent_name`, `workspace_root`, `config_path`).
- Assert only the outcomes the scenario explicitly states.

```python
# Specification scenario:
# GIVEN: configuration file exists at agents/base/agent.json
# WHEN: Agent is initialized with agent_name='story_bot'
# THEN: agent.config_path == agents/base/agent.json

def test_agent_loads_configuration_when_file_exists(self, workspace_root):
    # Given
    config_path = create_config_file(workspace_root, agent_name='story_bot')

    # When
    agent = Agent(agent_name='story_bot', workspace_root=workspace_root)
    agent.initialize()

    # Then — matches the THEN from the scenario exactly
    assert agent.config_path == workspace_root / 'agents' / 'base' / 'agent.json'
```

#### DON'T

- Use different terminology from the specification (`name` when spec says `agent_name`).
- Assert internal state not mentioned in the scenario.

```python
# WRONG: different variable name from spec
agent = Agent(name='story_bot')       # spec says agent_name, not name

# WRONG: asserting internal detail not in scenario
assert agent._initialized == True     # not in the scenario THEN conditions
```

﻿---
scanner: mock_boundaries_scanner.py
---

### Rule: Mock Only Boundaries

Mock **only** at architectural boundaries — external APIs, network calls, third-party services, and genuinely uncontrollable dependencies. Do **not** mock internal business logic, the class under test, or file operations. Use real temp files (`tmp_path`) for file I/O. Tests that mock internal logic verify the mock, not the code.

#### DO

- Mock external HTTP calls, remote APIs, or third-party services.
- Use `pytest`'s `tmp_path` for real file operations instead of mocking the file system.

```python
# Mock an external HTTP boundary
with patch('requests.get') as mock_get:
    mock_get.return_value.json.return_value = {'status': 'ok'}
    result = agent.fetch_remote_config('http://api.example.com')

# Real file I/O — no mock needed
config_file = tmp_path / 'config.json'
config_file.write_text('{"name": "story_bot"}')
agent = Agent(config_path=config_file)
```

#### DON'T

- Mock the class under test.
- Mock internal business logic or validation methods.
- Mock file I/O when `tmp_path` works.

```python
# WRONG: mocking the class under test
agent = Mock(spec=Agent)          # tests nothing real

# WRONG: mocking internal logic
with patch.object(Agent, 'validate_config'):   # defeats the test

# WRONG: mocking file ops that could use tmp_path
with patch('builtins.open', mock_open(read_data='{}')): ...
```

﻿---
scanner: no_guard_clauses_scanner.py
---

### Rule: No Defensive Code in Tests

Tests must **never** contain guard clauses, defensive conditionals, `try/except`, or fallback paths. Tests control their own setup — if setup is wrong, the test **must fail immediately and clearly**. Guard clauses hide problems by silently skipping assertions.

#### DO

- Assume correct setup; let the test fail if setup is not right.
- Call code directly without wrapping in conditionals.

```python
def test_behavior_loads_by_name(self, workspace_root):
    # Given — direct setup, no guard
    behavior = Behavior(name='shape', workspace_root=workspace_root)

    # When / Then — no if-check needed
    assert behavior.name == 'shape'
    assert behavior.instructions_path.exists()
```

#### DON'T

- Wrap operations in `if`, `try/except`, or `hasattr` checks.
- Add fallback paths to paper over setup problems.

```python
# WRONG: defensive conditional hides a broken test
if behavior_file.exists():        # if it doesn't exist, test silently passes!
    behavior = load_behavior(behavior_file)
    assert behavior.name == 'shape'

# WRONG: exception swallowed
try:
    agent.initialize()
except Exception:
    pass  # hides the real failure
```

﻿---
scanner: object_oriented_helpers_scanner.py
---

### Rule: Object-Oriented Test Helpers

Consolidate test setup around **shared helper objects** (test hoppers / factories) that build **complete domain fixtures** with standard data. Avoid scattering many primitive parameters across `parametrize` blocks or inline setups. A helper object centralizes construction of the full domain context in one place.

#### DO

- Use a test helper class (e.g. `BotTestHelper`) that builds a complete domain object in one call.
- Assert against complete objects, not fragments.

```python
class BotTestHelper:
    def __init__(self, workspace: Path) -> None:
        self._workspace = workspace
        self._bot = create_bot(workspace)

    def set_state(self, behavior: str, action: str) -> None:
        self._bot.navigate_to(behavior, action)

    def assert_at_behavior_action(self, behavior: str, action: str) -> None:
        assert self._bot.current_behavior == behavior
        assert self._bot.current_action == action

def test_bot_navigates_to_shape_clarify(self, workspace_root):
    helper = BotTestHelper(workspace_root)
    helper.set_state('shape', 'clarify')
    helper.assert_at_behavior_action('shape', 'clarify')
```

#### DON'T

- Spread test setup across many primitive parameters in `parametrize` blocks.
- Cherry-pick single values from a partial object.

```python
# WRONG: many primitives scattered across parametrize
@pytest.mark.parametrize('behavior, action, workspace, config, expected_status', [
    ('shape', 'clarify', '/tmp/ws1', {'k': 'v'}, 'active'),
    ...
])
def test_bot_state(self, behavior, action, workspace, config, expected_status):
    assert bot.status == expected_status  # single field
```

﻿---
scanner: import_placement_scanner.py
---

### Rule: Place Imports at Top

All imports must appear at the **top of the test file**, after the module docstring, before any code. Group imports: (1) standard library, (2) third-party, (3) local project. Never place imports inside functions or test methods.

#### DO

```python
"""Agent configuration tests."""
import json
import pytest
from pathlib import Path

from agile_bot.agents.base_bot.src.agent import Agent
from agile_bot.agents.base_bot.src.config_loader import ConfigLoader
```

#### DON'T

- Place imports inside functions or after code.

```python
def test_agent_initializes(self, tmp_path):
    from pathlib import Path            # WRONG: import inside function
    from agile_bot.agent import Agent   # WRONG: import inside test method
    ...
```

### Rule: Production Code Clean Functions

Production code functions must do **one thing**, stay **under 20 lines**, operate at a **single level of abstraction**, and have **no hidden side effects**. The function name must fully describe what it does. Extract multiple concerns into separate functions.

#### DO

- Each function has a single, named purpose.
- Functions compose to build complexity.

```python
def load_config(self, path: Path) -> dict:
    """Load configuration from file."""
    return json.loads(path.read_text())

def validate_config(self, config: dict) -> bool:
    """Validate configuration has required keys."""
    return all(key in config for key in ('name', 'workspace'))

def initialize_from_config(self, path: Path) -> None:
    """Initialize agent from configuration file."""
    config = self.load_config(path)
    if not self.validate_config(config):
        raise ValueError(f'Invalid config at {path}')
    self._apply_config(config)
```

#### DON'T

- Write functions that load, validate, apply, and log in the same body.
- Exceed 20 lines in a single function.

```python
# WRONG: function does too many things
def setup(self, path: Path) -> None:
    config = json.loads(path.read_text())   # load
    if 'name' not in config:                # validate
        raise ValueError('Invalid')
    self.name = config['name']              # apply
    logger.info(f'Initialized {self.name}') # log
    self._send_metrics()                    # side effect
```

﻿---
scanner: explicit_dependencies_scanner.py
---

### Rule: Production Code Explicit Dependencies

Production code must make **all dependencies explicit** through **constructor injection**. Pass every external dependency (config loader, graph, file system abstraction) as a constructor parameter. No hidden global state, no singletons created internally, no service-locator calls. Explicit dependencies make the class trivially testable.

#### DO

- Accept every dependency as a constructor parameter.
- Assign to instance attributes immediately.

```python
class Agent:
    def __init__(
        self,
        agent_name: str,
        workspace_root: Path,
        config_loader: ConfigLoader,
        domain_graph: DomainGraph,
    ) -> None:
        self.name = agent_name
        self.workspace_root = workspace_root
        self._config_loader = config_loader
        self._domain_graph = domain_graph
```

#### DON'T

- Create dependencies internally or access module-level singletons.

```python
# WRONG: hidden dependencies created inside the constructor
class Agent:
    def __init__(self, agent_name: str) -> None:
        self.name = agent_name
        self._loader = ConfigLoader()          # creates internally
        self._graph = DomainGraph.get_instance()  # global singleton
```

﻿---
scanner: orchestrator_pattern_scanner.py
scanner_note: Python / pytest — use the equivalent scanner for the target language
---

### Rule: pytest Orchestrator Pattern

Use the **orchestrator pattern** for story-based tests — no step-definition files. Every test method (under 20 lines) shows the Given-When-Then flow by calling named helper functions. Helper functions handle details (also under 20 lines). Test classes (or equivalent groupings) stay under 300 lines. Examples below are Python / pytest — apply the same structure in the idioms of the target language and framework.

#### DO

- Test methods show the flow; helpers execute the details.
- Use `# Given`, `# When`, `# Then` comment labels inside every test method.
- Keep test methods under 20 lines; extract anything longer to a helper.
- Keep helper functions under 20 lines each.

```python
# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_config_file(workspace: Path, name: str = 'bot') -> Path:
    """Helper: Create bot configuration file."""
    config_dir = workspace / 'agents' / 'base'
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / 'agent.json'
    config_file.write_text(f'{{"name": "{name}"}}')
    return config_file

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def workspace_root(tmp_path):
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    return workspace

# ============================================================================
# ORCHESTRATOR TESTS
# ============================================================================

class TestAgentInitialization:
    def test_agent_initializes_with_config(self, workspace_root):
        # Given
        config = create_config_file(workspace_root, 'story_bot')

        # When
        agent = Agent(agent_name='story_bot', workspace_root=workspace_root)
        agent.initialize()

        # Then
        assert agent.is_initialized
        assert agent.config_path == config
```

#### DON'T

- Use feature files or `@given`/`@when`/`@then` step decorators.
- Inline 10+ lines of setup directly inside test methods.
- Write test methods longer than 20 lines.

```python
# WRONG: step definitions
@given('config file exists')
def step_config_exists(context): ...

# WRONG: all setup inline — extract to helpers
def test_agent(self, tmp_path):
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    config_dir = workspace / 'agents' / 'base'
    config_dir.mkdir(parents=True)
    config_file = config_dir / 'agent.json'
    config_file.write_text('{"name": "bot"}')
    agent = Agent('bot', workspace)
    # ... 15 more lines ...
```

### Rule: Self-Documenting Tests

Tests are self-documenting through **code structure** — imports, constructor calls, and assertions show the API design. Do not add verbose comments that explain what will fail or restate what the code already says. Let the code speak for itself.

#### DO

- Let imports reveal which classes are needed.
- Let constructors show the required parameters.
- Let assertions show what is expected.

```python
def test_generator_creates_server_for_test_bot(self, workspace_root):
    # Given
    config_file = create_bot_config(workspace_root, 'test_bot', ['shape'])

    # When
    from agile_bot.mcp_server_generator import MCPServerGenerator
    generator = MCPServerGenerator(
        bot_name='test_bot',
        config_path=config_file,
        workspace_root=workspace_root,
    )
    server_file = generator.generate_server()

    # Then
    assert server_file.exists()
    assert server_file.name == 'test_bot_server.py'
```

#### DON'T

- Add comments explaining that the test will fail or what API is needed — the code shows this.
- Restate what constructors and assertions already communicate.

```python
# WRONG: verbose noise
    # TEST WILL FAIL: ImportError - MCPServerGenerator doesn't exist yet
    # Shows API needs: MCPServerGenerator(bot_name, config_path, workspace_root)
    # Shows API needs: generator.generate_server() returns Path
    # The code above already communicates all of this!

    assert server_file.exists()
```

﻿---
scanner: standard_data_reuse_scanner.py
---

### Rule: Standard Test Data Sets

Define **canonical, named test data sets** as module-level constants or factory functions and **reuse them** across tests. Do not recreate ad-hoc values in every test method. Standard data sets ensure every test exercises the full domain object and prevent tests from diverging on what "valid" data looks like.

#### DO

- Define standard data once at the module level (or in a shared helpers module).
- Reuse the same constants across tests in the file.

```python
STANDARD_AGENT_CONFIG = {
    'name': 'story_bot',
    'behaviors': ['shape', 'discovery', 'tests'],
    'workspace': 'agile_bots',
}

STANDARD_BOT_STATE = {
    'behavior': 'shape',
    'action': 'clarify',
    'phase': 'exploration',
}

def test_agent_loads_standard_config(self, workspace_root):
    config_file = create_config_file(workspace_root, STANDARD_AGENT_CONFIG)
    agent = Agent(config_path=config_file)
    agent.initialize()
    assert agent.config == STANDARD_AGENT_CONFIG
```

#### DON'T

- Create new ad-hoc config values per test.
- Assert only one field from a complex object that has a matching standard.

```python
# WRONG: ad-hoc values differ per test — hard to maintain
def test_agent_loads_config_a(self):
    config = {'name': 'bot', 'behaviors': ['shape']}
    ...

def test_agent_loads_config_b(self):
    config = {'name': 'mybot', 'behaviors': ['shape', 'tests']}  # inconsistent
    ...
```

﻿---
scanner: observable_behavior_scanner.py
---

### Rule: Test Observable Behavior

Test behavior through the **public API** — observable properties, return values, and state changes visible to callers. Do not assert on private attributes, internal flags, or implementation details. Tests that verify private state break on refactoring even when behavior is correct.

#### DO

- Assert on public properties and return values.
- Verify the outcome a caller would see.

```python
# Test public API
assert agent.is_initialized
assert agent.config_path.exists()
assert agent.get_config_value('name') == 'story_bot'
assert result.status == 'ready'
```

#### DON'T

- Assert on private attributes (`_`, `__`-prefixed).
- Test internal data structures or intermediate state that is not part of the contract.

```python
# WRONG: private implementation details
assert agent._initialized == True
assert agent._setup_called == True
assert len(agent._internal_steps) == 5
assert agent._config_cache is not None
```

﻿---
scanner: ascii_only_scanner.py
---

### Rule: Use ASCII Only

All test code must use **ASCII-only characters**. No Unicode symbols, emoji, special punctuation, or curly quotes. Windows environments and CI pipelines can mishandle non-ASCII bytes in source files. Use plain ASCII alternatives.

#### DO

- Use bracket labels for status indicators: `[PASS]`, `[FAIL]`, `[ERROR]`, `[SKIP]`.
- Use `->` for arrows, `!=` for not-equal, standard ASCII quotes.

```python
print('[PASS] Agent initialized')
print('[ERROR] Config not found')
result = {'status': 'ok', 'name': 'story_bot'}
```

#### DON'T

- Use Unicode symbols, emojis, or curly quotes anywhere in test code.

```python
# WRONG
print('\u2713 Done')           # Unicode checkmark
print('\U0001f7e2 OK')         # emoji
message = '\u201chello\u201d'  # curly quotes
```

﻿---
scanner: business_readable_test_names_scanner.py
---

### Rule: Use Domain Language

Apply **Ubiquitous Language** (DDD): use the same vocabulary in the domain model, stories, acceptance criteria, scenarios, **and** code. Class names map to domain entities or nouns; method names map to domain responsibilities or verbs; test names read like plain-English stories. This is priority 1 — it overrides generic technical naming at every level.

#### DO

- Class names → domain entities/nouns from the model (e.g. `GatherContextAction`, `BotConfig`, `Guardrails`).
- Method names → domain responsibilities/verbs (e.g. `inject_questions_and_evidence`, `load_trigger_words`).
- Test names → plain-English story descriptions readable aloud (`test_agent_loads_configuration_when_file_exists`).

```python
# Domain entity: 'Gather Context Action'
# Domain responsibility: 'Inject questions and evidence'

class GatherContextAction:
    def inject_questions_and_evidence(self) -> Instructions:
        ...

class ValidateRulesAction:
    def inject_behavior_specific_and_bot_rules(self) -> Instructions:
        ...

def test_agent_loads_configuration_when_file_exists(self, workspace_root):
    ...
```

#### DON'T

- Use generic technical terms not in the domain model.
- Name classes after infrastructure roles (`Loader`, `Manager`, `Handler`, `Service`, `StdioHandler`).
- Name methods with generic verbs that have no domain meaning (`execute_with_guardrails`, `process`, `handle_request`).
- Write test names that describe implementation rather than behavior.

```python
# WRONG: generic technical names
class Action:           # which action?
class Loader:           # not in domain
class Handler:          # not in domain

def execute_with_guardrails():  # domain says 'inject_questions_and_evidence'
def process():                  # too vague

def test_agt_init_sets_vars():  # abbreviations, implementation focus
```

### Rule: Use Domain Objects as Parameters

Pass **constructed domain objects** to test and helper functions — never raw IDs or bare primitives. Parameters must be named after their business role so each Given/When/Then step reads as a natural scenario in the domain language.

#### DO

- Pass real domain objects (`Cart`, `Order`, `User`) — not IDs or plain data.
- Name parameters after their business role (`cart`, `product`) — not their technical representation (`cart_id`, `product_id`).

```python
def test_adds_product_to_cart(self, workspace_root):
    # Given
    cart = given_cart_exists(workspace_root)
    product = given_product_is_available(workspace_root, 'item-a')
    # When
    when_product_is_added(cart, product)
    # Then
    then_cart_contains(cart, product)
```

#### DON'T

- Pass IDs or primitives where domain objects belong — steps become unreadable as business scenarios.

```python
def test_adds_product_to_cart(self, cart_id, product_id):
    given_cart_exists(cart_id)            # ID — not a business entity
    when_product_is_added(cart_id, product_id)
    then_cart_contains(cart_id, product_id)
```

﻿---
scanner: exact_variable_names_scanner.py
---

### Rule: Use Exact Variable Names

Use the **exact variable names** from the specification scenario in both the test code and the production code. When a scenario says `agent_name`, `workspace_root`, or `config_path`, use those exact identifiers — not abbreviations or synonyms. This keeps the traceability chain from spec → test → production intact.

#### DO

- Copy variable names verbatim from the scenario's Given/When/Then terminology.

```python
# Specification uses: agent_name, workspace_root, config_path
agent = Agent(agent_name='story_bot', workspace_root=workspace_root)
assert agent.config_path == workspace_root / 'agents' / 'base' / 'agent.json'
```

#### DON'T

- Shorten, abbreviate, or rename variables from the specification.

```python
# WRONG: different names from specification
agent = Agent(name='story_bot')          # spec says agent_name
agent = Agent(workspace=workspace_root)  # spec says workspace_root
assert agent.path == ...                 # spec says config_path
```

﻿---
scanner: given_when_then_helpers_scanner.py
---

### Rule: Use Given/When/Then Helpers

Use **reusable helper functions** for any inline code block of 4 or more lines. Place helpers at the right scope: story-level helpers inside the test class, sub-epic helpers at module level, and cross-epic helpers in a shared file. Name helpers with `given_`, `when_`, or `then_` prefixes when the domain language calls for it, but prioritise **domain-verb naming** over mechanical prefixes.

#### DO

- Extract 4+ line inline blocks to named helpers.
- Scope helpers to the level that needs them.

```python
def given_bot_config_exists(workspace: Path, name: str = 'story_bot') -> Path:
    return create_config_file(workspace, name)

def when_bot_instantiated(workspace: Path, name: str) -> Bot:
    return Bot(bot_name=name, workspace_root=workspace)

def then_bot_uses_correct_directories(bot: Bot, workspace: Path) -> None:
    assert bot.workspace_root == workspace
    assert bot.config_path.parent.exists()

class TestBotInitialization:
    def test_bot_initializes_with_config(self, workspace_root):
        given_bot_config_exists(workspace_root, 'story_bot')
        bot = when_bot_instantiated(workspace_root, 'story_bot')
        then_bot_uses_correct_directories(bot, workspace_root)
```

#### DON'T

- Leave 4+ line inline operations inside test methods.

```python
# WRONG: inline multi-line setup
def test_bot_initializes(self, tmp_path):
    config_dir = tmp_path / 'agents' / 'base'
    config_dir.mkdir(parents=True)
    config_file = config_dir / 'agent.json'
    config_file.write_text('{"name": "story_bot"}')
    # ... more inline code ...
```
<!-- execute_rules:bundle_rules:end -->
