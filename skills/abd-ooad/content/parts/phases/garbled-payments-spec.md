# Payments capability — draft notes (internal)

**Status:** mix of workshop sticky notes + email forwards; **not** reviewed for consistency. Owner TBD.

> **Note:** Intentionally raw **battle-test** input — not incrementally refined here. The **step** outputs (`nouns-verbs-rules-and-states.md` … `model-in-layers.md`) apply **continual refinement** and **`**newly added**`** per **[Domain model Markdown](../library/domain-model.md)**.

## What we need (high level)

The paymnts syhtrenmt has to take money from buyers and get it to sellers without us holding float longer than compliance allows. Local means same country / same rails as the merchant account; **global** means cross-border and FX may apply—we said FX is “someone else’s problem” in Q3 but legal wants us to show **mid rate snapshot** on receipts now.

All pmt types from the product matrix: card (debit/credit/prepaid), ACH-style bank pull where available, “instant” push-to-wallet, wire for B2B, and the crypto pilot **only** in regions where the checkbox in admin is green. Do **not** promise BNPL until Partner X signs; until then BNPL routes to “coming soon” screen.

Frontend has to **fulfgo** the happy path: user picks method, sees fees (if any), confirms, sees success or actionable failure. If the PSP needs redirect (3DS, bank login, etc.) we open browser / in-app webview—**online if necessary** to complete auth. After that, **fulfillment** of the order (digital vs physical) is **not** owned by payments team but we must emit `payment.settled` before warehouse picks for physical SKUs; for digital, sometimes we emit before download link—**check with Ops** (two conflicting emails on this).

## Rules that came up in meetings (unordered)

- Retry idempotency keys: client sends `Idempotency-Key` header; server must not double-charge. Someone wrote “keys expire after 24h” on the whiteboard; backend ticket says 72h—**align**.
- Partial capture: marketplace holds auth then captures less; remainder release—**only** for card rails that support it; otherwise full capture only.
- Refunds: full and partial; reason codes required for chargeback prep; SLA “as fast as rail allows” (not a number).
- If payer is in sanctioned country list, **block** before method selection UI (not after)—compliance doc v4.
- Subscriptions: out of scope for this phase except we need **webhook** shape so billing can subscribe later without renaming events.

## Local vs global (still fuzzy)

“Local” might mean: same **currency** as storefront OR same **merchant legal entity**—product used both definitions in different slides. Engineering assumption: **currency + merchant region** gate which PSP connector runs; global adds **FX quote id** on the intent object (nullable).

Tax: we display estimated tax on checkout; payments doesn’t calculate tax—**but** if payment fails after tax shown, cart must not double-apply coupons. (Cart team.)

## Failure modes (fragmentary)

timeouts, user closes webview, insufficient funds, issuer decline, fraud score block, velocity limit, mismatched billing zip, 3DS friction abandoned. Each should map to a **user-visible** message and a **log category** for support—not all mapped yet.

## Non-functional / misc

Audit: every state transition on the PaymentIntent (or whatever we call it—**Intent** vs **Session** naming not finalized) must be append-only log with actor `system|user|psp_webhook`.

Performance: p95 initiate &lt; 300ms excluding network—**from where** measured unclear.

Sample elements: we do **not** need a strict ordered sequence for the pilot demo; PM wants a **non ordered** sample flow list (browse → pay → fail → retry) to usability-test **without** implying that’s the only journey.

## Open questions

Who owns **dispute** lifecycle? Risk team says “merchant of record”; eng assumed “platform.”

Offline payments (cash at partner location): mentioned once; **not** in scope for MVP but field appears in schema—remove or hide?

---

*This document is intentionally inconsistent, typo-laden, and incomplete for OOAD / abd-ooad battle testing.*
