# Input traps — abd-architecture-outline

Assumptions, ambiguities, and missing context that commonly produce a weak outline. Check each trap against available input before generating — flag gaps honestly; do not invent systems or mechanisms to fill them.

- **System identity** — when someone says "the system," do all stakeholders picture the same boundary? What gets left out when you draw the box, and what gets accidentally included?
- **Hidden neighbors** — are there systems, services, or manual processes that interact with this system that nobody has mentioned yet? The ones that surface during integration are the ones nobody named during shaping.
- **Mechanism relevance** — which cross-cutting concerns actually matter here, and which are you including because they're "standard"? A mechanism that doesn't serve a real NFR adds complexity without value.
- **Connection assumptions** — for each arrow between systems, do you know the protocol, who initiates, and what happens when the other side is unavailable? Or are those details being deferred without anyone tracking the deferral?
- **Principles vs. preferences** — can each guiding principle be applied to a real code decision with a clear yes-or-no answer, or is it a sentiment that sounds wise but doesn't constrain anything?
- **What's deliberately excluded** — what have you decided is out of scope for this outline, and does the team agree it's out of scope — or are they assuming someone else is covering it?
