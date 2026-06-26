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

## Placement in `capturePage`

```
screenshot → ariaSnapshot → [Guard 1] → [Guard 2] → writeFile → push to pages[]
```

Never write files or push to the page log before the guards pass. A partial write with bad data is worse than a clean failure.
