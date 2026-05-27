# abd-answers retrieval — abd-bounded-context-map

Retrieval date: 2026-05-18
Queries: 4 Pinecone queries + 1 converted source document (stuff.docx → markdown/stuff.md)

---

## Kept chunks

### Chunk 1 — Bounded Context definition and Context Map creation steps

**Relevance:** `core_concept`, `procedure`
**Source:** stuff.md (Model Boundaries + Relationships Between Bounded Contexts sections)
**Query:** converted source document
**Rank:** primary source

```body
Multiple models coexist on big projects and each model applies in a context. The context of a particular model may be a certain part of the code, or the work of a particular team. The model context is whatever set of conditions must apply in order to be able to say that the terms in a model have a specific meaning. In order to establish model boundaries or a bounded context, the context within which the model applies must be explicitly defined.

Once bounded contexts have been defined, a Context Map is created that gives a global overview of the relevant model/system contexts and the relationships between them.

To create a context map follow these steps:
1. Identify each model in play on the project and define its bounded context
2. Name each bounded context and include the names in the ubiquitous language of the business domain model
3. Describe the points of contact between the models, outlining explicit translation for any communication
```

### Chunk 2 — Seven relationship patterns (Evans-grounded definitions)

**Relevance:** `core_concept`
**Source:** stuff.md (Relationships Between Bounded Contexts section)
**Query:** converted source document
**Rank:** primary source

```body
Shared kernel: When functional integration is limited, the overhead of continuous integration may be too high. Separate bounded contexts may be defined and multiple teams formed. In this case, designate some subset of the domain model that the two teams agree to share. This includes, along with this subset of the model, the subset of code or of the database design associated with that part of the model. The shared subset should not be changed without consultation with the other team.

Customer/supplier development teams: Often one subsystem essentially feeds another and all the dependencies go one way. In this case, establish a clear customer/supplier relationship between the two teams. Make the dependant team play the customer role to the team it relies on. Negotiate and budget tasks for dependant team requirements so that everyone understands the commitment and schedule.

Conformist: The customer/supplier development teams pattern will not work in certain situations such as when the two teams are in different companies or very far apart in the management hierarchy. In the case where the model style for both teams is of good quality and reasonably comparable it may be best to give up on an independent model altogether.

Anticorruption layer: When a new system is being built that must have a large interface with another, the difficulty of relating the two models can eventually overwhelm the intent of the new model altogether, causing it to be modified to resemble the other system's model, in an ad hoc fashion. In this case, create an isolation layer to provide clients with functionality in terms of their own domain model.

Separate ways: Integration is always expensive and sometimes the benefits are small. In many circumstances, integration provides no significant benefit and may not be necessary. In this case, declare a bounded context to have no connection to the others at all.

Open host services: When a subsystem has to be integrated with many others, customizing a translator for each can bog down the team. In this case, define a protocol that gives access to the subsystem as a set of services. Open the protocol so that all who need to integrate with the subsystem can use it.

Published language: Direct translation to and from the existing domain models may not be a good solution. Those models may be overly complex or poorly factored. In this case, use a well documented shared language that can express the necessary domain information as a common medium of communication, translating as necessary into and out of that language.
```

### Chunk 3 — Choosing and transforming boundaries

**Relevance:** `rule`, `procedure`
**Source:** stuff.md (Choosing boundaries section)
**Query:** converted source document
**Rank:** primary source

```body
In order to choose the right relationship, it is important to draw the context map to reflect the current situation at any given time. Once the context map is created it is possible to further define context boundaries and relationships. Some things to consider when choosing boundaries and relationships are:

Larger versus smaller: There are benefits to employing a few larger bounded contexts or more smaller bounded contexts. Larger bounded contexts can help the flow between user tasks become smoother, make the model more coherent, and foster more communication. Smaller bounded contexts can reduce communication overhead, keep the model less abstract, and can be catered to special needs.

Relationships with external systems: When dealing with external systems, three of the above mentioned patterns apply: Separate ways, Conformist and Anticorruption Layer. If integration is not required then choosing to go Separate ways is the best option.

Relationships within one system: As a team grows larger, continuous integration can become more difficult. Make sure to recognize new developments within the system under design and implement patterns accordingly. A good rule of thumb is to limit a bounded context around teams of no greater then 10 people.

Transforming relationships: There will be cases where the initial decisions about the boundaries and relationships between bounded contexts will change. Merging or changing the relationships between bounded contexts can be difficult. When conducting such changes, ensure that the current situation is fully understood, the end result is clearly defined and there are processes in place to execute the transformation.
```

### Chunk 4 — Duplicate concepts and false cognates

**Relevance:** `core_concept`
**Source:** stuff.md (Model Boundaries section)
**Query:** converted source document
**Rank:** primary source

```body
In defining model contexts, elements of distinct models are sometimes combined. Combining elements of distinct models causes two categories of problems:

Duplicate Concepts mean that there are two model elements (and attendant implementations) that actually represent the same concept. Every time this information changes, it has to be updated in two places with conversions.

False Cognates may be slightly less common, but more harmful. This is the case when two people who are using the same term (or implemented object) think they are talking about the same thing, but really are not. False cognates lead to development teams that step on each other's code, databases that have weird contradictions, and confusion in the communication within the team.
```

### Chunk 5 — Digital Cargo File case study

**Relevance:** `example`
**Source:** stuff.md (Digital Cargo File section)
**Query:** converted source document
**Rank:** primary source

```body
The context map below depicts the situation in the Digital Cargo File project. On the left side we find three existing contexts: Supply Operation, Invoice, and Trading. These three contexts exist inside different legacy systems that must be integrated with Digital Cargo File.

In the middle we find the Communication Gateway. On the right side we find the Digital Cargo File (DCF) with its three distinct model contexts: Front Page, Folder, and Document Storage.

Context Map Analysis: most of the encountered problems were caused by two factors: The role of the communication gateway (spider in the web) and the role of the front page (pollution of archive with unrelated functionality).

Recommended changes:
- Front page concept moved out of the archive and extended with anticorruption layer to isolate from Trading and Supply Operation
- Document control moved from Communication Gateway to Folder context
- Front end systems interact with Folder through an open host service

The "open host service" pattern is also in line with the principles of service oriented architecture (SOA).
```

### Chunk 6 — Booking Context example

**Relevance:** `example`
**Source:** stuff.md (Booking Context section)
**Query:** converted source document
**Rank:** primary source

```body
A shipping company has an internal project to develop a new application for booking cargo. The booking application is in bounds. The legacy cargo-tracking system is outside the boundary. Necessary translation between the new model and the legacy is to be the responsibility of the legacy maintenance team.

Yet another team is working on a model and application for scheduling the voyages of the cargo ships. The two teams had intended to produce a single, unified system but they are not working in the same bounded context. This is a risk, because they do not think of themselves as working on separate models.

So, what has been gained by defining this bounded context? For the teams working in context: clarity. For the teams outside: freedom. But the most concrete gain is probably realizing the risk of the informal sharing between the booking model team and the voyage schedule team.
```

### Chunk 7 — ABD three-dimension dependency model

**Relevance:** `core_concept`, `rule`
**Source:** Pinecone — DDD Training slide 66 (similarity 0.828); EWMA Slides slide 6 (similarity 0.769)
**Query:** "bounded context map team dependency collaboration integration mechanism"
**Rank:** 1, 8

```body
We need to call out mapping, an integration mechanism, and a team engagement model for every dependency that exists across our bounded context map.

1. Identify key domain constructs/objects that are relevant across more than one bounded context — map out how the specific elements relate to each other
2. Identify the integration approach: Events, Batch, Messaging, REST / API
3. Identify how the teams will collaborate across the bounded context:
   - Travelling Team Members (Significant Change): Members from multiple teams work as a single team
   - Service Provider (Small Change): One team makes changes according to needs of other team
   - Enabler (No Change): One team provides tools/APIs the other team uses self-service
```

### Chunk 8 — BC Map definition (ABD practitioner)

**Relevance:** `core_concept`
**Source:** Pinecone — Bounded Context Mapping Guidelines slide 3 (similarity 0.809); engineering practices section 14 (similarity 0.795)
**Query:** "bounded context mapping guidelines steps how to create a context map"
**Rank:** 6, 1

```body
A Bounded Dependency Map illustrates the relationship across our solution and the different teams, calling out how dependencies are managed on large scale programs.

Bounded Context:
- explicitly set boundaries in which the context of a model is applicable and explicitly managed to be uniform
- Organizational: a team, department, community, etc.
- Implementation: code base, database schema, etc.

Bounded Context Map:
- marks the boundaries and relationships between different models and/or system contexts in a specific project, program, or organization
- determines appropriate integration strategies
- identifies where a context may be shared across teams
- may span an entire system, a portion of a system, or across several systems within the enterprise
```

### Chunk 9 — Model Sharing Patterns catalogue (ABD visual)

**Relevance:** `core_concept`
**Source:** Pinecone — Bounded Context Mapping Guidelines slide 6 (similarity 0.834); DDD Training slide 110 (similarity 0.830)
**Query:** "bounded context map relationship patterns shared kernel customer supplier open host published language separate ways"
**Rank:** 1, 3

```body
A range of Model Sharing Patterns can be used to establish how individual Domain Boundaries can be integrated between agile teams:

Shared Kernel: Portions of two separate systems require tight integration. Designate some subset of the domain model, code, database, etc that the two teams agree to share. No changes to model subset is made without participation of the other team.

Open host services: A subsystem has to be integrated with many others. Define a common protocol that gives access as a set of services. Open the protocol to all teams who need access can use it. Enhance and expand the protocol to handle new requirements as necessary.

[Also includes: Customer/Supplier, Conformist, Anticorruption Layer, Separate Ways, Published Language — with visual diagrams]
```

### Chunk 10 — Microservices connection

**Relevance:** `core_concept`
**Source:** Pinecone — Lean-Agile Training Core Practices slide 190 (similarity 0.833)
**Query:** "bounded context map relationship patterns"
**Rank:** 2

```body
The first step to establishing micro-services, understanding your bounded contexts.

Customer Context — Product Context — Billing Context
```

### Chunk 11 — Evans: Conformist, ACL, testing at boundaries

**Relevance:** `core_concept`
**Source:** Pinecone — Domain-Driven Design: Tackling Complexity in the Heart of Software, section 23 (similarity 0.744, 0.720, 0.720, 0.714, 0.713)
**Query:** "context map upstream downstream conformist anticorruption layer shared kernel"
**Rank:** 1-5

```body
CONFORMIST: Eliminate the complexity of translation between BOUNDED CONTEXTS by slavishly adhering to the model of the upstream team. This cramps the style of the downstream designers but enormously simplifies integration. Also, you will share a UBIQUITOUS LANGUAGE with your supplier team.

CONFORMIST resembles SHARED KERNEL in that both have an overlapping area where the model is the same, areas where your model has been extended by addition, and no area of modification or contradiction. The difference is in the decision process and the degree of control: shared kernel is by agreement, conformist is by necessity.

ANTICORRUPTION LAYER: A FACADE is an alternative interface for a subsystem that simplifies access for the client and makes the subsystem easier to use. The FACADE does not change the model of the underlying system. It should be written strictly in accordance with the other system's model.

Testing at the CONTEXT Boundaries: Contact points with other BOUNDED CONTEXTS are particularly important to test. Tests help compensate for the subtleties of translation and the lower level of communication that typically exists at boundaries. They can act as a valuable early warning system.
```

---

## Discarded chunks

- Design Your Own Agile Method slides 38 (2019 and 2020 versions) — duplicate of stuff.md BC Map definition, lower fidelity
- EWMA Slides slide 2 — title-only slide, no content
- structural_scan_report section 2496 — stub heading only
- Agile-AI Augmented Delivery slide 5 — generic practice overview, not BC-specific
- Evans bibliography section — references only
- ABD_ConnectingModelsMapsSpecs slides 33 (2019, 2019-03) — duplicate "first step to micro-services" slide
