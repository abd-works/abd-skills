# Secure Code — Concepts

## Threat-informed defaults

Each rule maps to a **real failure mode** from the Secure Code Warrior corpus (injection, cryptographic failure, unsafe deserialization, mass assignment, information disclosure). Secure code is not a separate checklist bolted on at the end — it is how you handle **untrusted input**, **secrets**, **errors**, and **output encoding** in normal production modules.

---

## Parameterized data access

Databases, shells, and HTML parsers must receive **data as data**. SQL uses bound parameters; shell invocation uses argument arrays; browser output uses escaping or sanitization. Concatenating or interpolating untrusted strings into executable contexts is the common root of injection flaws.

---

## Secrets and verifiers

**Secrets** (API keys, private keys) never belong in source control. **Passwords** are one-way verifiers — store adaptive hashes with salts, not plaintext or reversible encryption. **Tokens** and session identifiers require cryptographically secure randomness.

---

## Fail safe to users, verbose to logs

Clients see generic errors with a correlation id. Operators see stack traces, query errors, and security events in protected logs — not in HTTP responses.

---

## Rules and scanners

**`rules/*.md`** state pass/fail conditions grounded in **`context/`** sources. **`scanners/python/`**, **`scanners/java/`**, and **`scanners/javascript/`** enforce the same rule stems mechanically. Run every language folder that matches files in the engagement workspace.

---

## Language stacks

| Stack | Scanner folder | Typical paths |
| --- | --- | --- |
| Python (Flask, Django, FastAPI) | `scanners/python/` | `src/`, `server/`, `app/` |
| Java (Spring, Jakarta EE, JDBC) | `scanners/java/` | `src/main/java/`, `server/` |
| Node.js / Express / Nest | `scanners/javascript/` | `server/`, `packages/*/src/` |
| Browser / React / Vue / Angular | `scanners/javascript/` | `client/`, `src/` |

---

## Rule map (OWASP themes)

| Prefix | Theme | Rule files |
| --- | --- | --- |
| **if** | Injection — SQL | `no-sql-string-concatenation.md` |
| **if** | Injection — OS command | `no-os-command-injection.md` |
| **if** | Injection — XSS / script | `no-dangerous-xss-sinks.md`, `no-eval-dynamic-code-execution.md` |
| **if** | Injection — LDAP | `no-ldap-filter-injection.md` |
| **cf** | Cryptographic failures | `no-plaintext-password-storage.md`, `no-plaintext-sensitive-data-at-rest.md`, `no-weak-crypto-algorithms.md`, `no-hardcoded-secrets.md` |
| **af** | Authentication failures | `no-predictable-session-token.md`, `no-insufficient-login-rate-limiting.md`, `no-client-side-auth-trust.md`, `no-jwt-none-algorithm.md` |
| **df** | Integrity / supply chain | `no-unsafe-deserialization.md`, `no-mass-assignment-from-request.md`, `no-untrusted-component-sources.md`, `no-xxe-unsafe-xml-parser.md` |
| **id** | Insecure design | `no-unsafe-file-upload-handling.md`, `no-path-traversal-in-paths.md`, `no-excessive-response-data.md` |
| **ec** | Exceptional conditions | `no-sensitive-error-disclosure.md`, `no-toctou-outside-lock.md` |
| **lf** | Logging failures | `no-secrets-in-log-output.md`, `no-missing-security-event-logging.md` |

**24 rules · 72 scanners** (24 stems × 3 languages).

---

## Context corpus

Authoritative training material: **`secure-code-warrior`** repo `context/`. Regression fixtures under that repo's `fixtures/`. Use **`context/green_belt_assessment/`** challenges when extending rules.
