# Rule: smoke-test-reachability

**Artifact:** The `## Smoke Test Results` section of `docs/stubs/stub-inventory.md` and the smoke-test script placed in the target repo.

The smoke test confirms that the application, with all stubs in place, reaches every significant screen without crashing, redirecting unexpectedly, or rendering an incomplete page. A screen is reachable when the automation tool returns a non-empty semantic tree (ARIA snapshot or UIA tree) with at least one landmark, heading, or interactive element, and no error-page pattern is present.

## DO

- Choose the automation tool from the shared **`../../reference/tool-selection.md`** based on the application surface before writing the smoke-test script.

  **Example (pass):** The target is a Next.js web app. The smoke-test script uses Playwright `page.ariaSnapshot()`. The `tool` field in `stub-inventory.md` front matter is `playwright`.

- Navigate to every screen listed in the application's routing configuration (`routes.ts`, `app/` directory structure, `openapi.yaml` paths) or equivalent entry-point inventory.

  **Example (pass):** The app has routes `/login`, `/dashboard`, `/campaigns`, `/campaigns/:id`, and `/settings`. All five are visited in the smoke-test script, and all five appear in the `## Smoke Test Results` table.

- Record each screen as PASS, FAIL, or WARN with a one-line note that states the key landmark or interactive element observed (PASS) or the failure reason (FAIL / WARN).

  **Example (pass):**
  ```
  01-login       PASS — email and password inputs, sign-in button visible
  02-dashboard   PASS — header nav, usage widget, billing summary present
  03-campaigns   WARN — spinner on first load; re-ran with 2 s additional wait; PASS on retry
  ```

- Re-run a FAIL or WARN screen once after adjusting the wait time or the stub state. If it still fails, record the failure reason and do not include it as PASS in the final inventory.

  **Example (pass):** `04-settings FAIL — redirected to /login; session cookie not injected by auth stub. Updated auth stub to set cookie. Re-run: PASS — profile form and notification preferences visible.`

- Seed stub state to make multi-step screens directly navigable without running the full flow. The smoke test must be able to reach a checkout-complete or onboarding-step-3 screen by pre-populating the session or database fixture the stub controls.

  **Example (pass):** The order confirmation screen at `/orders/:id/confirmation` is reached by setting `orderId: stub-order-001` in the session via the stub, navigating directly to `/orders/stub-order-001/confirmation`.

## DO NOT

- Mark a screen as PASS when the only element in the ARIA snapshot is a loading spinner, skeleton, or placeholder.

  **Example (fail):** `03-campaigns PASS — one spinner element found`. A spinner indicates the page did not finish rendering; this is a FAIL or WARN pending a longer wait or a stub fix.

- Skip screens that require multi-step flows to reach. Pre-seed the stub state instead.

  **Example (fail):** The order confirmation screen is omitted with the note "requires checkout completion". The smoke test must navigate there directly via stub-seeded session state.

- Use a pixel-based tool (e.g. screenshot only, pyautogui) as the primary smoke-test mechanism when a semantic-tree tool is available for the surface type.

  **Example (fail):** A web app smoke test uses only `page.screenshot()`. Playwright is installed; `page.ariaSnapshot()` must be the primary record.

- Count a redirect to a login or error page as PASS for the originally requested screen.

  **Example (fail):** Navigating to `/dashboard` redirects to `/login`. The smoke test records `02-dashboard PASS` because the login page loads. The PASS must be for the intended screen, not the redirect target. Record `02-dashboard FAIL — redirected to /login; auth stub missing session token`.

**Source:** Engagement convention (abd-stub-external-dependencies authoring, 2026-06-25).
