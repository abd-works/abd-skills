# Rule: Constraints are modeled as types, not prose

**Scanner:** Manual review

Every domain constraint that restricts a property's value, format, or identity **must be represented structurally** — as a named type or subtype — not as a text invariant hanging on another class. If you find yourself writing an invariant that says "X is always Y" or "X must match format Z," that constraint belongs on its own type.

This applies to:
- **Inherited properties** narrowed by a child class — introduce a subtype of the inherited type (e.g., `TaxCurrency : Currency`)
- **Fixed-value properties** — a property locked to one value gets a constrained type (e.g., currency is always USD → `TaxCurrency`)
- **Format-constrained identifiers** — a reference with a specific format gets its own type (e.g., TAX-YYYY-XXXXXX → `TaxReferenceNumber : ReferenceNumber`)
- **Restricted relationships** — a property whose target is narrower than the declared type gets a subtype (e.g., destination is always a tax jurisdiction → `TaxDestination : Destination`)
- **Role-equivalent properties** — when a child class introduces a property under a different name that fills the same role as a parent property, its type must still inherit from the parent's property type (e.g., ACHPayment has `recipient: Recipient` which fills the role of `destination: Destination` → `Recipient : Destination`)

The test: if you can't point to a class that owns the constraint, the constraint isn't modeled.

## DO

```markdown
### **TaxPayment : Payment**

TaxPayment(TaxJurisdiction, FromAccount, Money, EffectiveDate, TaxType, TaxPeriod, EIN, LegalName)
------
destination: TaxDestination
currency: TaxCurrency
...
----
generateReferenceNumber(): TaxReferenceNumber

### **TaxDestination : Destination**

------
jurisdiction: TaxJurisdiction
----
	Invariant: destination is always the tax jurisdiction routed through EFTPS

### **TaxCurrency : Currency**

------
----
	Invariant: always USD

### **TaxReferenceNumber : ReferenceNumber**

------
----
	Invariant: format is TAX-YYYY-XXXXXX
```

Each constraint is owned by its own type. The type inherits from the generic base and narrows it. The child class declares the constrained type — not the generic one.

```markdown
### **ACHPayment : Payment**

ACHPayment(Recipient, FromAccount, Money, Currency, EffectiveDate, SECCode, TransactionCode)
------
recipient: Recipient
currency: ACHCurrency
...

### **Recipient : Destination**

Recipient(ProfileName, RecipientType, RecipientName, RoutingNumber, AccountNumber, AccountType, RDFICountry)
------
profileName: ProfileName
routingNumber: RoutingNumber
accountNumber: AccountNumber
...
```

The ACH domain calls it "recipient" — but it fills the same role as `destination` on the parent. `Recipient` inherits from `Destination` so the type hierarchy stays connected.

## DO NOT

```markdown
### **TaxPayment : Payment**

TaxPayment(TaxJurisdiction, FromAccount, Money, EffectiveDate, TaxType, TaxPeriod, EIN, LegalName)
------
jurisdiction: TaxJurisdiction
taxType: TaxType
...
	Invariant: currency is always USD
	Invariant: destination is always the tax jurisdiction via EFTPS
	Invariant: reference number format is TAX-YYYY-XXXXXX
----
```

Text invariants dumped on the parent with no backing type. The constraint exists as documentation, not as a model element. Nothing in the type system distinguishes `Currency` on TaxPayment from `Currency` on any other Payment. The diagram shows no class, no edge, no structure — just a line of italic text in the wrong box.

```markdown
### **ACHPayment : Payment**

ACHPayment(Recipient, FromAccount, Money, Currency, EffectiveDate, SECCode, TransactionCode)
------
recipient: Recipient
...

### **Recipient**

Recipient(ProfileName, ...)
------
...
```

`Recipient` has account numbers, routing numbers, and account types — it IS the ACH destination — but nothing in the type system connects it to `Destination`. The inheritance hierarchy is broken: code that processes `Payment.destination` cannot see that an ACH payment's recipient is a destination. The domain relationship exists only in the developer's head.

## Principle

A constraint without a type is an assertion without enforcement. If the domain says "this is always X" or "this must be in format Y," that's a modeling decision — model it. Create the subtype. Show the inheritance edge. Make the constraint visible in the structure, not buried in prose.

## On the diagram

Each constrained type appears as its own class cell with:
- Title showing inheritance: `TaxDestination : Destination`
- The constraint in the invariants compartment
- An inheritance edge (hollow triangle) pointing to the base type
- An association edge from the owning class to the constrained type

**Source:** Engagement convention (domain-model skill).
