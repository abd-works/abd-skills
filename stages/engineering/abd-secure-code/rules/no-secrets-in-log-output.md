---
scanner: no_secrets_in_log_output_scanner.py
category: lf
---

# Rule: No secrets in log output

Logs often flow to centralized systems with broad access. Passwords, API keys, session tokens, and Authorization headers must never appear in log lines — even during debugging (CWE-532, OWASP A09).

## DO

- **DO** log security events with structured fields: event type, actor id, outcome, request id — not credential material.

  **Example (pass):**

  ```javascript
  logger.info({
    event: 'login_failed',
    userId: user.id,
    requestId: ctx.requestId,
    outcome: 'invalid_password',
  });
  ```

  **Example (pass):**

  ```python
  logger.warning(
      "authentication_failed",
      extra={"user_id": user_id, "request_id": request_id},
  )
  ```

- **DO** mask or omit token and session fields; hash session ids if correlation requires it.

  **Example (pass):** Log `session_id_prefix=abc123…` (first 8 chars) only in debug tiers with RBAC.

## DO NOT

- **DO NOT** log raw passwords, API keys, or Authorization header values.

  **Example (fail):**

  ```python
  logger.info("login attempt", extra={"email": email, "password": password})
  ```

- **DO NOT** log full JWT or reset tokens in info-level production logs.

  **Example (fail):**

  ```javascript
  console.log('token issued', { token: jwt });
  ```

- **DO NOT** print secrets to stdout/stderr in production code paths.

  **Example (fail):**

  ```java
  log.info("API call with key {}", apiKey);
  ```

**Source:** `context/09_Logging_Alerting_Failures/context/insufficient-logging-and-monitoring.md`
