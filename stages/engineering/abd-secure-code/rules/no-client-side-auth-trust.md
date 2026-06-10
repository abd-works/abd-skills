---
scanner: no_client_side_auth_trust_scanner.py
category: af
---

# Rule: No client-side auth trust

Authentication state must live server-side or in signed, integrity-protected tokens. Encoding user identity or roles in client-readable cookies (base64 JSON, unsigned blobs) lets attackers forge privileges (CWE-287, OWASP A07).

## DO

- **DO** keep session state in a server-side store keyed by a random, high-entropy session id.

  **Example (pass):**

  ```javascript
  req.session.userId = user.id;
  req.session.role = user.role;
  ```

- **DO** use signed (and when needed, encrypted) cookies or JWTs with verified signatures and validated claims.

  **Example (pass):**

  ```javascript
  res.cookie('session', signedSessionId, { httpOnly: true, secure: true, signed: true });
  ```

## DO NOT

- **DO NOT** base64-encode a JSON user object into a cookie and treat it as authoritative on read.

  **Example (fail):**

  ```javascript
  const payload = Buffer.from(JSON.stringify({ role: user.role, id: user.id })).toString('base64');
  res.cookie('user', payload);
  ```

  **Example (fail):**

  ```javascript
  const session = JSON.parse(Buffer.from(req.cookies.user, 'base64').toString());
  if (session.role === 'admin') { /* ... */ }
  ```

- **DO NOT** decode client cookies with `atob` / `Base64.getDecoder()` and trust embedded roles without signature verification.

  **Example (fail):**

  ```java
  String json = new String(Base64.getDecoder().decode(request.getCookie("user").getValue()));
  UserSession session = objectMapper.readValue(json, UserSession.class);
  ```

- **DO NOT** accept client-supplied `isAdmin` or `role` fields without server-side authorization checks.

  **Example (fail):** Trusting `req.body.role` on login to set persistent admin access.

**Source:** `context/07_Authentication_Failures/context/improper-authentication.md`
