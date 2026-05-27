---
scanner: no_plaintext_password_storage_scanner.py
category: cf
---

# Rule: No plaintext password storage

Passwords are verifier secrets — store only adaptive password hashes with per-password salts (and optional pepper in KMS). Plaintext, reversible encryption, or fast unsalted digests of passwords fail this rule (CWE-256, OWASP A02).

## DO

- **DO** hash passwords with Argon2id (preferred), scrypt, bcrypt, or PBKDF2-HMAC-SHA256 before persistence.

  **Example (pass):**

  ```python
  from argon2 import PasswordHasher
  password_hash = PasswordHasher().hash(password)
  db.save_user(email=email, password_hash=password_hash)
  ```

  **Example (pass):**

  ```javascript
  const passwordHash = await bcrypt.hash(password, 12);
  await users.insert({ email, passwordHash });
  ```

  **Example (pass):**

  ```java
  String hash = passwordEncoder.encode(rawPassword);
  userRepository.save(new User(email, hash));
  ```

- **DO** store algorithm identifier and cost parameters with each hash for future upgrades (PHC string or structured record).

  **Example (pass):** `$argon2id$v=19$m=47104,t=1,p=1$...` stored in `password_hash` column.

- **DO** re-hash on successful login when work factors are below current policy.

  **Example (pass):** After `verify`, if cost parameter is outdated, `upgrade_hash()` and persist new PHC string.

## DO NOT

- **DO NOT** persist the registration password field as-is from the request body.

  **Example (fail):**

  ```javascript
  await User.create({ email, password: req.body.password });
  ```

  **Example (fail):**

  ```java
  user.setPassword(request.getParameter("password"));
  ```

- **DO NOT** log or echo submitted passwords during authentication flows.

  **Example (fail):**

  ```python
  logger.info("login attempt", extra={"email": email, "password": password})
  ```

- **DO NOT** use MD5, SHA1, or single-round SHA256 without salt for password storage.

  **Example (fail):**

  ```python
  stored = hashlib.sha256(password.encode()).hexdigest()
  ```

**Source:** `context/04-cryotiographic-failures/context/password-storage-cheat-sheet.md`
