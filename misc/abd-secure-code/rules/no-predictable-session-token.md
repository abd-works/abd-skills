---
scanner: no_predictable_session_token_scanner.py
category: af
---

# Rule: No predictable session token

Session identifiers and authentication tokens must be generated with a cryptographically secure random number generator (CSPRNG) and sufficient entropy (128+ bits). Predictable session ids enable session hijacking, account takeover, and horizontal privilege escalation.

## DO

- **DO** use the framework session manager or `secrets` / `crypto.randomBytes` / `SecureRandom` for session id generation.

  **Example (pass):**

  ```python
  import secrets
  session_id = secrets.token_urlsafe(32)
  session_store.save(session_id, user_id)
  ```

  **Example (pass):**

  ```javascript
  req.session.regenerate((err) => {
    // express-session generates high-entropy id server-side
  });
  ```

  **Example (pass):**

  ```java
  String sessionId = UUID.randomUUID().toString();
  sessionRepository.create(sessionId, userId);
  ```

- **DO** rotate session id on login, privilege elevation, and logout; enforce idle and absolute timeouts server-side.

  **Example (pass):** Invalidate server-side session record on logout; issue new session id after successful authentication.

## DO NOT

- **DO NOT** derive session ids from username, email, or numeric user id.

  **Example (fail):**

  ```javascript
  req.session.id = req.body.username;
  ```

- **DO NOT** use incrementing counters, small random ranges, or `Math.random()` for session tokens.

  **Example (fail):**

  ```java
  sessionId = String.valueOf(random.nextInt(100000));
  ```

**Source:** `context/07_Authentication_Failures/context/improper-authentication.md`, `context/07_Authentication_Failures/exercises-challenges/weak-session-token-generation.md`

See also: **no-jwt-none-algorithm**, **no-client-side-auth-trust** for token verification and client-side session state.
