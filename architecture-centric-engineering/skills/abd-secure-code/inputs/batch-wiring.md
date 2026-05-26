# Batch wiring — abd-secure-code

Authoritative map: [`batch-wiring.json`](batch-wiring.json). Validate with `scripts/validate_batch_wiring.py`.

## Green belt `e0523` (10 challenges → rules → fixtures)

| Ch | Topic | Rule(s) | Fixture |
| --- | --- | --- | --- |
| 1 | Error details | no-sensitive-error-disclosure | `fixtures/green-belt/e0523/challenge-01/` |
| 2 | File upload | no-unsafe-file-upload-handling, no-path-traversal-in-paths | `challenge-02/` |
| 3 | Anti-automation | no-insufficient-login-rate-limiting | `challenge-03/` |
| 4 | Mass assignment | no-mass-assignment-from-request | `challenge-04/` |
| 5 | Stored XSS | no-dangerous-xss-sinks | `challenge-05/` |
| 6 | Weak crypto | no-weak-crypto-algorithms | `challenge-06/` |
| 7 | Untrusted components | no-untrusted-component-sources | `challenge-07/` |
| 8 | Plaintext passwords | no-plaintext-password-storage | `challenge-08/` |
| 9 | SQL + LDAP | no-sql-string-concatenation, no-ldap-filter-injection | `challenge-09/` |
| 10 | Race / TOCTOU | no-toctou-outside-lock | `challenge-10/` |

## Other batches

- **`practice_run/`** and **`new_run/`** — same 10-challenge topic map; markdown templates only until content is filled. Wiring inherits from `e0523`.
- **Exercise challenges** — nine OWASP exercise files under `context/` mapped in `batch-wiring.json` → `exercise_batches`.

## New rules (from e0523 gaps)

| Rule | Batch source |
| --- | --- |
| no-ldap-filter-injection | e0523 ch9 |
| no-xxe-unsafe-xml-parser | e0523 ch7 (XML hardening) |
| no-untrusted-component-sources | e0523 ch7, exercise |
| no-insufficient-login-rate-limiting | e0523 ch3 |
| no-toctou-outside-lock | e0523 ch10 |

**Totals:** 19 rules · 57 scanners (Python, Java, JavaScript)
