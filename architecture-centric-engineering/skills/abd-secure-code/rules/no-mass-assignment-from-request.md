---
scanner: no_mass_assignment_from_request_scanner.py
category: df
---

# Rule: No mass assignment from request

HTTP request bodies are untrusted input. Blindly copying every field into persistence models lets attackers set privileged attributes (`role`, `isAdmin`, `accountVerified`) unless each update uses an explicit allow-list.

## DO

- **DO** map allowed fields explicitly from DTO to entity.

  **Example (pass):**

  ```javascript
  await User.update(userId, {
    displayName: body.displayName,
    timezone: body.timezone,
  });
  ```

- **DO** use schema validation (Zod, Joi, pydantic) that strips or rejects unknown keys before persistence.

  **Example (pass):** `profileUpdateSchema.parse(req.body)` with `.strict()` or known field set.

## DO NOT

- **DO NOT** spread or assign entire `req.body` / `request.json` into ORM update/create.

  **Example (fail):**

  ```javascript
  await User.findByIdAndUpdate(id, req.body);
  ```

- **DO NOT** unpack request dicts into model constructors without filtering.

  **Example (fail):**

  ```python
  User(**request.json)
  ```

- **DO NOT** bind entire request maps into entities without an allow-list.

  **Example (fail):**

  ```java
  BeanUtils.populate(product, request.getParameterMap());
  ```

**Source:** `context/08_Software_or_Data_Integrity_Failures/context/mass-assignment.md`, `context/08_Software_or_Data_Integrity_Failures/exercises-challenges/mass-assigment-challenge.md`
