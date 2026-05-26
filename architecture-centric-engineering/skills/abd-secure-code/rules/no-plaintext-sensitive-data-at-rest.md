---
scanner: no_plaintext_sensitive_data_at_rest_scanner.py
category: cf
---

# Rule: No plaintext sensitive data at rest

PII and regulated data (SSN, tax id, payment identifiers, health records) must be encrypted, tokenized, or otherwise protected before persistence. Plaintext storage in application databases or files fails this rule — distinct from password hashing (CWE-312, OWASP A02).

## DO

- **DO** encrypt or tokenize sensitive fields with envelope encryption or a KMS-backed data key before insert/update.

  **Example (pass):**

  ```python
  encrypted_ssn = field_encryptor.encrypt(ssn, key_id=PII_KEY)
  db.save_user(email=email, ssn_ciphertext=encrypted_ssn)
  ```

  **Example (pass):**

  ```javascript
  const token = await vault.tokenize('ssn', ssn);
  await users.insert({ email, ssnToken: token });
  ```

  **Example (pass):**

  ```java
  String ciphertext = piiCipher.encrypt(rawSsn);
  userRepository.save(new User(email, ciphertext));
  ```

- **DO** store algorithm, key id, and version metadata needed for rotation and decryption.

  **Example (pass):** Column `ssn_ciphertext` plus `encryption_key_id` and `cipher_version`.

## DO NOT

- **DO NOT** persist SSN, card numbers, or national ids from the request body without encryption.

  **Example (fail):**

  ```javascript
  await Profile.create({ userId, ssn: req.body.ssn });
  ```

  **Example (fail):**

  ```python
  db.execute("INSERT INTO users (ssn) VALUES (%s)", (request.form["ssn"],))
  ```

  **Example (fail):**

  ```java
  user.setSsn(request.getParameter("ssn"));
  userRepository.save(user);
  ```

- **DO NOT** store reversible “encoding” (base64, hex) instead of cryptographic protection.

  **Example (fail):** `stored = base64.b64encode(ssn.encode())` without encryption.

**Source:** `context/04-cryotiographic-failures/exercises-challenges/sensitive-data-storage-plain-text-storage-of-sensitive-info.md`, `context/04-cryotiographic-failures/context/password-storage-cheat-sheet.md`
