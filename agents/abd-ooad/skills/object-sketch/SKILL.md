---
name: object-sketch
description: >-
  Sketch an initial object model into object-sketch.md: mechanics (domain-logic
  bullets), concepts, subtype "*is a type of*", extracts. May seed from
  extracted-domain-logic.md (extract-domain-logic). Shapes in template. No full
  Key Abstraction carry-forward, no DDD stereotypes or APIs.
---

# object-sketch

## Purpose

The purpose of this skill is to **sketch an initial object model** from **whatever context the engagement supplies**: authoritative text, cited extracts, **`extracted-domain-logic.md`** when **`extract-domain-logic`** was run, and/or **key abstractions** in **`key-abstractions.md`**.

It **organizes** identification into concepts that are **structured** but also written in **plain English** so a **business reader** can follow. **Concepts** are structured according to **what it is for**, **what it knows and does**, and **how it relates to other concepts** (who it depends on, who it works with).

## Agent instructions

1. **Anti-drift handoff:** When **`abd-ooad/object-sketch.md` does not exist** yet, **materialize** it by copying **one** upstream file in full, then refine into the object-sketch template. **Precedence** (first that exists): **`extracted-domain-logic.md`**, then **`key-abstractions.md`**, then **`module-partitioning.md`**. Record the **Seed:** in the sketch header (per template). Upstream files stay for audit; **the sketch is canonical** for object modeling after this skill.
2. Emit **`object-sketch.md`** according to **`templates/object-sketch-template.md`** for placeholder shapes and separator styling. Deliverable: `<active_skill_workspace>/abd-ooad/object-sketch.md`.
3. **Concept input (order of precedence) when not seeding from a full-file copy:** When **`key-abstractions.md`** exists, treat it as the **primary source** for what to model: mirror **`## Module: [Name]`** from it and use each **`### Key Abstraction:`** as the main seed for **`### Concept`** blocks (refine/split/merge against the real source; see **Key abstractions**). When **`extracted-domain-logic.md`** exists and **`key-abstractions.md`** does not, derive **modules and `## Domain-logic`** from the extract file and infer concepts from those lines plus **`### Extract`**. When both are **absent**, derive modules and concepts from the scope the user gives (chapter list, bounded slice, or sections of **source context**). Include **`[Unallocated]`** / **`[Rejected]`** only when the engagement uses them.
4. **Module completeness:** Each in-scope module follows the **template** (opening **`### Extract`**, **`## Domain-logic`**, then one or more concepts). A module may be intentionally empty only with **`Reason:`** under **`### Extract`** and enough pointers to show why.
5. **Subtype discipline:** shared behavior on the **base** concept; subtype block only adds **delta** behaviors and collaborations.
6. **Traceability:** at module end, `Key Abstraction: X -> ### Concept: A, B` if reviewers need a map.

## Core concepts

### Key abstractions

A **key abstraction** is a **named domain idea** the team already treats as important enough to model (a thing, rule bundle, or mechanism) - the **seed** for a **`### Concept`**. You **turn each abstraction into one or more concepts** by determining name, intent, behaviors, and collaborations against the real source (**merge**, **split**, or **rename** as needed); evidence is always under **`### Extract`** (module inventory) and **`#### Extract - ...`** on every concept or subtype.

If **`key-abstractions.md`** exists use it as the **default source** of those seeds: read each **`### Key Abstraction:`** and produce the **`### Concept`** blocks here; do **not** mirror the whole file as a second carry-forward. If it is **missing**, **infer your own key abstractions** from the authoritative source, then build concepts and citations per **Sequence**.

If the live source and **`key-abstractions.md`** disagree, **write down the tension** then **prefer the source material** and correct stale abstraction text and make note of stale abstraction text.

### Source Extraction Slicing

Every identification passage or **Source slice** that belongs in scope must be **mentioned** in **`object-sketch.md`** at exactly **one** of these levels:

1. **`#### Extract - ...`** under a **concept** or **subtype** block (verbatim or explicit pointer to a module **`### Extract`** bullet), or
2. A bullet under **`### Extract`** at the start of that module (pointers, **`Source:`** / **`Locator:`**, optional short quote), or
3. **`## Module: [Unallocated]`** with its **`### Extract`**, or
4. **`## Module: [Rejected]`** with its **`### Extract`**.

Nothing in scope may be left uncited. There is no parallel **Module sources** section: inventory and concept evidence both use **Extract** headings.

### Domain Logic

During object sketching, domain logic is extracted from the source context. Domain logic describes the business behvior, business state, business rules, interactions, and constraints for a particular **module**. Domain logic is written in **short lines of prose**. These statements can be read by a non technical person, and can be validated against the real sorce material. You take it from whatever you are treating as **authoritative** for this engagement, paraphrased or quoted tightly enough that it can be defended if someone asks “where did that come from?” It gives everyone the **truth grounded in the source, but structured and organized** so a team can understand how the domain actually behaves before mmaking decions about classes , methods, or properties

**Examples** (generic business wording; not RPG or combat rules; here emphasizing **interactions** and **behavior**, not only hard constraints):

- When on-hand quantity for a sku falls below the reorder point, replenishment creates a transfer and the warehouse moves stock from bulk storage to the pick face so picking can continue in the next wave.
- The carrier posts a delivery scan; fulfillment matches that event to an open shipment, updates the customer-facing status, and records the delivery milestone as complete for that shipment.
- The broker submits the customs filing; customs returns a duty assessment; the importer accepts it and the port system marks the shipment cleared to leave, which triggers the downstream haulage booking.

For a **separate module-level pass** before sketching concepts, use **`extract-domain-logic`** and **`extracted-domain-logic.md`**; the sketch then **seeds** from that file when present (**Agent instructions**). The domain logic statements (here or there) are the primary input toward sketching **Concepts**.

### Concepts

During object sketching, **concepts** are the named ideas you treat as **candidate objects** in the business: what each one is **for**, what it **does**, who it **works with** or **leans on**, the **vocabulary** that belongs with it, and **evidence** from the real material so a non-technical reader can follow and anyone can challenge you to show **where it came from**. When **`key-abstractions.md`** already exists for the engagement, use it as the usual **starting point** for those names and intents; when it does not, pull the same grain of ideas from **user scope** and **source context** and still keep that traceability. **Specializations** are written in plain English as one kind of thing **being a type of** another: keep the **shared** behavior and relationships on the **broader** idea, and let the more specific one say only what is **extra**, so you are not telling the same story twice.

**Out of scope for this skill:** `<<Entity>>` / VO / Service labels, operation signatures, cardinality, full lifecycle tables, long bounded-context essays.

## Sequence (normative)

Use this **order** in **`object-sketch.md`**. **`templates/object-sketch-template.md`** shows **how blocks look** (placeholders, `----` / `-----`, heading spellings); it does **not** redefine sequence.

**File top**

1. `# Object sketch - ...` then **Scope** and **Sources** lines (shape per template).

**Inside each `## Module: [Name]`** (including **`[Unallocated]`** and **`[Rejected]`** when those modules exist)

2. **`### Extract`** - Inventory of **every** source passage or pointer that feeds this module (bullets; each bullet at least **`Source:`** and **`Locator:`** when available). Use this for module-wide pointers and optional short quotes; passage-specific verbatim still ends up under the right **`#### Extract - ...`** on a concept (or a pointer from that **`#### Extract`** back to a bullet here). If the module is intentionally empty, one line **`Reason:`** instead.
3. **`## Domain-logic`** - Optional one-line intro, then markdown bullets; each bullet is one testable rule.
4. **Concept units** - Repeat in this order for every **`### Concept`** and every **`### Subtype *is a type of* Base`**:
   - **Heading** - `###` + name (Title Case if multi-word), or subtype heading in plain English.
   - **Intent** - One paragraph (no subheading): purpose, partner concepts, how they cooperate (about two or three sentences).
   - **`----`** - **Behaviors:** short lines, usually verb-led (what this concept does).
   - **`-----`** - **Collaborations:** short lines (depends on / uses / relates to other concepts); prefer prose over machine `uses:` unless the engagement wants it.
   - **`----`** - **`Shape hint:`** line (and optional **`Tension:`** line).
   - **`#### Core terms`** - Bullet list of vocabulary.
   - **`#### Extract - ...`** (required on every concept and subtype) - `Source:`, `Locator:`, `Extract:` (**whole** or **partial**), blank line, then verbatim body (no fenced block) **or** one line pointing at the module **`### Extract`** bullet that carries the quote (still satisfies **Source accounting**).

**Module file order (convention)**

- Put substantive **`## Module: [Name]`** blocks first, then **`## Module: [Unallocated]`**, then **`## Module: [Rejected]`** when the engagement uses them. **Each** of those module blocks repeats steps **2-4** above. Parked or rejected passages must appear in that module's **`### Extract`** and/or a **`#### Extract - ...`** under a concept when appropriate.

## What each section means

- **Extract (module)** - First subsection inside a module: **`### Extract`** inventory bullets for **Source accounting** (see **Core concepts**).
- **Concept heading** - Names the concept; subtype form states generalization in English (`*is a type of*`), not `Child : Parent`.
- **Intent** - Why the concept exists and how it cooperates with others.
- **Behaviors** - Domain actions or rules this concept is responsible for carrying out.
- **Collaborations** - Other concepts it leans on or connects to.
- **Shape hint** - Modeling or structural note. **Tension** - Optional tradeoff or open issue.
- **Core terms** - Words to track from the source.
- **Extract (concept)** - Every **`### Concept`** / subtype ends with **`#### Extract - ...`**: verbatim identification **or** a pointer to the module **`### Extract`** bullet that holds it (still **mentioned** once).

## When to use

- To get an OO-shaped sketch before CRC, with **readable English** inside each concept.



## Example (generic - not a specific game or product)

```markdown
## Module: [Fulfillment]

### Extract

- Source: Fulfillment requirements (source context) | Locator: Policy ch.4 (warehouse gate)
- Source: Fulfillment requirements (source context) | Locator: Operations manual 4.1 (release rule)
- Source: Carrier integration spec | Locator: Tracking API (delivery confirmation)

## Domain-logic

Rules that govern how a shipment may move and be closed.

- A shipment may leave the warehouse only after payment has cleared.
- Delivery is confirmed when the carrier posts a terminal scan or the customer signs.

### Shipment lifecycle

Coordinates whether a shipment is allowed to leave the warehouse and when it is considered delivered. Works with **Payment clearance** to gate exit, and with **Carrier events** to interpret scans and signatures.

----
gates warehouse exit until payment clearance is on record
marks the shipment delivered when carrier or customer confirmation is present
-----
depends on Payment clearance for the all-clear to ship
uses Carrier events to interpret tracking and proof of delivery
----
Shape hint: orchestration object; does not store every carrier field.
Tension: Customer sign-off and carrier scan can disagree; policy must pick one.

#### Core terms
- clearance
- proof of delivery

#### Extract - Gate before ship (partial)
Source: Fulfillment requirements (source context)
Locator: Operations manual 4.1
Extract: partial
No physical release may occur before finance marks the order paid.

### International shipment *is a type of* Shipment

Adds customs documentation and duty handling before the same exit and delivery rules apply. Carrier confirmation wording is not re-quoted here; it is listed under the module **### Extract** (third bullet).

----
collects customs commodity codes for each line
holds duty estimate until the broker accepts
-----
uses Customs broker to file declarations
depends on Shipment lifecycle for the same exit and delivery gates
----
Shape hint: subtype adds paperwork; base lifecycle still owns state transitions.

#### Core terms
- customs declaration
- duty estimate

#### Extract - Broker filing (partial)
Source: Fulfillment requirements (source context)
Locator: Customs addendum B
Extract: partial
The broker must accept the filing before duty is considered final.
```

## Validate

- No full **`### Key abstractions (carry-forward)`** mirroring **`key-abstractions.md`** unless the team explicitly opts in.
- **Source accounting:** Every in-scope identification or **slice of source context** is **mentioned** at **concept** (`#### Extract - ...` or pointer to module **`### Extract`** bullet), **module** (`### Extract` inventory), **[Unallocated]**, or **[Rejected]** - never dropped.
- Each **`## Module: [...]`** opens with **`### Extract`** (or **`Reason:`** for an empty module).
- Each **`### Concept`** (and each subtype block) follows **Sequence**: **Intent**, then **`----`** behaviors, **`-----`** collaborations, **`----`** Shape hint / optional Tension, **`#### Core terms`**, then **`#### Extract - ...`** (verbatim or pointer to module **`### Extract`**).
- **`### Subtype *is a type of* Base`** uses **English generalization**, not `Child : Base`, for this skill.
- Domain-logic bullets are **rules-bearing** only.

## Hand-off

Upstream: **`module-partitioning.md`**, **`key-abstractions.md`**, optional **`extracted-domain-logic.md`** from **`extract-domain-logic`**. **`object-sketch.md`** combines **`### Extract`**, **`## Domain-logic`**, and **concept blocks** with **`#### Extract - ...`**, so **all source is accounted for**. After the sketch exists, it is the **canonical** object-oriented sketch for CRC; older artifacts are for audit.

**Promoted engagement path (abd-ooad):** **module-partitioning** and/or **key-abstraction-identification**, optional **extract-domain-logic**, **object-sketch**, **class-responsibility-collaborator**, **elaborate-business-logic** (post-CRC **`business-logic.md`**), **scenario-walkthrough**, **properties-methods-and-relationships**.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. -->
<!-- execute_rules:bundle_rules:end -->
