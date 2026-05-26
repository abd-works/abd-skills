---
scanner: no_sensitive_error_disclosure_scanner.py
category: ec
---

# Rule: No sensitive error disclosure

Error responses shown to end users must be generic. Detailed stack traces, framework versions, and file paths belong in secure internal logs correlated by request id — not in HTTP bodies.

## DO

- **DO** return a stable user message plus opaque reference id; log full diagnostics server-side.

  **Example (pass):**

  ```javascript
  logger.error({ requestId, err });
  res.status(500).json({ message: 'An internal error occurred', reference: requestId });
  ```

- **DO** disable framework debug pages in production deployments.

  **Example (pass):** `app.set('env', 'production')` with centralized exception handler.

## DO NOT

- **DO NOT** send `err.stack`, Python tracebacks, or SQL error text to clients.

  **Example (fail):**

  ```javascript
  res.status(500).send(err.stack);
  ```

- **DO NOT** enable verbose SQL or ORM logging that echoes to API responses.

  **Example (fail):** Returning `{ error: dbError.detail }` from a catch block on login failure.

**Source:** `context/10_Mishandling_of_Exceptional_Conditions/context/error-details.md`
