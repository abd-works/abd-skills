<!--
  Bounded Context Map — output template.

  Copy to: <workspace>/bounded-context-map.md

  Contract:
    - One file per project/system.
    - Inventory section lists every bounded context with owning team and scope.
    - Dependencies section declares every cross-boundary arc with all three
      dimensions: domain mapping, integration mechanism, team engagement model.
    - Decisions / Tensions section captures open questions and deferred items.
    - Every bounded context must appear in at least one dependency or be
      declared standalone.
-->

# Bounded Context Map — {{project_name}}

Scope: {{system | subsystem | enterprise}}
Date: {{date}}

---

## Bounded Contexts

### {{ContextName}}

- **Owning team:** {{team_name}}
- **Scope:** {{one-sentence description of what this context owns}}
- **Implementation:** {{monolith module | microservice | shared library | legacy system | external vendor}}

### {{AnotherContext}}

- **Owning team:** {{team_name}}
- **Scope:** {{one-sentence description}}
- **Implementation:** {{implementation type}}

---

## Dependencies

### {{SourceContext}} → {{TargetContext}}

- **Direction:** {{upstream/downstream | mutual}}
- **Domain mapping:** {{which domain concepts cross the boundary; what translation is required}}
- **Integration mechanism:** {{Events | Messaging | REST/API | Batch | Shared DB | File Transfer | Shared Kernel codebase}}
- **Team engagement model:** {{named pattern — Shared Kernel | Customer/Supplier | Conformist | Anticorruption Layer | Open Host/Published Language | Separate Ways}} + {{team collaboration — Travelling Team Members | Service Provider | Enabler}}
- **Rationale:** {{why this pattern was chosen; trade-offs accepted}}

### {{AnotherSource}} → {{AnotherTarget}}

- **Direction:** {{direction}}
- **Domain mapping:** {{concepts}}
- **Integration mechanism:** {{mechanism}}
- **Team engagement model:** {{pattern + collaboration}}
- **Rationale:** {{rationale}}

---

## Standalone Contexts

{{List any bounded context that does not participate in a dependency arc, with a rationale for why it stands alone. If none, state "No standalone contexts."}}

---

## Decisions and Tensions

- {{Open question, contested boundary, or deferred integration with owner and target resolution date}}
- {{Another decision or tension}}

---

---

## Example — Digital Cargo File (delete after use)

This filled example is based on the Digital Cargo File project case study. It demonstrates the template shape with six bounded contexts, five dependency arcs, four different relationship patterns, and a before/after transformation analysis.

# Bounded Context Map — Digital Cargo File

Scope: system
Date: 2026-05-18

---

## Bounded Contexts

### Supply Operation

- **Owning team:** Operations Team
- **Scope:** Delivery of cargo — scheduling, tracking, and operational logistics for physical cargo movement.
- **Implementation:** legacy system

### Trading

- **Owning team:** Trading Desk
- **Scope:** Sales of cargos — deal management, pricing, counterparty communication.
- **Implementation:** legacy system

### Invoice

- **Owning team:** Finance Team
- **Scope:** Financial settlement — invoice generation, payment tracking, reconciliation.
- **Implementation:** legacy system

### Communication Gateway

- **Owning team:** IT Operations
- **Scope:** Transmission and filing of business messages (email, fax, telex) and document control — tracking when messages were sent.
- **Implementation:** legacy system (shared infrastructure)

### DCF — Folder and Document Control

- **Owning team:** DCF Project Team
- **Scope:** Logical and physical document storage, filing, retrieval, and document control (previously split between Communication Gateway and the old Folder context; merged after context map analysis).
- **Implementation:** microservice (new build)

### DCF — Front Page (Case Management)

- **Owning team:** DCF Project Team (shared with Operations liaison)
- **Scope:** Case follow-up, workflow, and aggregated cargo/deal information — extracted from the archive after analysis revealed it polluted the filing concern.
- **Implementation:** microservice (new build, separated from archive)

---

## Dependencies

### Supply Operation → DCF — Front Page

- **Direction:** Supply Operation is upstream; Front Page is downstream
- **Domain mapping:** Cargo status, delivery milestones, and allocation data flow from Supply Operation into the Front Page for case follow-up. Front Page aggregates this with Trading data to show a unified case view.
- **Integration mechanism:** REST/API (via Filing and Communications Service)
- **Team engagement model:** Anticorruption Layer — Front Page isolates itself from Supply Operation's legacy model to avoid coupling case management to operational data structures. Service Provider — Operations team pushes data per DCF team's interface spec.
- **Rationale:** The legacy Supply Operation model is stable but complex; an ACL lets the Front Page evolve its case management model independently. The API contract is owned by the DCF team.

### Trading → DCF — Front Page

- **Direction:** Trading is upstream; Front Page is downstream
- **Domain mapping:** Deal information, counterparty details, and pricing data flow into the Front Page for case aggregation. The Front Page does not write back to Trading.
- **Integration mechanism:** REST/API (via Filing and Communications Service)
- **Team engagement model:** Anticorruption Layer — same rationale as Supply Operation. Service Provider — Trading team publishes data per the DCF interface contract.
- **Rationale:** Isolating Front Page from Trading prevents deal model changes from breaking case management workflows.

### Communication Gateway → DCF — Folder and Document Control

- **Direction:** Communication Gateway is upstream; Folder and Document Control is downstream
- **Domain mapping:** Inbound and outbound messages are the shared domain objects. Document control (filing of inbound messages) was moved from the Communication Gateway into Folder and Document Control, reducing the Gateway to a pure transmission concern.
- **Integration mechanism:** Messaging (message queue for inbound/outbound)
- **Team engagement model:** Open Host Service / Published Language — the Filing and Communications Service is published as an open protocol accessible to all front-end systems. Enabler — the Gateway team provides the messaging transport; the DCF team consumes it self-service.
- **Rationale:** Moving document control out of the Communication Gateway eliminated the "spider in the web" problem. Users no longer interact with the Gateway for filing, reducing average filing time by ~30 seconds per message across 1000 daily messages.

### DCF — Front Page → DCF — Folder and Document Control

- **Direction:** Front Page is downstream; Folder and Document Control is upstream (Front Page reads from the archive)
- **Domain mapping:** Front Page retrieves filed documents and filing status from Folder and Document Control. It does not manage filing — only reads.
- **Integration mechanism:** REST/API (Filing and Communications Service)
- **Team engagement model:** Customer/Supplier — Front Page team requests retrieval capabilities; Folder team negotiates and delivers. Travelling Team Members — both contexts are owned by the DCF Project Team, so cross-context work happens within one team.
- **Rationale:** Loose coupling via the service interface enables both contexts to evolve independently while the single-team ownership keeps communication cost low.

### Invoice → Trading

- **Direction:** Invoice is downstream; Trading is upstream
- **Domain mapping:** Deal identifiers, pricing terms, and counterparty references flow from Trading into Invoice for settlement.
- **Integration mechanism:** Batch (nightly extract from Trading into Invoice ledger)
- **Team engagement model:** Conformist — Invoice team adopts Trading's deal model directly because the Finance team has no need to reinterpret deal structure. Service Provider — Trading team provides the nightly extract per Invoice team's schedule.
- **Rationale:** The Invoice context needs deal data as-is; building a translation layer would add cost without business value. The nightly batch is acceptable because invoices are not real-time.

---

## Standalone Contexts

No standalone contexts. All six bounded contexts participate in at least one dependency arc.

---

## Decisions and Tensions

- **Shipment & Allocation context** — identified in the original map as a future context for oil field operation and owner allocation. Not yet scoped for integration. Owner: Operations Team. Target: Q3 planning.
- **Front Page variants** — each business unit historically had its own front page variant. Standardized to a limited set, but tension remains around advanced case management and workflow capabilities the paper-based front page concept cannot fully replicate. Owner: DCF Product Owner.
- **Communication Gateway retirement** — with document control moved to Folder and front-end systems no longer routing through the Gateway, the Gateway's role is reduced to pure message transmission. Consider whether Separate Ways is appropriate long-term. Owner: IT Operations.
