---
scanner: no_insufficient_login_rate_limiting_scanner.py
category: af
---

# Rule: No insufficient login rate limiting

Authentication endpoints must resist credential stuffing and brute force: per-IP and per-account rate limits, progressive delays, lockouts, and structured logging of failures (CWE-307, OWASP A07). A login handler with no throttling fails this rule.

## DO

- **DO** enforce rate limits and progressive backoff on login, password reset, and MFA endpoints.

  **Example (pass):**

  ```javascript
  app.post('/login', loginRateLimiter, captchaWhenSuspicious, async (req, res) => {
    await recordAuthAttempt({ ip: req.ip, username: req.body.email, outcome });
  });
  ```

  **Example (pass):**

  ```python
  @limiter.limit("5 per minute")
  def login(request):
      audit_log.info("auth_attempt", extra={"ip": request.META["REMOTE_ADDR"]})
  ```

- **DO** return generic errors (`Invalid username or password`) — same message for unknown user and bad password.

  **Example (pass):** Single error string regardless of which check failed.

## DO NOT

- **DO NOT** expose login endpoints with unlimited attempts and no monitoring.

  **Example (fail):**

  ```javascript
  app.post('/login', async (req, res) => {
    const user = await db.findByEmail(req.body.email);
    if (!user || !(await bcrypt.compare(req.body.password, user.hash))) {
      return res.status(401).json({ error: 'invalid' });
    }
  });
  ```

- **DO NOT** reveal account existence through different error messages or timing on login failure.

  **Example (fail):** `User not found` vs `Wrong password` responses.

**Source:** `context/green_belt_assessment/e0523/challenge-3.md`, `context/07_Authentication_Failures/context/insufficient-anti-automation.md`
