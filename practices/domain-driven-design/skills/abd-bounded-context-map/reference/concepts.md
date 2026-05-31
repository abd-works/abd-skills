# Bounded Context Map — Concepts

## Bounded context

A **bounded context** is an explicitly set boundary in which a model applies and is managed to be uniform. It has two facets:

- **Organizational** — the team, department, or community responsible for the model.
- **Implementation** — the code base, database schema, or deployable unit that embodies the model.

Within a bounded context, every term in the model has one meaning. Across boundaries, the same word may mean something different — and that difference is either managed or it becomes a defect. Two failure modes signal missing or misdrawn boundaries:

- **Duplicate concepts** — two model elements represent the same real-world thing, forcing double updates and conversion logic.
- **False cognates** — two teams use the same term but mean different things, leading to contradictory code, confused databases, and miscommunication.

## Bounded context map

A **bounded context map** is a global view of all the model contexts in a project and the relationships between them. It marks the boundaries, determines integration strategies, identifies where contexts may be shared across teams, and may span an entire system, a portion of a system, or across several systems within the enterprise.

Creating a context map follows three steps:

1. **Identify** each model in play on the project and define its bounded context.
2. **Name** each bounded context and include the names in the ubiquitous language of the business domain model.
3. **Describe** the points of contact between the models, outlining explicit translation for any communication.

## Three dimensions per dependency

Every dependency between two bounded contexts must be declared across three dimensions. Leaving any dimension implicit is a gap the team will pay for later.

1. **Domain mapping** — which domain constructs or objects are relevant across more than one bounded context; how the specific elements in each context relate to each other and what translation is required at the boundary.

2. **Integration mechanism** — how the systems actually communicate: Events, Messaging, REST/API, Batch, Shared DB, File Transfer, or a Shared Kernel codebase. The mechanism constrains consistency, latency, and coupling.

3. **Team engagement model** — how the teams that own the two contexts will collaborate when changes are needed:
   - **Travelling Team Members** — members from multiple teams work as a single team (for significant changes).
   - **Service Provider** — one team makes changes according to the needs of the other team (for small changes).
   - **Enabler** — one team provides tools or APIs the other team uses self-service (for no-change integration).

## Relationship patterns

The relationship between two bounded contexts takes one of several named patterns. Each pattern encodes a different trade-off between autonomy and coupling. Choosing the right one depends on team structure, power dynamics, and how much model divergence the business can tolerate.

- **Shared Kernel** — a subset of the domain model that two teams agree to share, including associated code and data. No changes to the shared subset without consultation. Use when tight integration is needed and the teams can sustain the communication overhead.

- **Customer/Supplier** — one subsystem feeds another; all dependencies go one way. The downstream team plays the customer role, negotiating requirements. Both teams jointly develop automated acceptance tests to validate the interface.

- **Conformist** — the downstream team gives up on an independent model and slavishly adheres to the upstream team's model. Simplifies integration enormously but cramps downstream design. Often appropriate when consuming enterprise packages (ERP, CRM) that require only moderate customization.

- **Anticorruption Layer** — an isolation layer that provides clients with functionality in terms of their own domain model, translating in both directions between the two models. Use when a new system must interface with a large or messy legacy system without letting the legacy model pollute the new design.

- **Open Host Service / Published Language** — a common protocol published as a set of services, open to all who need to integrate. Often paired: the open host defines the access; the published language defines the shared vocabulary. Aligns with service-oriented architecture principles.

- **Separate Ways** — no integration. The bounded context has no connection to the others, allowing developers to find simple, specialized solutions within a small scope.

## Choosing and transforming boundaries

Drawing a context map is not a one-time event. Boundaries shift as teams grow, systems evolve, and business needs change. Several heuristics help:

- **Larger vs smaller** — larger bounded contexts make the model more coherent and the flow between user tasks smoother, but increase communication overhead. Smaller contexts reduce communication, keep models less abstract, and can be tailored to special needs. A practical upper bound is roughly ten people per bounded context.
- **External systems** — three patterns typically apply: Separate Ways (no integration needed), Conformist (adopt their model), or Anticorruption Layer (insulate from their model).
- **Internal boundaries** — watch for informal sharing that signals two teams are not in the same context but think they are. Formalize the relationship with a Shared Kernel or Customer/Supplier pattern.
- **Transformation** — when initial boundary decisions change, ensure the current situation is fully understood, the end result is clearly defined, and processes are in place to execute the transformation without disrupting neighbouring contexts.
