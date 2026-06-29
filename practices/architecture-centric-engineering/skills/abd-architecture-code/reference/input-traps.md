# Input traps — abd-architecture-code

Assumptions, ambiguities, and missing context that commonly produce wrong code. Check each trap against available input before generating — flag gaps honestly; do not guess spec layout.

- **Layer boundaries** — where does one layer's responsibility end and the next begin? If you can't name what each layer is allowed to know about the layers around it, the code will blur those boundaries under pressure.
- **Spec vs. reality** — which parts of the architecture spec have never been exercised by a real story? Those are the patterns most likely to need rework once production code hits them.
- **Domain behavior vs. framework plumbing** — for each scenario you're about to implement, is the interesting behavior in the domain logic or in the framework wiring? If the test is mostly asserting plumbing, what domain risk is it leaving uncovered?
- **Boundary assumptions** — when this code calls another system or layer, what responses are you assuming you'll get? Which of those assumptions have you verified, and which are you hoping are right?
- **Test tier coverage gaps** — which behaviors are only proven at one tier? If the domain test passes but the integration test doesn't exist yet, what could still be wrong that you wouldn't catch?
- **Scenario completeness** — are there flows through this story that nobody has written a scenario for — error paths, concurrent access, partial failures — that the architecture spec implies but the story doesn't explicitly name?
