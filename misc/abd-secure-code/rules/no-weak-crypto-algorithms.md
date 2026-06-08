---
scanner: no_weak_crypto_algorithms_scanner.py
category: cf
---

# Rule: No weak crypto algorithms

Cryptographic choices must match the threat: password hashing uses adaptive algorithms; transport uses TLS 1.2+; symmetric encryption uses modern AEAD; tokens use CSPRNG. Legacy digests and ciphers fail when used for security-sensitive operations (CWE-327, OWASP A02).

## DO

- **DO** use Argon2id, scrypt, bcrypt, or PBKDF2 for password hashing — not general-purpose digests.

  **Example (pass):**

  ```javascript
  const hash = await bcrypt.hash(password, 12);
  ```

- **DO** use AES-GCM or ChaCha20-Poly1305 for authenticated encryption at rest when encryption is required.

  **Example (pass):**

  ```javascript
  crypto.createCipheriv('aes-256-gcm', key, iv);
  ```

  **Example (pass):**

  ```java
  Cipher.getInstance("AES/GCM/NoPadding");
  ```

- **DO** use `secrets`, `crypto.randomBytes`, or `SecureRandom` for session tokens, reset links, and CSRF secrets.

  **Example (pass):**

  ```python
  import secrets
  token = secrets.token_urlsafe(32)
  ```

## DO NOT

- **DO NOT** use MD5 or SHA1 for password storage or integrity protection of security artifacts.

  **Example (fail):**

  ```python
  stored = hashlib.md5(password.encode()).hexdigest()
  ```

  **Example (fail):**

  ```java
  MessageDigest.getInstance("MD5");
  ```

- **DO NOT** use `Math.random()`, `random.randint()`, or `java.util.Random` for session tokens or security nonces.

  **Example (fail):**

  ```javascript
  const token = Math.floor(Math.random() * 1e6);
  ```

- **DO NOT** accept JWT with `alg: none` or use SHA1withRSA in new signature code.

  **Example (fail):**

  ```javascript
  jwt.sign(payload, secret, { algorithm: 'none' });
  ```

**Source:** `context/04-cryotiographic-failures/context/guildline-weak-algoithm-use.md`
