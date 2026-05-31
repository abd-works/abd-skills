# `docs/ux/interface-design.md` stays in sync with the code

The markdown spec and the running code are two views of the same screen implementation. They must agree at every commit.

**DO** author or update `docs/ux/interface-design.md` **before** writing or changing code. The markdown carries the framework decision, host project conventions, the AC → behaviour → test mapping, the accessibility checklist, and the performance budgets. The code is written against it.

**DO** update `docs/ux/interface-design.md` at the end of every skill run with the current test statuses (pending / passing / failing), the current accessibility check results, and the current performance measurements.

**DO** append a row to the change log in `docs/ux/interface-design.md` whenever the code changes in a way that affects mapping, accessibility, or performance — recording date, direction (`md → code` or `code → md`), and a one-line summary.

**DO NOT** commit code whose behaviours, test names, accessibility results, or performance measurements disagree with `docs/ux/interface-design.md`. If they disagree, decide which one is right, fix the other, and only then commit.

**DO NOT** treat the markdown as project documentation that lags behind. It is the live spec: every code change that affects the table cells updates the cells.
