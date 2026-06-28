# Rule: Capture Quality Guards

Every `capturePage` call in an extraction spec MUST hard-fail if the captured page did not render real UI content. Write these two assertions immediately after `page.ariaSnapshot()`, before writing any files.

## Guard 1 — Minimum ARIA depth

```ts
const ariaLines = ariaContent.trim().split('\n').filter(l => l.trim().length > 0)
expect(
  ariaLines.length,
  `[${opts.slug}] ARIA has only ${ariaLines.length} line(s) — page did not render. ` +
  `Content: ${ariaContent.trim().slice(0, 200)}`,
).toBeGreaterThan(3)
```

**Why:** A loading spinner, blank screen, or fatal app error typically produces 0–2 ARIA nodes. Fewer than 4 lines is a hard signal the page was not ready. Without this guard the test passes silently and the extraction output contains empty or meaningless ARIA files.

**DO NOT** lower the threshold to work around a page that genuinely renders sparse content. Instead fix the underlying issue (render timing, auth, MSW registration) and re-run.

## Guard 2 — No build-tooling overlays

```ts
const hasToolingOverlay =
  ariaContent.includes('[TypeScript]') ||
  ariaContent.includes('vite-error-overlay') ||
  ariaContent.includes('plugin-error-overlay')
expect(
  hasToolingOverlay,
  `[${opts.slug}] ARIA contains a build-tooling overlay (TS/Vite errors). ` +
  `Disable error overlays in stub/test mode before running extraction. ` +
  `Vite: set mode !== 'stub' && checker({...}) in vite.config.ts.`,
).toBe(false)
```

**Why:** Vite's `vite-plugin-checker` and similar tools inject a full-screen error overlay into the DOM when TypeScript errors exist. This overlay fills the ARIA with error messages and obscures the real UI. The extraction data becomes worthless.

**Fix:** In `vite.config.ts`, gate the checker plugin on the build mode so it is off during extraction:

```ts
// vite.config.ts
plugins: [
  react(),
  mode !== 'stub' && checker({ typescript: true }),
]
```

## Rule for `waitForRender`

Use `domcontentloaded` + service-worker controller check, not `networkidle`. `networkidle` hangs indefinitely when MSW or other service worker interceptors are active because the SW's internal fetch loop is counted as pending network activity.

```ts
async function waitForRender(page) {
  // Always reload — eliminates the race between SW registration and first-navigation
  // intercept regardless of whether this is the first or tenth test in the session.
  await page.waitForLoadState('domcontentloaded')
  await page.waitForFunction(() => !!navigator.serviceWorker?.controller, { timeout: 15_000 }).catch(() => {})
  await page.reload({ waitUntil: 'domcontentloaded' })
  await page.waitForTimeout(2000)
}
```

**DO NOT** use a conditional reload (`if (!controlled) { reload }`). The SW may already be registered but the current page's first navigation still races with SW claiming. An unconditional reload is the only fully reliable pattern.

## Rule: Complete Interactivity — Capture All Interactive States

**Correction (2026-06-26):** Extraction tests MUST simulate user interactions to capture every meaningful UI state, not just the initial page load. Static capture of the landing state is not enough.

**For every page, identify and capture:**

1. **Expanded states** — accordions, collapsibles, tabs. Click each expandable and capture the open state as a separate slug (e.g. `05b-my-billing-past-payments`).
2. **Form states** — fill inputs with realistic values before capture. Capture both empty (initial) and filled states.
3. **Wizard steps** — for multi-step flows, navigate directly to the correct step URL rather than clicking through intermediate screens. Example: `/sign-up/plan-starter` starts the Sign-Up wizard directly at the CreateAccount step (`startIndex=2`), bypassing the Slick slider carousel.
4. **Modal / sheet triggers** — if a button opens a modal or bottom sheet, click it and capture the open state.

**DO NOT** try to `force: true` click elements buried under overlay components (Slick slider, MUI Backdrop, Portal). Instead, find the direct navigation path: URL params, query strings, or programmatic state that bypasses the overlay entirely.

**Naming convention for interactive states:**

```
<base-slug>         → initial / default state
<base-slug>-<state> → interactive state (e.g. 05b-my-billing-past-payments)
```

**Example — billing accordions:**

```typescript
// Initial state
test('05-my-billing', ...) { await page.goto('/my/billing'); ... }

// Expanded accordion state
test('05b-my-billing-past-payments', async ({ page }) => {
  await page.goto('/my/billing')
  await waitForRender(page)
  const btn = page.getByRole('button', { name: /past payments/i })
  if (await btn.isVisible()) { await btn.click(); await page.waitForTimeout(1000) }
  await capturePage(page, { slug: '05b-my-billing-past-payments', ... })
})
```

**Example — wizard direct navigation (bypass carousel):**

```typescript
// Correct: navigate directly to the step URL
test('02b-sign-up-create-account', async ({ page }) => {
  await page.goto('/sign-up/plan-starter') // planId in URL → startIndex=2 (CreateAccount)
  await waitForRender(page)
  await capturePage(page, { slug: '02b-sign-up-create-account', ... })
})

// WRONG: clicking "Sign up now" inside a Slick slider carousel
// The carousel overlay intercepts pointer events; force-click fires DOM event
// but React synthetic event may not propagate to the onClick handler correctly.
```

## Placement in `capturePage`

```
screenshot → ariaSnapshot → [Guard 1] → [Guard 2] → writeFile → push to pages[]
```

Never write files or push to the page log before the guards pass. A partial write with bad data is worse than a clean failure.
