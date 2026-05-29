# Rule: Performance constraints are met or, if undeclared, the baseline is not regressed

**Scanner:** AI review

If the host project declares performance constraints (initial paint budget, time-to-interactive budget, frame budget for animations, bundle size budget, render-time budget), the screen implementation meets them and the project's perf checks pass. If the host project does not declare explicit budgets, the implementation does not regress whatever the project's current baseline is.

## DO

- Read the host project's perf configuration (`lighthouserc`, bundle-size config, perf test thresholds, frame budget docs) before implementing and design within those bounds.

  **Example (pass):** Host project has a `bundlesize.config.json` that caps a screen at 80 KB gzipped — the new screen's bundle is well inside that cap and the check passes.

- Lazy-load heavy dependencies the screen does not need on first paint.

  **Example (pass):** A path-picker file dialog component is dynamically imported only when `Browse...` is clicked.

- Keep animations within the project's frame budget.

  **Example (pass):** Transition animations use transform/opacity (cheap), stay under 16 ms per frame, and are reduced or disabled when `prefers-reduced-motion` is set.

## DO NOT

- Add heavy dependencies for cosmetic reasons.

  **Example (fail):** Importing an entire icon library to render two icons; importing a full animation framework for a single fade.

- Block first paint on data that is not needed to render the screen.

  **Example (fail):** The screen waits on a network call that has nothing to do with the AC before any region renders.

- Silence perf checks rather than fix the regression.

  **Example (fail):** Raising the bundle-size cap because the new code is over budget, without justifying the change in `corrections-log.md`.
