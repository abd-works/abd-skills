# `docs/ux/lo-fi.md` stays in sync with the canvas

The markdown spec and the canvas are two views of the same lo-fi screen. They must agree at every commit.

**DO** author or update `docs/ux/lo-fi.md` **before** driving the canvas. The markdown carries the verbatim UL excerpt, the verbatim AC, the regions, and the affordances-with-traces. The canvas is drawn from it.

**DO** read the updated canvas after the agent finishes and reflect any change (renamed affordance, affordance moved between regions, added region, changed label) back into `docs/ux/lo-fi.md` in the same skill run — including the affordance-trace column.

**DO** append a row to the change log in `docs/ux/lo-fi.md` every time the canvas changes, recording date, direction (`md → canvas` or `canvas → md`), and a one-line summary.

**DO NOT** commit a `.tldr` or `.svg` whose regions, affordances, or labels disagree with `docs/ux/lo-fi.md`. If they disagree, decide which one is right, fix the other, and only then commit.

**DO NOT** let the UL excerpt or the AC drift in the markdown. Re-copy from the source UL and AC files if there is any doubt — the verbatim rules apply to the markdown the same way they apply to the canvas labels.
