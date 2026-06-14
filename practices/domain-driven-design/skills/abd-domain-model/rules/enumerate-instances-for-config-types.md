# Rule: Enumerate instances for configuration-driven types

**Scanner:** Manual review

A passing model enumerates concrete instances when a typed concept drives behavior through its values rather than through subclassing. When the system's capabilities are determined by which instances exist — not by class hierarchy — the model must show those instances so readers understand what the type actually permits. A failing model defines only the class shape and leaves the reader guessing which values are valid and what each one enables.

## When this applies

A concept is configuration-driven when:
- The set of valid values determines what users can do (permissions, entitlements, service access).
- Behavior varies by instance value, not by overridden methods.
- The design chose typed instances over inheritance (e.g. `Activity` with named values rather than `InitiateActivity`, `ApproveActivity` subclasses).
- The instances form a closed or slowly-changing set that the business manages.

## DO

Define the class, then enumerate its instances with what each one means:

```markdown
### **Activity**

------
name: ActivityName
----
	Invariant: each activity is scoped to exactly one service

#### Activity instances

- **initiate** — create and submit a payment or transfer within a service
- **approve** — confirm or reject a pending item within a service
- **add** — create a new record (e.g. recipient)
- **edit** — modify an existing record
- **remove** — permanently delete a record
- **configure-mailbox** — configure file transfer mailbox (administrator only)
- **assign-entitlement** — assign an entitlement to a user profile (administrator only)
```

The instances reveal the actual behavioral surface: readers know exactly which activities exist, what each grants, and which are restricted.

## DO NOT

Define the class without instances:

```markdown
### **Activity**

------
name: ActivityName
----
	Invariant: each activity is scoped to exactly one service
```

The reader sees a typed concept with a name property but has no idea what the valid values are, how many exist, or what capabilities they unlock. In a configuration-driven system this is equivalent to an undocumented enum — the model hides the very information that determines behavior.

## Guidance

- **Entitlement matrices** — When a concept pairs two configuration types (e.g. Service + Activity → Entitlement), enumerate the valid combinations as an instance table showing what each pair grants.
- **User profiles or roles** — When profiles are assembled from entitlement instances, show the named profiles with their constituent instances.
- **Scope to increment** — Instance lists can be scoped (e.g. "Increment 1 instances") when the full set is large or evolving; make the scope explicit.
- **Prefer instances over prose** — A table or bullet list of instances communicates faster and more precisely than a paragraph describing "various activities exist."

## Diagram representation

When a class diagram accompanies the domain model, instance enumerations appear as **coloured note cells** positioned near the class they describe. Each note contains a styled table or bullet list of instances, connected to the parent class by a dashed edge. Use distinct fill colours to differentiate instance types at a glance (e.g. yellow for entitlement matrices, blue for service instances, green for activity instances, purple for profile instances).

**Example:** The `domain-model-class-diagram-entitlements.drawio` diagram shows:
- A yellow "Entitlement Instances (Service + Activity)" note with every valid combination in a three-column table.
- A blue "Service Instances" note listing each service with a one-line description.
- A green "Activity Instances" note listing each activity with its meaning.
- A purple "UserProfile Instances — Increment 1" note showing named profiles, their entitlements, and hardcoded test users.

Each note is visually associated (dashed edge) with the class whose instances it enumerates.

**Source:** Engagement convention (domain-model skill) — configuration-driven entitlement modeling pattern.
