/**
 * extract.spec.ts  —  abd-context-app-extractor / Phase 0 scout (web)
 *
 * Copy this file into <repo>/tests/extract.spec.ts, then:
 *   1. Fill in the PAGES array with the routes you want to capture.
 *   2. Run:  npx playwright test extract.spec.ts --reporter=line
 *
 * Outputs (relative to repo root) — three files per page:
 *   docs/extracted-context/app-extraction/pages/<slug>/screenshot.png
 *   docs/extracted-context/app-extraction/pages/<slug>/aria.yaml
 *   docs/extracted-context/app-extraction/pages/<slug>/interactivity.json
 *
 * And one overview:
 *   docs/extracted-context/app-extraction/extraction-overview.md
 *
 * Prerequisites:
 *   - @playwright/test installed (>=1.61 for page.ariaSnapshot())
 *   - A playwright.config.ts with baseURL set
 *   - Dev/test server running (or webServer config in playwright.config.ts)
 *
 * See example-output/ for annotated examples of each file.
 */

import * as fs from 'node:fs'
import * as path from 'node:path'
import { test, expect } from '@playwright/test'

// ---------------------------------------------------------------------------
// ✏️  CONFIGURE — fill these in for your application
// ---------------------------------------------------------------------------

const APP_NAME = 'my-app'                    // used in extraction-overview.md title
const PERSONA  = 'Primary user persona'      // who is doing the exploration

/**
 * Pages to capture.
 *
 * Each entry produces one folder under pages/ and one section in
 * extraction-overview.md. The `slug` becomes the folder name — keep it short,
 * lowercase, hyphenated, and prefix with a two-digit order number.
 *
 * For modals/drawers opened from another page, add them as a sub-test below
 * and use the parent slug with a letter suffix, e.g. "03b-campaign-create-modal".
 */
const PAGES: Array<{
	slug: string
	url: string
	userIntent: string
	domainFocus: string[]
	uxFocus: string[]
	notes: string
}> = [
	// ✏️  Replace with your actual routes
	{
		slug: '01-login',
		url: '/login',
		userIntent: 'Authenticate and gain access to the application.',
		domainFocus: ['authentication'],
		uxFocus: ['login-form'],
		notes: 'Entry point. No content visible until authenticated.',
	},
	{
		slug: '02-home',
		url: '/',
		userIntent: 'Orient to the available features and navigate to primary areas.',
		domainFocus: [],
		uxFocus: ['dashboard', 'sidebar', 'top-nav'],
		notes: 'Home / dashboard view after login.',
	},
	// Add more pages here...
]

// ---------------------------------------------------------------------------
// Output paths — do not change
// ---------------------------------------------------------------------------

const EXTRACTION_ROOT = path.resolve('docs/extracted-context/app-extraction')
const PAGES_DIR       = path.join(EXTRACTION_ROOT, 'pages')

fs.mkdirSync(PAGES_DIR, { recursive: true })

// ---------------------------------------------------------------------------
// Step model
// ---------------------------------------------------------------------------

type PageEntry = {
	step_id:             string
	url_or_view:         string
	user_intent:         string
	domain_focus:        string[]
	ux_focus:            string[]
	aria_snapshot_file:  string
	screenshot_file:     string
	interactivity_file:  string
	notes:               string
}

const pages: PageEntry[] = []

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function waitForRender(page: import('@playwright/test').Page): Promise<void> {
	// Always reload after the initial navigation.
	// MSW service worker intercept behaviour is inconsistent between the page that
	// triggers SW registration (no intercept on first load) and subsequent pages
	// (SW already active, but first navigation may still race with SW claiming).
	// An unconditional reload eliminates the race: by reload time the SW is
	// always active and controlling, so all API calls are intercepted correctly.
	await page.waitForLoadState('domcontentloaded')
	await page.waitForFunction(() => !!navigator.serviceWorker?.controller, { timeout: 15_000 }).catch(() => {})
	await page.reload({ waitUntil: 'domcontentloaded' })
	await page.waitForTimeout(2000)
}

/**
 * Capture raw DOM interactivity facts — written to interactivity.json.
 *
 * Two sections:
 *   clickable_non_semantic  — divs/spans/li with cursor:pointer that are NOT
 *                             natively interactive (button, a, input, …).
 *                             These are invisible to ARIA but clickable.
 *   aria_states             — elements carrying an active ARIA state attribute
 *                             (aria-selected, aria-current, aria-expanded, …).
 *                             Captures which items are selected/expanded at
 *                             the moment of extraction.
 *
 * Raw facts only — no interpretation. Interpretation is downstream.
 * See example-output/pages/01-example-page/interactivity.json for shape.
 */
async function captureInteractivity(
	page: import('@playwright/test').Page,
	pageDir: string,
): Promise<void> {
	const SEMANTIC = ['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA', 'OPTION', 'SUMMARY', 'LABEL']

	const result = await page.evaluate((semanticTags: string[]) => {
		type ClickableEntry = {
			tag: string; text: string; classes: string
			role: string | null; testid: string | null; count: number
		}
		type AriaStateEntry = {
			attribute: string; value: string | null
			tag: string; text: string; role: string | null
		}

		// Non-semantic elements with cursor:pointer — deduplicated by class fingerprint.
		// count > 1 means the same component renders multiple times (e.g. list items).
		const clickableMap = new Map<string, ClickableEntry>()
		document.querySelectorAll('div, span, li, td, article, section').forEach(el => {
			if (semanticTags.includes(el.tagName)) return
			if (window.getComputedStyle(el).cursor !== 'pointer') return
			const classes = [...el.classList].filter(c => c.length < 60).join(' ')
			const key = `${el.tagName}:${classes}`
			const existing = clickableMap.get(key)
			if (existing) {
				existing.count++
			} else {
				clickableMap.set(key, {
					tag: el.tagName,
					text: (el.textContent ?? '').trim().replace(/\s+/g, ' ').slice(0, 80),
					classes,
					role: el.getAttribute('role'),
					testid: el.getAttribute('data-testid'),
					count: 1,
				})
			}
		})

		// Elements with non-false ARIA state attributes — reflects current UI state
		// (selected tab, expanded accordion, checked checkbox, etc.)
		const ariaStates: AriaStateEntry[] = []
		const attrs = ['aria-selected', 'aria-current', 'aria-expanded', 'aria-checked', 'aria-pressed', 'aria-disabled']
		attrs.forEach(attr => {
			document.querySelectorAll(`[${attr}]`).forEach(el => {
				const value = el.getAttribute(attr)
				if (value === null || value === 'false') return  // skip unset / inactive
				ariaStates.push({
					attribute: attr,
					value,
					tag: el.tagName,
					text: (el.textContent ?? '').trim().replace(/\s+/g, ' ').slice(0, 80),
					role: el.getAttribute('role') ?? el.tagName.toLowerCase(),
				})
			})
		})

		return {
			clickable_non_semantic: [...clickableMap.values()],
			aria_states: ariaStates,
		}
	}, SEMANTIC)

	fs.writeFileSync(
		path.join(pageDir, 'interactivity.json'),
		JSON.stringify(result, null, 2),
		'utf-8',
	)
}

/**
 * Capture one page:
 *   1. Creates  pages/<slug>/  folder
 *   2. Screenshot       → pages/<slug>/screenshot.png
 *   3. ARIA snapshot    → pages/<slug>/aria.yaml
 *   4. Interactivity    → pages/<slug>/interactivity.json
 *   5. Pushes PageEntry into the shared log
 */
async function capturePage(
	page: import('@playwright/test').Page,
	opts: {
		slug:        string
		urlOrView:   string
		userIntent:  string
		domainFocus: string[]
		uxFocus:     string[]
		notes:       string
	},
): Promise<void> {
	const pageDir = path.join(PAGES_DIR, opts.slug)
	fs.mkdirSync(pageDir, { recursive: true })

	await page.screenshot({ path: path.join(pageDir, 'screenshot.png'), fullPage: true })

	const ariaContent = await page.ariaSnapshot()

	// Hard-fail: a real rendered page has multiple structural elements.
	// Fewer than 4 lines means the page is still loading, blank, or errored.
	const ariaLines = ariaContent.trim().split('\n').filter(l => l.trim().length > 0)
	expect(
		ariaLines.length,
		`[${opts.slug}] ARIA has only ${ariaLines.length} line(s) — page did not render. ` +
		`Content: ${ariaContent.trim().slice(0, 200)}`,
	).toBeGreaterThan(3)

	// Hard-fail: detect dev-tool overlays (e.g. Vite/TypeScript checker error overlay)
	// injected by build tooling — these fill the ARIA with error text, not real UI.
	const hasToolingOverlay =
		ariaContent.includes('[TypeScript]') ||
		ariaContent.includes('vite-error-overlay') ||
		ariaContent.includes('plugin-error-overlay')
	expect(
		hasToolingOverlay,
		`[${opts.slug}] ARIA contains a build-tooling overlay (TypeScript/Vite errors). ` +
		`Disable error overlays in test/stub mode before running extraction. ` +
		`Vite: set mode !== 'test' && checker({...}) in vite.config.ts.`,
	).toBe(false)

	fs.writeFileSync(path.join(pageDir, 'aria.yaml'), ariaContent, 'utf-8')
	await captureInteractivity(page, pageDir)

	pages.push({
		step_id:            opts.slug,
		url_or_view:        opts.urlOrView,
		user_intent:        opts.userIntent,
		domain_focus:       opts.domainFocus,
		ux_focus:           opts.uxFocus,
		aria_snapshot_file: `./pages/${opts.slug}/aria.yaml`,
		screenshot_file:    `./pages/${opts.slug}/screenshot.png`,
		interactivity_file: `./pages/${opts.slug}/interactivity.json`,
		notes:              opts.notes,
	})
}

// ---------------------------------------------------------------------------
// Tests — one test per top-level page, inline calls for modals/drawers
// ---------------------------------------------------------------------------

test.describe(`abd-context-app-extractor — ${APP_NAME} scout`, () => {
	test.setTimeout(120_000)

	// Auto-generate one test per PAGES entry
	for (const p of PAGES) {
		test(`${p.slug} — ${p.url}`, async ({ page }) => {
			await page.goto(p.url)
			await waitForRender(page)
			await capturePage(page, {
				slug:        p.slug,
				urlOrView:   p.url,
				userIntent:  p.userIntent,
				domainFocus: p.domainFocus,
				uxFocus:     p.uxFocus,
				notes:       p.notes,
			})
		})
	}

	// ✏️  Add hand-crafted tests here for pages that require interaction
	// (opening modals, clicking tabs, navigating to dynamic routes, etc.)
	//
	// Example:
	//
	// test('03b-item-create-modal', async ({ page }) => {
	//   await page.goto('/items')
	//   await waitForRender(page)
	//   await page.getByRole('button', { name: /new item/i }).click()
	//   await page.waitForSelector('[role=dialog]', { timeout: 5000 })
	//   await waitForRender(page)
	//   await capturePage(page, {
	//     slug: '03b-item-create-modal',
	//     urlOrView: '/items (New Item modal)',
	//     userIntent: 'Create a new item.',
	//     domainFocus: ['item'],
	//     uxFocus: ['modal', 'form'],
	//     notes: 'Create dialog. Inputs: name, description.',
	//   })
	// })

	// -------------------------------------------------------------------------
	// Write extraction-overview.md — always last
	// -------------------------------------------------------------------------

	test('99 — Write extraction overview', async () => {
		const allDomainTags = [...new Set(pages.flatMap((p) => p.domain_focus))].sort()
		const allUxTags     = [...new Set(pages.flatMap((p) => p.ux_focus))].sort()

		const frontMatter = [
			'---',
			`app: ${APP_NAME}`,
			'surface: "web"',
			'phase: "scout"',
			`persona: "${PERSONA}"`,
			'automation_tool: "playwright"',
			'pages_dir: "./pages/"',
			'primary_views: ["story", "domain", "ux"]',
			'tags:',
			`  domain: [${allDomainTags.map((t) => `"${t}"`).join(', ')}]`,
			`  ux:     [${allUxTags.map((t) => `"${t}"`).join(', ')}]`,
			'---',
		].join('\n')

		const pageSections = pages.map((p) => {
			const domainList = p.domain_focus.map((f) => `"${f}"`).join(', ')
			const uxList     = p.ux_focus.map((f) => `"${f}"`).join(', ')
			return [
				`## ${p.step_id} — ${p.url_or_view}`,
				'',
				`- user_intent: "${p.user_intent}"`,
				`- domain_focus: [${domainList}]`,
				`- ux_focus: [${uxList}]`,
				`- aria_snapshot: "${p.aria_snapshot_file}"`,
				`- screenshot: "${p.screenshot_file}"`,
				`- interactivity: "${p.interactivity_file}"`,
				`- notes: |`,
				`  ${p.notes}`,
				'',
			].join('\n')
		})

		const report = [
			`# ${APP_NAME} — Extraction Overview`,
			'',
			`Generated: ${new Date().toISOString()}`,
			`Phase: scout (abd-context-app-extractor Phase 0)`,
			`Source: tests/extract.spec.ts via Playwright.`,
			'',
			frontMatter,
			'',
			'---',
			'',
			...pageSections.flatMap((s) => [s, '---', '']),
		].join('\n')

		const outPath = path.join(EXTRACTION_ROOT, 'extraction-overview.md')
		fs.writeFileSync(outPath, report, 'utf-8')

		console.log(`\nExtraction overview: ${outPath}`)
		console.log(`Pages:               ${PAGES_DIR}/`)
		console.log(`Pages recorded:      ${pages.length}`)

		expect(pages.length).toBeGreaterThan(0)
	})
})
