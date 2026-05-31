## Module: [Order]

Scope: Guest checkout, billing, StripeWave payment, order confirmation email, and store employee click-and-collect fulfillment. Increment 2 checkout and pickup.

**Core terms**:
- guest checkout
- billing address
- payment method
- StripeWave
- order confirmation
- click-and-collect order
- order fulfillment

---

**Ref â€” Engagement scope (checkout spine)**
Source: context/CONTEXT.md
Locator: lines 8, 13
Extract: partial
Part: pay → pickup spine; guest checkout only (accounts out of scope).

**Ref â€” Increment 2 checkout and pickup stories**
Source: context/stories/thin-slicing.md
Locator: lines 38–44
Extract: partial
Part: Checkout, payment, confirmation, and store employee pickup stories.

**Ref â€” Checkout & Payment sub-epic**
Source: context/stories/story-graph.json
Locator: epics[2].sub_epics[1] "Checkout & Payment"
Extract: partial
Part: Guest checkout through Confirm Order and Send Confirmation Email.

**Ref â€” Store Fulfillment sub-epic**
Source: context/stories/story-graph.json
Locator: epics[2].sub_epics[2] "Store Fulfillment"
Extract: whole
