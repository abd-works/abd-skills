---
scanner: no_eval_dynamic_code_execution_scanner.py
category: if
---

# Rule: No eval or dynamic code execution

`eval`, `exec`, `Function`, and string-form `setTimeout` turn data into code. Any path that executes attacker-influenced strings is remote code execution regardless of language.

## DO

- **DO** parse structured data with `JSON.parse`, schema validators, or safe parsers — then branch on typed values.

  **Example (pass):**

  ```javascript
  const config = JSON.parse(raw);
  if (typeof config.retries !== 'number') throw new ValidationError('retries');
  ```

- **DO** use sandboxed expression engines only when absolutely required, with strict allow-lists and no filesystem/network.

  **Example (pass):** Dedicated rules engine library configured with a fixed function set — not `eval`.

## DO NOT

- **DO NOT** call `eval`, `exec`, or `new Function` on request-derived strings.

  **Example (fail):**

  ```javascript
  const result = eval(req.query.expression);
  ```

- **DO NOT** pass string callbacks to timer APIs.

  **Example (fail):** `setTimeout("updateCount(" + n + ")", 1000)`

**Source:** `context/05-injection-flaws/context/cross-site-scripting-prevention-cheat-sheet.md` (unsafe sinks / script execution)
