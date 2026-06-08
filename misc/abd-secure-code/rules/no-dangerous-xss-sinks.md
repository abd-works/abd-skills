---
scanner: no_dangerous_xss_sinks_scanner.py
category: if
---

# Rule: No dangerous XSS sinks

When untrusted content renders in a browser, use framework auto-escaping or context-appropriate encoding. APIs that treat strings as HTML or script bypass defenses and enable cross-site scripting.

## DO

- **DO** render user content through framework text nodes or escaped templates.

  **Example (pass):** React `{userDisplayName}` in JSX — default escaping applies.

- **DO** sanitize HTML with a maintained library (e.g. DOMPurify) when rich text is required, then assign to a controlled sink.

  **Example (pass):**

  ```javascript
  const clean = DOMPurify.sanitize(userHtml);
  element.textContent = clean; // prefer textContent when HTML not required
  ```

## DO NOT

- **DO NOT** assign untrusted strings to `innerHTML`, `outerHTML`, or `dangerouslySetInnerHTML`.

  **Example (fail):**

  ```javascript
  div.innerHTML = req.query.message;
  ```

- **DO NOT** disable template auto-escaping without a documented sanitization step.

  **Example (fail):** Jinja `{{ bio | safe }}` where `bio` originates from user input.

**Source:** `context/05-injection-flaws/context/cross-site-scripting-prevention-cheat-sheet.md`
