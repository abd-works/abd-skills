---
scanner: no_excessive_response_data_scanner.py
category: id
---

# Rule: No excessive response data

APIs must return only the fields the client is authorized to see. Serializing full domain entities, ORM models, or database rows exposes internal fields, PII, and secrets (CWE-200, OWASP A04).

## DO

- **DO** map domain objects to DTOs, view models, or serializers with an explicit allow-list before responding.

  **Example (pass):**

  ```javascript
  const user = await users.findById(req.params.id);
  return res.json({ id: user.id, email: user.email, displayName: user.displayName });
  ```

  **Example (pass):**

  ```python
  patient = service.get_patient(patient_id)
  return jsonify(PatientSummary.from_entity(patient))
  ```

  **Example (pass):**

  ```java
  User user = userRepository.findById(id);
  return ResponseEntity.ok(UserResponse.from(user));
  ```

- **DO** use `@JsonView`, field exclusion annotations, or schema-driven serializers when returning nested graphs.

  **Example (pass):** Public profile endpoint returns `UserPublicView` only — no `ssn`, `passwordHash`, or internal flags.

## DO NOT

- **DO NOT** return the full persisted entity to HTTP clients.

  **Example (fail):**

  ```javascript
  const user = await User.findById(req.params.id);
  res.json(user);
  ```

- **DO NOT** serialize ORM `to_dict()` / `__dict__` output without filtering.

  **Example (fail):**

  ```python
  return jsonify(user.__dict__)
  ```

- **DO NOT** send raw database rows or JPA entities in REST responses.

  **Example (fail):**

  ```java
  return ResponseEntity.ok(userRepository.findById(id).get());
  ```

**Source:** `context/06-Insecure-Design/context/sensitive-data-exposure.md`
