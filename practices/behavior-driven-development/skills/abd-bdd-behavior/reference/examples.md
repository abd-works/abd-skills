# Examples — abd-bdd-behavior

## Worked example: Voucher feature

**Inputs used:**
- `story-map.md` — sub-epic: `Redeem Voucher`
- `domain-language.md` — concepts: Voucher, Discount, Order, Customer
- `domain-model.md` — Voucher: validates eligibility, applies discount, tracks redemption state
- `acceptance-criteria.md` — AC for stories in the `Redeem Voucher` sub-epic

**Correct scaffold — `voucher-behavior.md`**

```
Redeem Voucher
  Voucher
    Redemption
      should apply a percentage discount to eligible items
      should apply a fixed-amount discount to the order total
      should reject a voucher code that does not exist
      should reject a voucher past its expiry date
      should reject a voucher already redeemed
    Eligibility
      should only allow redemption by the customer it was issued to
      should refuse a voucher applied to an ineligible product category
  Order
    Display
      should show the saving amount on the order summary
      should show the original price alongside the discounted price
```

Why this is right:
- The top-level describe (`Redeem Voucher`) is the sub-epic from the story map
- Nested describes (`Voucher`, `Order`) are concepts from the domain language
- Inner describes (`Redemption`, `Eligibility`, `Display`) are states and groupings from the domain model
- All leaf lines start with `should`
- No code syntax anywhere
- A non-technical stakeholder can read every line without asking what it means
- Each leaf traces to a story or acceptance criterion in the `Redeem Voucher` sub-epic

## Counter-example — what not to write

```
VoucherService
  applyVoucher
    calls calculateDiscount on DiscountCalculator
    throws VoucherExpiredException when TTL exceeded
```

Why this is wrong:
- `VoucherService` is an implementation class, not a sub-epic or domain concept
- `applyVoucher` is a method name, not a concept grouping from the domain language
- Leaf lines describe implementation detail, not observable behavior
- No `should` prefix on any leaf
- Nothing traces to a story or acceptance criterion
