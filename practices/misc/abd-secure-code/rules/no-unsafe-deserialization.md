---
scanner: no_unsafe_deserialization_scanner.py
category: df
---

# Rule: No unsafe deserialization

Untrusted serialized object graphs can execute attacker-controlled code or corrupt application state. Prefer JSON/DTO mapping with schema validation; never feed untrusted bytes to language-native deserializers.

## DO

- **DO** parse JSON (or similar text formats) into plain objects and map fields explicitly to domain types.

  **Example (pass):**

  ```javascript
  const dto = orderSchema.parse(JSON.parse(body));
  const order = Order.fromDto(dto);
  ```

- **DO** verify signatures or HMACs on serialized payloads before parsing when integrity matters.

  **Example (pass):** Reject payload when `verify_hmac(payload, signature, secret)` fails.

## DO NOT

- **DO NOT** call native deserializers on request bodies or message queue payloads.

  **Example (fail):**

  ```python
  obj = pickle.loads(request.data)
  ```

- **DO NOT** use `yaml.load` without `SafeLoader` on external input.

  **Example (fail):** `yaml.load(untrusted_yaml_string)`

**Source:** `context/08_Software_or_Data_Integrity_Failures/context/deserialization-of-untrusted-data.md`
