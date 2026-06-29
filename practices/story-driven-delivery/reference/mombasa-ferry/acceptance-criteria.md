# Mombasa Ferry Service — Acceptance Criteria

Reference acceptance criteria for the `abd-story-acceptance-criteria` skill. Covers three stories from Increment 1 and Increment 3. Used as a quality bar and grill-me scenario. See [`README.md`](./README.md) for domain context.

---

## Story: Pay Cash Fare

**Story type:** user

### Domain terms

- *Fare* — the fixed fee for a single passenger *Crossing*
- *Cash Fare* — a *Fare* paid in physical currency at the quay; non-refundable once the *Crossing* begins
- *Boarding Queue* — the ordered line of passengers waiting for the next *Vessel* departure
- *Payment Terminal* — the staffed or self-service point where cash *Fare* is collected

### Acceptance criteria

1. **WHEN** a passenger presents the correct *Cash Fare* amount at the *Payment Terminal*  
   **THEN** the system records the payment  
   **AND** the passenger is admitted to the *Boarding Queue*  
   **Evidence:** KFS Operations Manual §3.1 — "Admit passenger to queue on cash receipt"

2. **WHEN** a passenger presents insufficient cash at the *Payment Terminal*  
   **THEN** the system does not admit the passenger to the *Boarding Queue*  
   **AND** the *Payment Terminal* displays the shortfall amount  
   **BUT** the partial amount presented is returned to the passenger  
   **Evidence:** KFS Operations Manual §3.2 — "No partial admission; return funds"

3. **WHEN** a passenger presents exact or excess cash  
   **THEN** the system admits the passenger and returns any change  
   **BUT** does not hold the excess as credit toward a future *Crossing*  
   **Evidence:** KFS Operations Manual §3.3 — "Cash is not stored as balance"

---

## Story: Present Journey Card

**Story type:** user

### Domain terms

- *Journey Card* — a rechargeable travel card; balance is decremented at boarding
- *Balance* — the remaining fare credit on a *Journey Card*
- *Fare* — the per-*Crossing* charge deducted from *Balance* at boarding
- *Insufficient Balance* — a *Balance* below the *Fare* amount for one *Crossing*

### Acceptance criteria

1. **WHEN** a passenger presents a *Journey Card* with sufficient *Balance*  
   **THEN** the system deducts one *Fare* from the *Balance*  
   **AND** the passenger is admitted to the *Boarding Queue*  
   **AND** the *Payment Terminal* displays the remaining *Balance*  
   **Evidence:** KFS Card Spec §2.1 — "Deduct fare at boarding gate on sufficient balance"

2. **WHEN** a passenger presents a *Journey Card* with *Insufficient Balance*  
   **THEN** the system rejects the fare deduction  
   **AND** the *Payment Terminal* displays the current *Balance* and the *Fare* shortfall  
   **BUT** the passenger is not admitted to the *Boarding Queue*  
   **BUT** no amount is deducted from the *Balance*  
   **Evidence:** KFS Card Spec §2.2 — "Reject and display shortfall; no partial deduction"

3. **WHEN** a passenger presents an expired or blocked *Journey Card*  
   **THEN** the system rejects the card  
   **AND** displays the reason (expired / blocked)  
   **BUT** does not deduct any *Balance*  
   **Evidence:** KFS Card Spec §2.4 — "Blocked card must not deduct; show reason"

---

## Story: Close Boarding At Capacity

**Story type:** user (Ferry Operator)

### Domain terms

- *Capacity* — the maximum number of foot passengers a *Vessel* can carry on one *Crossing*
- *Boarding Count* — the current number of passengers who have boarded since *Open Boarding*
- *Boarding Queue* — the queue of passengers still waiting; remains in place after boarding closes
- *Full* — the state of a *Vessel* when *Boarding Count* equals *Capacity*

### Acceptance criteria

1. **WHEN** the *Boarding Count* reaches *Capacity*  
   **THEN** the system marks the *Vessel* as *Full*  
   **AND** boarding closes automatically  
   **AND** passengers remaining in the *Boarding Queue* are held for the next *Crossing*  
   **Evidence:** KFS Operations Manual §4.3 — "Auto-close on capacity; queue persists"

2. **WHEN** the operator manually closes boarding before *Capacity* is reached  
   **THEN** the system marks the *Vessel* boarding as closed  
   **AND** the current *Boarding Count* is recorded  
   **BUT** the *Vessel* is not marked as *Full* (capacity is not assumed to be reached)  
   **Evidence:** KFS Operations Manual §4.4 — "Manual close is distinct from full; operator may close early for safety"

3. **WHEN** boarding is closed (automatically or manually)  
   **THEN** no further passengers may board this *Crossing*  
   **BUT** the *Boarding Queue* for the next *Crossing* remains open  
   **Evidence:** KFS Operations Manual §4.3–§4.4 — "Queue for next crossing always open"

---

## What to notice

- Every AC uses **WHEN/THEN** (and **AND/BUT** where needed) — no `Given`, no capability statements
- Each **Domain terms** section traces to a domain source; do not invent terms
- **BUT** distinguishes what explicitly must NOT happen (negative carve-outs)
- Negative paths are **first-class** criteria — not afterthoughts
- Evidence cites the actual source document, section, and the relevant phrase
- AC 1 and AC 2 in "Close Boarding At Capacity" distinguish two related paths rather than merging them
