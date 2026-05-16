# `docs/ux/hi-fi.md` stays in sync with the canvas

The markdown spec and the canvas are two views of the same hi-fi screen. They must agree at every commit.

**DO** author or update `docs/ux/hi-fi.md` **before** driving the canvas. The markdown carries the committed aesthetic direction, the typography role table, the colour role table, the density, and the spacing scale. The canvas applies those decisions.

**DO** read the updated canvas after the agent finishes and reflect any value change (new type style, new colour, changed spacing value, changed density) back into the role tables in `docs/ux/hi-fi.md` in the same skill run.

**DO** append a row to the change log in `docs/ux/hi-fi.md` every time the canvas changes, recording date, direction (`md → canvas` or `canvas → md`), and a one-line summary.

**DO NOT** commit a `.tldr` or `.svg` whose typography, colour, density, or spacing values disagree with the role tables in `docs/ux/hi-fi.md`. If they disagree, decide which one is right, fix the other, and only then commit.

**DO NOT** allow one-off type styles, one-off colours, or one-off spacing values on the canvas that are not declared as roles in `docs/ux/hi-fi.md`. Every visual decision on the canvas is named in the markdown.
