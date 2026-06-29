# Grill me — drawio-domain-sync

Only when the invocation includes **"grill me"**. Tooling skill — grill focuses on diagram fidelity choices, not domain discovery.

- Which source fidelity did you choose and why — domain specification, domain model, or domain language?
- Which KAs have boundary classes that should appear dashed — and which cross-KA subtypes did you correctly exclude?
- What manual layout edits would a full re-render destroy — and did you use incremental update instead?
- What did `audit_diagram_report()` report — and which overlaps or edge crossings remain?
- If syncing back from Draw.io, what diff will the user see — and which changes are safe to apply to the markdown source?
