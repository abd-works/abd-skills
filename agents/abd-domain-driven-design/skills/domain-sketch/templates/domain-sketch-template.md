<!--
  domain-sketch template — shows the growing module file shape AFTER domain-sketch enrichment.

  The file already exists at state: key-abstractions.
  This skill enriches it in place. Key changes this phase makes:

    1. Adds #### Domain Sketch under each ### term — verb-led behavior bullets and
       an optional role sentence describing what the term is for and who it works with
    2. Adds or extends #### Decisions made at the ## KA level and/or ### term level
    3. Deduplicates #### References across terms within the same ## KA
       (remove a ref from a ### term if the identical ref already appears in another
       ### term under the same ## KA; keep it on the first term that needs it)
    4. Adds new **Ref —** entries for any behavior bullet not yet cited
    5. Bumps state to domain-sketch

  Contract:
    - Everything from UDL and KA stages stays unchanged:
        #### Domain Language bullets — never touched
        ## KA prose definitions — never touched
        #### References already present — only deduplicated (removed from later
        terms when identical ref exists earlier in the same ## KA block)
    - #### Domain Sketch is NEW — added under each ### term
    - Subtypes use the heading form ### SubtypeName *is a type of* BaseName
      and appear under the same ## KA as their base term
    - No separate ## Domain logic section
    - No ---- behavior separators, no ----- collaboration separators
    - No concept role paragraphs as standalone text blocks outside #### sections
-->

---
state: domain-sketch
---

# Module: [{{ModuleName}}]

Scope: {{scope from partition — unchanged}}

**Core terms**:
- {{term1}}
- {{term2}}
- …

**Moved to other modules**:
- {{moved_term}} → {{DestinationModule}}

---

# Core Domain

## {{KAName}}

{{KA prose definition — unchanged from key-abstractions stage}}

#### Decisions made

- {{decision from KA stage — unchanged}}
- {{new DS decision added here if needed}}

### {{term_name}}

#### Domain Language

- {{behavioral line — unchanged from UDL stage}}
- {{behavioral line — unchanged from UDL stage}}

#### Domain Sketch

{{Optional one-sentence role statement: what this term is for and who it works with.}}

- {{verb-led behavior bullet: what it does, enforces, or produces}}
- {{verb-led behavior bullet}}
- {{verb-led behavior bullet}}
- **Invariant:** {{rule that must always hold, if any}}

#### Decisions made

- {{boundary call, scope call, structural call, or open question with reasoning}}

#### References

**Ref — {{title}}**
Source: {{source chunk path — unchanged}}
Locator: {{locator — unchanged}}
Extract: whole

```source
{{verbatim text — unchanged}}
```

---

### {{SubtypeName}} *is a type of* {{BaseName}}

#### Domain Language

- {{behavioral line — unchanged}}

#### Domain Sketch

{{One sentence: what this subtype adds beyond the base.}}

- {{delta behavior — only what the subtype adds, not what it shares with the base}}
- {{delta behavior}}

#### Decisions made

- {{why this is a subtype rather than a separate concept}}

#### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

## {{AnotherKAName}}

{{KA prose definition — unchanged}}

#### Decisions made

- {{…}}

### {{term_name}}

#### Domain Language

- {{behavioral line — unchanged}}

#### Domain Sketch

- {{verb-led behavior bullet}}

#### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

# Boundary Domain

## {{boundary_term}}

Owned by: {{module — unchanged}}

#### Domain Language

- {{behavioral line — unchanged}}

#### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text — unchanged}}
```

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled — Fulfillment module)

```markdown
---
state: domain-sketch
---

# Module: [Fulfillment]

Scope: Warehouse release, shipment tracking, delivery confirmation.

**Core terms**:
- shipment
- clearance
- proof of delivery
- carrier event
- line item

---

# Core Domain

## Shipment Lifecycle

Owns the end-to-end state of a shipment from warehouse to customer doorstep — whether it may leave, when it is in transit, and what confirms delivery. Groups clearance, release, and confirmation behaviors.

#### Decisions made

- Shipment Lifecycle is a single abstraction, not split into Release and Delivery — the source treats them as one flow with gates.
- Payment check is a prerequisite consumed from another module, not owned here.

### clearance

#### Domain Language

- Warehouse hold is removed only after payment clearance is on record.
- A clearance event must carry the authorizing reference.

#### Domain Sketch

The gate that must be passed before a shipment may leave; it depends on an external payment status signal.

- gates warehouse exit until payment clearance is on record
- records the authorizing reference on the clearance event
- rejects release if payment status is absent or failed

#### Decisions made

- Clearance owns the gate decision; Billing owns the payment status that satisfies it.

#### References

**Ref — Gate before ship**
Source: Fulfillment requirements
Locator: Operations manual 4.1
Extract: partial

```source
A shipment may not leave the warehouse until payment clearance has been received
and recorded against the shipment record.
```

### proof of delivery

#### Domain Language

- Confirmed when carrier posts a terminal scan or customer signs.
- Conflicting signals require escalation.

#### Domain Sketch

The signal that closes the delivery loop; it works with carrier events and customer confirmations.

- marks the shipment delivered when carrier scan or customer signature is present
- escalates when carrier and customer signals conflict

#### Decisions made

- Escalation path (carrier vs. customer disagreement) is an open question for the domain expert.

#### References

**Ref — Delivery confirmation**
Source: Fulfillment requirements
Locator: Policy ch.4 (delivery)
Extract: whole

```source
Delivery is confirmed when the carrier posts a terminal scan or the customer
provides a signature. Conflicting signals require escalation to operations.
```

### International Shipment *is a type of* clearance

#### Domain Language

- Adds customs documentation and duty handling before the same exit rules apply.

#### Domain Sketch

Extends the clearance gate with customs prerequisites that domestic shipments do not have.

- collects customs commodity codes for each line before gate evaluation
- holds duty estimate until the broker accepts

#### Decisions made

- International Shipment is a subtype — it adds customs paperwork but reuses the same exit gate from the base.

#### References

**Ref — Broker filing**
Source: Fulfillment requirements
Locator: Customs addendum B
Extract: partial

```source
International shipments require a commodity code for each line and a confirmed
duty estimate from the licensed broker before the warehouse gate may open.
```

---

# Boundary Domain

## payment status

Owned by: Billing

#### Domain Language

- Determines whether shipment clearance is granted.

#### References

**Ref — Payment gate**
Source: Fulfillment requirements
Locator: Policy ch.4 (warehouse gate)
Extract: partial

```source
Clearance is contingent on a positive payment status signal from the Billing system.
```
```
