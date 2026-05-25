---
name: abd-clean-code
catalog_garden_tier: practice
catalog_garden_family: architecture-centric-engineering
catalog_garden_order: 60
catalogue_one_liner: >-
  Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS).
description: >-
  Write production code that implements story behavior using domain language,
  clean functions, explicit dependencies, and observable design. This skill
  covers the full quality bar for implementation code: single-responsibility
  functions and classes, intention-revealing names, explicit constructor
  injection, guard-clause control flow, domain exceptions, encapsulation, and
  DRY structure. Use it when writing any production module from scratch,
  reviewing code for quality, driving the GREEN phase of a TDD cycle, or
  refactoring to clean up debt. Produces Python or JavaScript/ES module output
  from templates and validates against embedded scanner-backed rules.
---
# abd-clean-code

## Purpose

Write production code that implements story behavior using **domain language**, **clean functions**, **explicit dependencies**, and **observable design**.

This skill produces real, runnable production modules — in Python or JavaScript — from whatever context is available: a story, acceptance criteria, a failing test, or a description of the behavior to implement. The output follows a consistent layout: one module per sub-epic area, one class per domain entity, functions under 20 lines, and all dependencies injected through the constructor.

The skill covers the full implementation quality bar: names that reveal intent, guard-clause control flow, no magic numbers, no swallowed exceptions, no hidden globals, encapsulated internals, and domain vocabulary throughout.

## When to use this skill

- You are writing **production code** to implement a story or acceptance criteria.
- You are in the **GREEN phase** of a TDD cycle — a test is failing and you need to make it pass.
- You are **reviewing code quality**: naming, size, dependencies, encapsulation, error handling.
- You are **refactoring** to remove duplication, flatten nesting, or separate concerns.
- You are **fixing a bug** and want the correct pattern before writing the fix.
- An agent is asked to "implement", "write the code for", "build the production module for", or "refactor".

---

## Agent Instructions

1. **Confirm language and framework** — If not stated, default to Python (stdlib only) or JavaScript (ES modules). Ask if the target is unclear.
2. **Identify the story, then declare names** — State the domain entity and the responsibilities the module will own before writing any code. Class names come from the domain model; method names come from domain responsibilities.
3. **Pick the matching template** from `templates/` — `clean-code.py` or `clean-code.js`. Emit code only; omit the `## Instructions` block from the template.
4. **Build** — One module per sub-epic area, one class per domain entity, functions under 20 lines, explicit constructor injection, private helpers prefixed with `_` or `#`.
5. **Validate** — Peer-review the output against the Rules section below before returning it. Fix any violation.
6. **Assembling this skill** — Reassemble with `bundle_rules_into_skill_md.py` after editing `rules/` or `templates/`.

---

## What is clean code?

Clean code reads like well-written prose. Every name answers "why does this exist?", every function does exactly one thing, and every dependency is visible at the construction site. You can change any one piece without surprising the rest.

Five properties that define clean production code:

- **Functions do one thing** — a calculation function calculates; it does not log, save, or send.
- **Names reveal intent** — `elapsed_time_in_days`, not `e`; `MILLISECONDS_PER_DAY`, not `86400000`.
- **Explicit dependencies** — every collaborator arrives through the constructor; no hidden globals.
- **Domain language** — class and method names come from the business model, not from technical patterns.
- **No hidden state** — internals are private; callers see behavior, not data.

---

## Core concepts

### Domain language

Class names are domain entities — the nouns from your story model: `Cart`, `Order`, `Product`, `Invoice`, `Inventory`. Method names are domain responsibilities — the verbs those entities own: `place_order`, `confirm`, `reserve`, `apply_loyalty_discount`. `Service`, `Calculator`, `Manager`, `Handler` are technical suffixes that hide what the code actually does. If a class is called `CheckoutService`, rename it to the entity doing the work — usually that is `Cart` (which places orders) and `Order` (which knows its own total).

**Wrong:** `CheckoutService.process_order(user, cart)` — a service acting on passive data objects.
**Right:** `cart.place_order()` — the Cart places its own order; the Order knows its own total.

### Function discipline

Every function has a **single responsibility** and stays under **20 lines**. Prefer **0-2 parameters**; use a dataclass or destructured object when more configuration is needed. Avoid boolean flag parameters — they are two hidden functions pretending to be one. Use **guard clauses** at the top to eliminate deep nesting: return early for invalid conditions, then write the happy path flat.

### Dependency injection

Pass every collaborator — repositories, mailers, loggers, external clients — through the **constructor**. Store them as private attributes (`_repo`, `_mailer`). Never reach for a global, and never construct a collaborator inside `__init__`. This makes every dependency visible, mockable in tests, and swappable without changing the class.

### Class design

Each class has **one reason to change** (Single Responsibility Principle). Keep classes under 200-300 lines. If a class calculates, persists, formats, and emails, it should be four classes. Expose **behavior** through domain methods, not raw data through public attributes. Hide implementation details behind `_private` helpers.

### Properties (and setters) over getters and setters

Prefer properties and property setters over explicit getters (`get_`/`is_`/`has_`) and setters (`set_`) when exposing derived, computed, or validated values. Use the language’s property feature (e.g., `@property` and `@<property>.setter` in Python, `get` and `set` accessors in JavaScript) to expose these as natural attributes, not as method calls. This allows callers to access and assign the value as an attribute (e.g., `order.total`, `user.is_active`, `profile.display_name = "Alex"`) rather than calling a function. Reserve methods for actions or functions that require parameters or have side effects.

**Wrong:**  
- `order.get_total()`  
- `user.is_active()`  
- `profile.set_display_name("Alex")`

**Right:**  
- `order.total`  
- `user.is_active`  
- `profile.display_name = "Alex"`

Make it obvious whether a member is a calculated value or an action by using properties for values, and verbs for actions. A property getter should never perform side effects—only calculate and return a value.

### Error handling

Define **domain exceptions** that extend the language's base error type and name them after what went wrong in the domain (`EmptyCartError`, `PaymentDeclinedError`). Never return `None` to signal failure — raise. Never swallow: if you catch an exception you cannot handle, log and re-raise. Isolate `try/except` blocks into dedicated functions so business logic stays clean.

---

## Example

```python
"""
cart.py

Domain area   : cart
Responsibilities: hold items, compute totals, place an order
"""
from __future__ import annotations
from dataclasses import dataclass

TAX_RATE = 0.13
LOYALTY_THRESHOLD = 1000


class EmptyCartError(Exception):
    """Raised when place_order() is called on an empty cart."""


class InvalidQuantityError(Exception):
    """Raised when a line item is added with qty < 1."""


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: float             # price lives on Product, not duplicated on LineItem


class LineItem:
    """A chosen quantity of a Product. Gets its price from the Product."""

    def __init__(self, product: Product, qty: int) -> None:
        if qty < 1:
            raise InvalidQuantityError(f"qty for '{product.sku}' must be >= 1")
        self._product = product
        self._qty = qty

    @property
    def extended_price(self) -> float:
        return round(self._product.price * self._qty, 2)


class Cart:
    """A shopping cart that owns its items and knows its own totals."""

    def __init__(self, owner) -> None:
        self._owner = owner
        self._items: list[LineItem] = []

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    @property
    def subtotal(self) -> float:
        return round(sum(i.extended_price for i in self._items), 2)

    def add(self, product: Product, qty: int) -> None:
        self._items.append(LineItem(product=product, qty=qty))

    def place_order(self) -> Order:
        if self.is_empty:
            raise EmptyCartError("Cannot place an order from an empty cart.")
        return Order(owner=self._owner, items=tuple(self._items))


class Order:
    """A placed order that owns its pricing and confirmation lifecycle."""

    def __init__(self, owner, items: tuple[LineItem, ...]) -> None:
        self._owner = owner
        self._items = items
        self._confirmed = False

    @property
    def subtotal(self) -> float:
        return round(sum(i.extended_price for i in self._items), 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * TAX_RATE, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)

    @property
    def is_confirmed(self) -> bool:
        return self._confirmed

    def confirm(self) -> None:
        if self._confirmed:
            raise RuntimeError("Order is already confirmed.")
        self._confirmed = True
```

---

## The shape of good production code

```
<domain_entity_snake_case>.py
  Module docstring: domain entity + responsibilities covered
  Imports  (stdlib -> third-party -> local)

  DOMAIN CONSTANTS section
    TAX_RATE = 0.13          <- named constant, no magic numbers
    LOYALTY_THRESHOLD = 1000

  DOMAIN EXCEPTIONS section
    class EmptyCartError(Exception): ...
    class InvalidQuantityError(Exception): ...

  CLASS: <DomainEntity>      <- Cart, Order, Product, Invoice -- not CheckoutService
    Docstring: one sentence on what this entity is responsible for.

    @property                <- what this entity IS / CONTAINS
      is_empty
      subtotal
      total

    public methods           <- what this entity CAN DO, under 20 lines each
      def add(product, qty)
      def remove(sku)
      def place_order()
      def confirm()

    _private helpers         <- implementation details, under 20 lines each
      def _apply_loyalty_discount(amount)
      def _assert_not_already_confirmed()
```

---

<!-- execute_rules:bundle_rules:begin -->
---
scanner: function_single_responsibility_scanner.py
---

### Rule: Keep Functions Single Responsibility

Functions do one thing. No hidden side effects, no mixing business logic with I/O or mutations.

#### DO

- Separate pure calculations from orchestration.
- Each function has one reason to change.
- Side effects live in dedicated orchestration functions.

```python
def subtotal(items: list) -> float:
    return sum(i.price * i.qty for i in items)  # pure calculation

def checkout(user, cart, services):
    sub = subtotal(cart.items)                  # calls pure helper
    services.logger.info('checkout', extra={'user_id': user.id})
    return sub
```

```javascript
export function subtotal(items) {
  return items.reduce((s, i) => s + i.price * i.qty, 0);  // pure calculation
}

export async function checkout({ user, cart, services }) {
  const sub = subtotal(cart.items);             // calls pure helper
  services.logger.info('checkout', { userId: user.id });
  return sub;
}
```

#### DON'T

- Mix business logic with logging, I/O, or mutations in the same function.

```python
def full_name(user):
    print("User:", user.id)       # WRONG: hidden side effect in calculation
    metrics.append(user.id)       # WRONG: state mutation in pure function
    return f"{user.first} {user.last}"
```

```javascript
function fullName(user) {
  console.log('User:', user.id);  // WRONG: hidden side effect
  return `${user.first} ${user.last}`;
}
```

---
scanner: function_size_scanner.py
---

### Rule: Keep Functions Small and Focused

Keep functions under 20 lines. Extract complex logic into named helpers.

#### DO

- Functions fit in one screen.
- Extract calculation, validation, and persistence into named helpers.

```python
TAX_RATE = 0.13

def total_with_tax(subtotal: float, tax_rate: float = TAX_RATE) -> float:
    return round(subtotal * (1 + tax_rate), 2)

def checkout(user, cart, services):
    sub = subtotal(cart.items)
    total = total_with_tax(sub)
    invoice = save_invoice(user, total, cart.items)
    return invoice, total
```

```javascript
const TAX_RATE = 0.13;

export function totalWithTax(subtotal, tax = TAX_RATE) {
  return Math.round(subtotal * (1 + tax) * 100) / 100;
}

export async function checkout({ user, cart, services }) {
  const sub = subtotal(cart.items);
  const total = totalWithTax(sub);
  const invoice = await saveInvoice(user, total, cart);
  return { invoice, total };
}
```

#### DON'T

- Write functions that inline calculation, persistence, email, and logging together.

```python
def checkout(user, cart):
    subtotal = sum(i.price * i.qty for i in cart.items)  # WRONG: mixed abstraction levels
    total = round(subtotal * 1.13, 2)
    db.invoices.insert({'user_id': user.id, 'total': total})
    for it in cart.items:
        db.products.decrement(it.sku, it.qty)
    email.send(user.email, f"Thanks for ${total}")
    print('checkout complete')
    return total
```

```javascript
async function checkout(user, cart) {
  let subtotal = 0;
  for (const i of cart.items) subtotal += i.price * i.qty;  // WRONG: mixed levels
  const total = subtotal * 1.13;
  await db.invoices.insert({ userId: user.id, total });
  for (const it of cart.items) await db.products.decrement(it.sku, it.qty);
  await email.send(user.email, `Thanks for $${total}`);
  return total;
}
```

---
scanner: clear_parameters_scanner.py
---

### Rule: Use Clear Function Parameters

Prefer 0-2 parameters. Use parameter objects for more. Avoid boolean flag parameters.

#### DO

- Use a dataclass or destructured object for complex configuration.
- Separate export functions instead of switching on a flag.

```python
from dataclasses import dataclass

@dataclass
class ConnectionOptions:
    host: str
    port: int
    timeout_ms: int = 2000

def connect(opts: ConnectionOptions): ...

def export_csv(data): return to_csv(data)   # separate functions, not flags
def export_json(data): return to_json(data)
```

```javascript
export function connect({ host, port, timeoutMs = 2000 }) {
  // clear, named parameters
}

export function exportCsv(data) { return toCsv(data); }   // separate, not flag-based
export function exportJson(data) { return toJson(data); }
```

#### DON'T

- Pass boolean flags that change function behavior.
- Exceed 3 positional parameters.

```python
def export_report(data, is_csv: bool):         # WRONG: boolean flag
    return to_csv(data) if is_csv else to_json(data)

def render(chart, dark, pretty, borders): ...  # WRONG: too many parameters
```

```javascript
function exportReport(data, isCsv) {           // WRONG: boolean flag
  return isCsv ? toCsv(data) : toJson(data);
}

function render(chart, dark, pretty, borders) { }  // WRONG: too many parameters
```

---
scanner: simplify_control_flow_scanner.py
---

### Rule: Simplify Control Flow

Use guard clauses to reduce nesting. Return early for invalid or boundary conditions.

#### DO

- Guard clauses at the top of the function.
- Flat structure, maximum 2 levels of nesting.

```python
def price_for(user, plan):
    if not user or not plan: return 0       # guard clause
    if user.is_student: return plan.base * 0.5
    return plan.base
```

```javascript
function priceFor(user, plan) {
  if (!user || !plan) return 0;             // guard clause
  if (user.isStudent) return plan.base * 0.5;
  return plan.base;
}
```

#### DON'T

- Nest if statements 3 or more levels deep.
- Use else when an early return makes it unnecessary.

```python
def price_for(user, plan):
    if user is not None:          # WRONG: deep nesting
        if plan is not None:
            if user.is_student:
                return plan.base * 0.5
            else:
                return plan.base
    return 0
```

```javascript
function priceFor(user, plan) {
  if (user) {                     // WRONG: deep nesting
    if (plan) {
      if (user.isStudent) return plan.base * 0.5;
      return plan.base;
    }
  }
  return 0;
}
```

---
scanner: intention_revealing_names_scanner.py
---

### Rule: Use Intention-Revealing Names

Names answer "why does this exist?". Avoid abbreviations, single letters, and undescriptive identifiers.

#### DO

- Named constants for every magic number.
- Variable names that reveal purpose, unit, and domain context.

```python
MILLISECONDS_PER_DAY = 86_400_000

elapsed_time_in_days = timer.elapsed_ms() / MILLISECONDS_PER_DAY
```

```javascript
const MILLISECONDS_PER_DAY = 86_400_000;

const elapsedTimeInDays = timer.elapsedMs / MILLISECONDS_PER_DAY;
```

#### DON'T

- Use single-letter variable names outside of trivial loop indices.
- Abbreviate names that carry domain meaning.

```python
d = 86400000                                  # WRONG: meaningless name, magic number
elapsed = timer.elapsed_ms() / 86400000       # WRONG: no context on unit
```

```javascript
const d = 86400000;                           // WRONG: meaningless name, magic number
const elapsed = timer.elapsedMs / 86400000;   // WRONG: no context
```

---
scanner: consistent_naming_scanner.py
---

### Rule: Use Consistent Naming

One word per concept across the codebase. Pick a verb and use it everywhere for the same operation.

#### DO

- All retrieval functions share the same prefix across the codebase.

```python
def get_user(user_id): ...
def get_order(order_id): ...
def get_product(sku): ...
```

```javascript
function getUser(userId) { }
function getOrder(orderId) { }
function getProduct(sku) { }
```

#### DON'T

- Mix `get_`, `fetch_`, and `retrieve_` for the same concept in the same codebase.

```python
def get_user(user_id): ...      # WRONG: inconsistent verb usage
def fetch_order(order_id): ...
def retrieve_product(sku): ...
```

```javascript
function getUser(userId) { }        // WRONG: mixed terms for retrieval
function fetchOrder(orderId) { }
function retrieveProduct(sku) { }
```

---
scanner: meaningful_context_scanner.py
---

### Rule: Provide Meaningful Context

Replace magic numbers and inline literals with named constants that explain their purpose and unit.

#### DO

- Declare a named constant for every value with business meaning.

```python
ADULT_AGE = 18
TAX_RATE = 0.13

def is_adult(age: int) -> bool:
    return age >= ADULT_AGE
```

```javascript
const ADULT_AGE = 18;
const TAX_RATE = 0.13;

function isAdult(age) {
  return age >= ADULT_AGE;
}
```

#### DON'T

- Inline unexplained numbers or business constants.

```python
def is_adult(age):
    return age >= 18          # WRONG: magic number with no context

import time
time.sleep(86400000)          # WRONG: what unit? what meaning?
```

```javascript
function isAdult(age) {
  return age >= 18;           // WRONG: magic number with no context
}

const total = subtotal * 1.13;  // WRONG: unexplained magic number
```

---
scanner: duplication_scanner.py
---

### Rule: Eliminate Duplication

Extract repeated logic into reusable functions. Do not repeat yourself.

#### DO

- One canonical function for each repeated calculation or operation.

```python
def calculate_subtotal(items):
    return sum(i.price * i.qty for i in items)

subtotal_a = calculate_subtotal(items_a)
subtotal_b = calculate_subtotal(items_b)
```

```javascript
function calculateSubtotal(items) {
  return items.reduce((sum, i) => sum + i.price * i.qty, 0);
}

const subtotalA = calculateSubtotal(itemsA);
const subtotalB = calculateSubtotal(itemsB);
```

#### DON'T

- Copy-paste the same logic in multiple places.

```python
subtotal_a = 0                    # WRONG: duplicated logic
for i in items_a:
    subtotal_a += i.price * i.qty

subtotal_b = 0                    # WRONG: same logic repeated
for i in items_b:
    subtotal_b += i.price * i.qty
```

```javascript
let subtotalA = 0;                // WRONG: duplicated logic
for (const i of itemsA) subtotalA += i.price * i.qty;

let subtotalB = 0;                // WRONG: same logic repeated
for (const i of itemsB) subtotalB += i.price * i.qty;
```

---
scanner: separate_concerns_scanner.py
---

### Rule: Separate Concerns

Keep pure calculations separate from side effects. Logging, I/O, and mutations belong in dedicated functions.

#### DO

- Pure functions return values without touching external state.
- Side effects are isolated in dedicated orchestration functions.

```python
def full_name(user) -> str:
    return f"{user.first} {user.last}"          # pure: no side effects

def greet(user, logger) -> str:
    logger.debug("Greeting", extra={"user_id": user.id})
    return f"Hello, {full_name(user)}!"
```

```javascript
function fullName(user) {
  return `${user.first} ${user.last}`;          // pure: no side effects
}

function greet(user, { logger }) {
  logger.debug({ userId: user.id });
  return `Hello, ${fullName(user)}!`;
}
```

#### DON'T

- Log, mutate, or perform I/O inside a calculation function.

```python
def discount(total):
    d = total * 0.1 if total > 100 else 0
    logging.info("discount=%s", d)              # WRONG: side effect in calculation
    return d
```

```javascript
function discount(total) {
  const d = total > 100 ? total * 0.1 : 0;
  console.log('discount:', d);                  // WRONG: side effect in calculation
  return d;
}
```

---
scanner: abstraction_levels_scanner.py
---

### Rule: Maintain Abstraction Levels

Step down one abstraction level at a time. High-level functions call medium-level helpers; never mix raw SQL or HTTP with business logic.

#### DO

- High-level orchestration calls named helpers at the next level down.

```python
def checkout(user, cart, services):
    sub = subtotal(cart.items)            # medium-level calculation
    total = total_with_tax(sub)           # medium-level calculation
    invoice = save_invoice(user, total, cart.items)  # medium-level persistence
    return invoice, total
```

```javascript
export async function checkout({ user, cart, taxRate, services }) {
  const sub = subtotal(cart.items);           // medium-level calculation
  const total = totalWithTax(sub, taxRate);   // medium-level calculation
  const invoice = await saveInvoice(user, total, cart);  // medium-level persistence
  return { invoice, total };
}
```

#### DON'T

- Mix raw SQL or low-level I/O detail directly in high-level orchestration.

```python
def checkout(user, cart):
    sub = sum(i.price * i.qty for i in cart.items)   # WRONG: low-level detail
    db.execute("INSERT INTO invoices (user_id, total) VALUES (?, ?)", user.id, sub)
```

```javascript
async function checkout(user, cart) {
  const sub = cart.items.reduce((s, i) => s + i.price * i.qty, 0);  // WRONG: low-level
  await db.execute("INSERT INTO invoices...");       // WRONG: SQL in orchestration
}
```

---
scanner: exception_handling_scanner.py
---

### Rule: Use Exceptions Properly

Use domain-specific exceptions with informative messages. Never return None to signal an error condition.

#### DO

- Define domain exceptions that extend built-in error types.
- Include the original cause when re-raising to preserve the stack.

```python
class ParseError(ValueError):
    pass

def parse_json(payload: str) -> dict:
    try:
        return json.loads(payload)
    except json.JSONDecodeError as e:
        raise ParseError("Invalid JSON") from e   # preserves cause
```

```javascript
class ParseError extends Error { }

function parseJson(payload) {
  try {
    return JSON.parse(payload);
  } catch (e) {
    throw new ParseError('Invalid JSON');         // informative, domain-named
  }
}
```

#### DON'T

- Return None to signal failure.
- Use bare except or silent catch-all blocks.

```python
def load(payload):
    try:
        return json.loads(payload)
    except:                     # WRONG: bare except catches everything
        return None             # WRONG: silent failure, caller gets None with no context
```

```javascript
function load(payload) {
  try {
    return JSON.parse(payload);
  } catch (e) {
    /* ignore */                // WRONG: silent failure, caller has no idea what happened
  }
}
```

---
scanner: swallowed_exceptions_scanner.py
---

### Rule: Never Swallow Exceptions

Never silently swallow exceptions. Always log and re-raise, re-raise, or convert to a domain exception.

#### DO

- Log and re-raise when you cannot fully handle the error.
- Convert to a domain exception with context to help the caller.

```python
def parse_request(raw_data):
    try:
        return _parse_json(raw_data)
    except ParseError as e:
        logger.error("Parse failed", exc_info=e)
        raise
```

```javascript
async function parseRequest(rawData) {
  try {
    return await _parseJson(rawData);
  } catch (err) {
    logger.error('Parse failed', err);
    throw err;
  }
}
```

#### DON'T

- Use bare `except: pass` or an empty catch block.
- Catch exceptions and return None.

```python
try:
    result = risky_operation()
except:                         # WRONG: swallows everything including SystemExit
    pass                        # WRONG: silent failure, caller has no signal
```

```javascript
try {
  result = riskyOperation();
} catch (e) {
  // WRONG: swallowed, caller never knows
}
```

---
scanner: explicit_dependencies_scanner.py
---

### Rule: Use Explicit Dependencies

Pass all dependencies through the constructor. No hidden globals, no constructing collaborators inside __init__.

#### DO

- Accept every dependency as a constructor parameter.
- Store dependencies as private attributes.

```python
class CheckoutService:
    def __init__(self, invoice_repo, inventory, mailer):
        self._invoice_repo = invoice_repo   # injected
        self._inventory = inventory         # injected
        self._mailer = mailer               # injected
```

```javascript
export class CheckoutService {
  constructor(invoiceRepo, inventory, mailer) {
    this._invoiceRepo = invoiceRepo;        // injected
    this._inventory = inventory;            // injected
    this._mailer = mailer;                  // injected
  }
}
```

#### DON'T

- Reach for global state inside the constructor.
- Construct collaborator objects inside __init__ or constructor.

```python
class CheckoutService:
    def __init__(self):
        self.repo = global_invoice_repo     # WRONG: hidden global dependency
        self.inventory = Inventory()        # WRONG: hidden construction, untestable
```

```javascript
export class CheckoutService {
  constructor() {
    this.repo = globalInvoiceRepo;          // WRONG: hidden global dependency
    this.inventory = new Inventory();       // WRONG: hidden construction, untestable
  }
}
```

---
scanner: property_encapsulation_code_scanner.py
---

### Rule: Enforce Encapsulation

Hide implementation details. Private attributes use `_` prefix (Python) or `#` private fields (JS). Expose domain behavior, not raw data.

#### DO

- Prefix implementation details with `_` or use `#` private fields.
- Expose behavior through domain methods, not internal attributes.

```python
class Inventory:
    def __init__(self, repo):
        self._repo = repo                   # private

    def adjust_many(self, changes: list):
        for sku, delta in changes:
            self._adjust_one(sku, delta)    # private helper

    def _adjust_one(self, sku: str, delta: int):
        self._repo.update_stock(sku, delta)
```

```javascript
export class Inventory {
  #repo;                                    // private field

  constructor(repo) {
    this.#repo = repo;
  }

  async adjustMany(changes) {
    for (const { sku, delta } of changes) {
      await this.#adjustOne(sku, delta);    // private helper
    }
  }
}
```

#### DON'T

- Expose internal attributes as public fields.
- Let callers access or mutate implementation details.

```python
class Inventory:
    def __init__(self):
        self.repo = Repository()            # WRONG: public implementation detail
        self.cache = {}                     # WRONG: exposed internal state
```

```javascript
export class Inventory {
  constructor() {
    this.repo = new Repository();           // WRONG: public implementation detail
    this.cache = {};                        // WRONG: exposed internal state
  }
}
```

---
scanner: single_responsibility_scanner.py
---

### Rule: Keep Classes Single Responsibility

Each class has one reason to change. Split classes that calculate, persist, and notify into dedicated collaborators.

#### DO

- One class per domain responsibility.
- Separate repository, calculator, and notifier roles.

```python
class InvoiceRepository:                    # focused on persistence
    def save(self, invoice): ...
    def find_by_id(self, invoice_id): ...

class InvoiceCalculator:                    # focused on calculation
    def calculate_total(self, items): ...
    def apply_discount(self, total, discount): ...
```

```javascript
export class InvoiceRepository {            // focused on persistence
  async save(invoice) { }
  async findById(invoiceId) { }
}

export class InvoiceCalculator {            // focused on calculation
  calculateTotal(items) { }
  applyDiscount(total, discount) { }
}
```

#### DON'T

- Build classes that calculate, persist, notify, and format.

```python
class Invoice:                              # WRONG: multiple responsibilities
    def calculate_total(self): ...          # calculation
    def save_to_db(self): ...               # persistence
    def send_email(self): ...               # notification
    def format_pdf(self): ...              # formatting
```

```javascript
export class Invoice {                      // WRONG: multiple responsibilities
  calculateTotal() { }                      // calculation
  saveToDB() { }                            // persistence
  sendEmail() { }                           // notification
  formatPDF() { }                           // formatting
}
```

---
scanner: domain_language_code_scanner.py
---

### Rule: Use Domain Language

Class names are domain entities. Method names are domain responsibilities. Avoid generic names like Manager, Handler, process(), and execute().

#### DO

- Name classes after domain entities from the ubiquitous language.
- Name methods after domain responsibilities, not technical verbs.

```python
class CheckoutService:
    def __init__(self, invoice_repo, inventory, mailer):
        self._invoice_repo = invoice_repo
        self._inventory = inventory
        self._mailer = mailer

    def process_order(self, user, cart): ...
    def apply_loyalty_discount(self, user, total): ...
```

```javascript
export class CheckoutService {
  constructor(invoiceRepo, inventory, mailer) {
    this._invoiceRepo = invoiceRepo;
    this._inventory = inventory;
    this._mailer = mailer;
  }

  async processOrder(user, cart) { }
  applyLoyaltyDiscount(user, total) { }
}
```

#### DON'T

- Use generic class names: Manager, Handler, Helper, Processor, Util.
- Use generic method names: process(), handle(), execute(), run(), do().

```python
class Manager:                              # WRONG: no domain meaning
    def process(self, data): ...            # WRONG: too generic, hides intent
    def handle(self, event): ...
```

```javascript
export class Handler {                      // WRONG: no domain meaning
  execute(data) { }                         // WRONG: too generic, hides intent
  run(event) { }
}
```

---
scanner: useless_comments_scanner.py
---

### Rule: Stop Writing Useless Comments

Comments should explain WHY, not WHAT. The code already shows what it does. Delete noise comments and commented-out code.

#### DO

- Legal notices.
- Explanations for non-obvious algorithms.
- Actionable TODOs with context.

```python
# Copyright 2025 Company Name

# Newton-Raphson approximation for 1/sqrt(x); see Quake III Arena source
def fast_inverse_sqrt(x):
    ...

# TODO: Replace with paginated query when dataset exceeds 10k rows
def load_all_orders():
    ...
```

```javascript
// Copyright 2025 Company Name

// Newton-Raphson approximation for 1/sqrt(x); see Quake III Arena source
function fastInverseSqrt(x) {
  // ...
}

// TODO: Replace with paginated query when dataset exceeds 10k rows
function loadAllOrders() { }
```

#### DON'T

- Write comments that restate what the code already says.
- Leave commented-out code in the codebase.
- Add attribution comments.

```python
# i = 0  # initialize counter
i = 0

# def old_process(data):  # WRONG: commented-out code as backup
#     return legacy(data)
def process(data):
    return transform(data)
```

```javascript
let i = 0;  // initialize counter      // WRONG: noise comment

// const oldResult = legacyTransform(data);  // WRONG: commented-out code
// const newResult = transform(data);
function process(data) {
  return transform(data);
}
```
<!-- execute_rules:bundle_rules:end -->
