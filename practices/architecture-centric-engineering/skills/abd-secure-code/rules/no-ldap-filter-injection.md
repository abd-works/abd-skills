---
scanner: no_ldap_filter_injection_scanner.py
category: if
---

# Rule: No LDAP filter injection

LDAP search filters must treat user input as data, not filter syntax. Substituting untrusted values into filter strings like `(email={0})` without RFC 4515 escaping enables filter injection — attackers can broaden queries to return all directory entries (CWE-90, OWASP A03).

## DO

- **DO** escape LDAP filter special characters (`*`, `(`, `)`, `\`, NUL) per RFC 4515 before substitution.

  **Example (pass):**

  ```java
  String safeEmail = LdapEncoder.filterEncode(email);
  String filter = "(mail=" + safeEmail + ")";
  ctx.search(baseDn, filter, controls);
  ```

  **Example (pass):**

  ```python
  from ldap3.utils.conv import escape_filter_chars
  safe = escape_filter_chars(email)
  conn.search(base, f"(mail={safe})", attributes=attrs)
  ```

- **DO** use library APIs that guarantee parameterized filter escaping — verify in docs, do not assume `{0}` templates escape automatically.

  **Example (pass):** Spring LDAP `EqualsFilter("mail", email)` builds a safe filter internally.

## DO NOT

- **DO NOT** pass raw user input into MessageFormat-style LDAP filters without escaping.

  **Example (fail):**

  ```java
  ldapTemplate.search("(email=" + email + ")", handler);
  ```

- **DO NOT** build LDAP filters via string concatenation with request parameters.

  **Example (fail):**

  ```javascript
  const filter = `(uid=${req.query.username})`;
  client.search(baseDN, { filter });
  ```

**Source:** `context/green_belt_assessment/e0523/challenge-9.md`, `context/05-injection-flaws/context/guideline-sql-injection.md` (injection family)
