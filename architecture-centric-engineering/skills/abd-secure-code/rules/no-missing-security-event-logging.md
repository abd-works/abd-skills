---
scanner: no_missing_security_event_logging_scanner.py
category: lf
---

# Rule: No missing security event logging

Authentication and authorization outcomes must be recorded for detection and investigation. Failed logins, successful logins, logout, token issuance, and privilege changes need structured audit entries — not silent returns (CWE-778, OWASP A09).

## DO

- **DO** log authentication events with event type, actor identifier, outcome, and request correlation id — without credential material.

  **Example (pass):**

  ```javascript
  if (!valid) {
    logger.warn({ event: 'login_failed', userId: email, requestId, outcome: 'invalid_password' });
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  logger.info({ event: 'login_success', userId: user.id, requestId });
  ```

  **Example (pass):**

  ```python
  if not verify_password(user, password):
      logger.warning(
          "authentication_failed",
          extra={"user_id": user_id, "request_id": request_id, "outcome": "invalid_password"},
      )
      raise AuthenticationError("Invalid credentials")
  ```

- **DO** log authorization failures and privilege elevation with the same structured fields.

  **Example (pass):** `audit.log("role_changed", actor=admin_id, target=user_id, new_role="support")`

## DO NOT

- **DO NOT** handle login or logout without any security audit log in the handler.

  **Example (fail):**

  ```javascript
  app.post('/login', async (req, res) => {
    const ok = await verify(req.body.email, req.body.password);
    res.json({ ok });
  });
  ```

- **DO NOT** return authentication failure to the client without recording the attempt.

  **Example (fail):**

  ```java
  if (!passwordEncoder.matches(raw, user.getPasswordHash())) {
      return ResponseEntity.status(401).build();
  }
  ```

- **DO NOT** rely on generic application logs that omit event type and outcome for security flows.

  **Example (fail):** `log.debug("bad login")` with no structured security event field.

**Source:** `context/09_Logging_Alerting_Failures/context/insufficient-logging-and-monitoring.md`, `context/09_Logging_Alerting_Failures/exercises-challenges/insufficient-logging-and-monitoring-challenge.md`
