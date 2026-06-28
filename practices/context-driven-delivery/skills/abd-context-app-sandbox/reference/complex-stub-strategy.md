# Complex Stub Strategy

## When simple enumeration is not enough

Simple stubbing works when external services are few, their interfaces are obvious from
the call sites, and their return shapes do not drive branching UI logic.

**Complex stubbing** is required when any of the following are true:

- The application has **five or more** distinct external services.
- One or more stubs must return **domain-shaped data** (e.g. a `Customer` object with
  nested fields) that drives routing, conditional rendering, or step-machine transitions.
- An external service controls **authentication state** that gates which screens are
  reachable (e.g. Cognito session token → onboarding step redirect).
- An external service supplies **feature flags** that enable or disable entire flows
  (e.g. GrowthBook → Persona KYC on/off).
- The correct hardcoded values for stubs are **not obvious from the call site alone** —
  you need to understand the domain to know what a realistic response looks like.

In these situations, jumping straight to stub authoring produces stubs that are either
too thin (returning empty objects that crash downstream components) or wrong (returning
shapes that do not match what the app actually expects).

---

## The deliberate strategy: Discover → Explore → Stub

Before writing any stub file for a complex application, the session checklist **must**
include all three of the following discrete steps — in order. They are not optional and
cannot be collapsed into a single checkbox.

---

### Mandatory pre-stub step 1 — Story mapping (minimal stub-focus pass)

Run a minimal story-mapping pass focused entirely on which external services are touched
by each user activity and what those services must return for the activity to advance.

**What to produce** (`docs/stubs/story-map.md`):

- List each user activity (e.g. Sign Up, Verify Identity, Add Payment, Activate SIM).
- For each activity: which external service is called, at which step, and what the
  minimum response shape is (field names only — no implementation yet).
- Flag any activity where the response drives a branch (e.g. `customer.status ===
  "active"` → redirect to dashboard).

This step answers: **"Which stubs are needed, and what must each one return for the
flow to advance?"**

---

### Mandatory pre-stub step 2 — Acceptance criteria (minimal stub-focus pass)

Run a minimal acceptance criteria pass to surface the observable outcomes that each
stub response must enable. This is the "so what" layer: given the stub returns X, the
app must do Y.

**What to produce** (`docs/stubs/acceptance-criteria.md`):

- For each user activity from the story map, write 2–4 acceptance criteria in plain
  language (not Gherkin yet).
- Each criterion names: the stub value that triggers it, the observable outcome, and
  the screen or component it is visible on.

Example:
> **Sign Up — Cognito stub returns `{ isSignUpComplete: true }`**
> → User sees the email verification screen (not the sign-up form)
> → "Check your email" heading is present

This step answers: **"What does the app visibly do in response to each stub return?"**

---

### Mandatory pre-stub step 3 — Domain language (minimal stub-focus pass)

Run a minimal domain language pass to establish the names and minimum fields of every
domain object that crosses a stub boundary.

**What to produce** (`docs/stubs/domain-glossary.md`):

- For each domain term that appears in an external service response
  (e.g. `Customer`, `Voucher`, `Inventory`, `Plan`):
  - List the minimum fields the UI reads from it (field name, type, example value).
  - Note which screen or component reads each field.
  - Note whether the field drives routing, conditional rendering, or a step transition.

This step answers: **"What exact shape must each stub return to produce realistic,
non-crashing behaviour?"**

---

### Step 4 — Stub authoring (only after all three steps above are complete)

Only after the story map, acceptance criteria, and domain glossary are written, proceed
to the standard sandbox enumeration:

1. Enumerate candidates (informed by the story map).
2. Classify each (external vs in-scope).
3. **Author stubs with domain-shaped return values** drawn from the domain glossary —
   not empty objects or `{}`.
4. For stateful stubs, cover the minimum fixture set: unauthenticated,
   authenticated-no-data, and authenticated-with-data.
5. Start the application and run the smoke test.

---

## Output locations

| Artifact | Path |
|----------|------|
| Stub-focused story map | `docs/stubs/story-map.md` |
| Domain glossary (stub fields) | `docs/stubs/domain-glossary.md` |
| Stub inventory | `docs/stubs/stub-inventory.md` |

---

## Trigger

Apply this strategy automatically when the enumeration step (step 1 of the standard
sandbox process) identifies **five or more distinct external services**, or when any
single stub must return a nested domain object with more than three fields.

Do not skip to stub authoring until the story map and domain glossary are written.
