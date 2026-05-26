---
scanner: no_jwt_none_algorithm_scanner.py
category: af
---

# Rule: No JWT none algorithm

JSON Web Tokens must be verified with an explicit allow-list of strong algorithms. Accepting `alg: none`, skipping signature verification, or verifying with a null secret enables token forgery (CWE-347, OWASP A07).

## DO

- **DO** verify JWTs with HMAC-SHA256/384/512 or asymmetric algorithms (RS256, ES256) and a configured secret or public key.

  **Example (pass):**

  ```javascript
  const payload = jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS256'] });
  ```

  **Example (pass):**

  ```python
  jwt.decode(token, key, algorithms=["RS256"], audience="api.example.com")
  ```

  **Example (pass):**

  ```java
  Jwts.parserBuilder().setSigningKey(publicKey).requireAudience("api").build().parseClaimsJws(token);
  ```

- **DO** reject tokens whose header algorithm is not on the allow-list.

  **Example (pass):** Middleware returns 401 when `alg` is missing or not in configured algorithms.

## DO NOT

- **DO NOT** verify JWTs with `algorithms: ['none']` or equivalent.

  **Example (fail):**

  ```javascript
  jwt.verify(token, null, { algorithms: ['none'] });
  ```

- **DO NOT** decode JWT payload without signature verification for authentication decisions.

  **Example (fail):**

  ```python
  payload = jwt.decode(token, options={"verify_signature": False})
  ```

- **DO NOT** sign tokens with `algorithm: 'none'`.

  **Example (fail):**

  ```javascript
  jwt.sign({ sub: user.id }, null, { algorithm: 'none' });
  ```

**Source:** `context/07_Authentication_Failures/context/improper-authentication.md`
