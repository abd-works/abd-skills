# Secure Code Warrior — context retrieval index

Evidence for **abd-secure-code** rules (**24 rules**, **72 scanners**). Category prefixes: `context/category-index.md`. Rules index: `inputs/rules-index.json`. Batch map: `inputs/batch-wiring.json`.

## Exercise challenges

| Prefix | Kept chunk | Source | Rule(s) |
| --- | --- | --- | --- |
| **if** | SQL injection prevention | `context/05-injection-flaws/context/sql-injection-prevention-cheat-sheet.md` | no-sql-string-concatenation |
| **if** | SQL injection exercise | `context/05-injection-flaws/exercises-challenges/sql-injection.md` | no-sql-string-concatenation |
| **if** | OS command injection | `context/05-injection-flaws/context/os-command-injection.md` | no-os-command-injection |
| **if** | OS command exercise | `context/05-injection-flaws/exercises-challenges/os-command-injection.md` | no-os-command-injection |
| **if** | XSS prevention | `context/05-injection-flaws/context/cross-site-scripting-prevention-cheat-sheet.md` | no-dangerous-xss-sinks, no-eval-dynamic-code-execution |
| **if** | XSS exercise | `context/05-injection-flaws/exercises-challenges/cross-site-scripting-xss.md` | no-dangerous-xss-sinks |
| **cf** | Password storage | `context/04-cryotiographic-failures/context/password-storage-cheat-sheet.md` | no-plaintext-password-storage |
| **cf** | Weak algorithms | `context/04-cryotiographic-failures/context/guildline-weak-algoithm-use.md` | no-weak-crypto-algorithms |
| **id** | Sensitive data exposure | `context/06-Insecure-Design/context/sensitive-data-exposure.md` | no-excessive-response-data |
| **cf** | Sensitive data storage exercise | `context/04-cryotiographic-failures/exercises-challenges/sensitive-data-storage-plain-text-storage-of-sensitive-info.md` | no-plaintext-sensitive-data-at-rest |
| **df** | Unsafe deserialization | `context/08_Software_or_Data_Integrity_Failures/context/deserialization-of-untrusted-data.md` | no-unsafe-deserialization |
| **df** | Mass assignment | `context/08_Software_or_Data_Integrity_Failures/context/mass-assignment.md` | no-mass-assignment-from-request |
| **df** | Mass assignment exercise | `context/08_Software_or_Data_Integrity_Failures/exercises-challenges/mass-assigment-challenge.md` | no-mass-assignment-from-request |
| **df** | Untrusted components exercise | `context/08_Software_or_Data_Integrity_Failures/exercises-challenges/Using-Components-From-Untrusted-Source.md` | no-untrusted-component-sources |
| **ec** | Error disclosure | `context/10_Mishandling_of_Exceptional_Conditions/context/error-details.md` | no-sensitive-error-disclosure |
| **ec** | Error exercise | `context/10_Mishandling_of_Exceptional_Conditions/exercises-challenges/error-details-exercise.md` | no-sensitive-error-disclosure |
| **af** | Improper authentication | `context/07_Authentication_Failures/context/improper-authentication.md` | no-predictable-session-token, no-client-side-auth-trust, no-jwt-none-algorithm |
| **af** | Insufficient anti-automation | `context/07_Authentication_Failures/context/insufficient-anti-automation.md` | no-insufficient-login-rate-limiting |
| **af** | Weak session token exercise | `context/07_Authentication_Failures/exercises-challenges/weak-session-token-generation.md` | no-predictable-session-token |
| **id** | Unrestricted file upload | `context/06-Insecure-Design/context/unrestricted-file-upload.md` | no-unsafe-file-upload-handling, no-path-traversal-in-paths |
| **id** | File upload exercise | `context/06-Insecure-Design/exercises-challenges/File-Upload-Vulnerability-Unrestricted-File-Upload.md` | no-unsafe-file-upload-handling |
| **lf** | Insufficient logging | `context/09_Logging_Alerting_Failures/context/insufficient-logging-and-monitoring.md` | no-secrets-in-log-output, no-missing-security-event-logging |
| **lf** | Insufficient logging exercise | `context/09_Logging_Alerting_Failures/exercises-challenges/insufficient-logging-and-monitoring-challenge.md` | no-secrets-in-log-output, no-missing-security-event-logging |

## Green belt batch `e0523` (wired)

| Ch | Prefix | Title | Rule(s) | Fixture |
| --- | --- | --- | --- | --- |
| 1 | **ec** | Error details | no-sensitive-error-disclosure | `fixtures/green-belt/e0523/challenge-01/` |
| 2 | **id** | Unrestricted file upload | no-unsafe-file-upload-handling, no-path-traversal-in-paths | `challenge-02/` |
| 3 | **af** | Insufficient anti-automation | no-insufficient-login-rate-limiting | `challenge-03/` |
| 4 | **df** | Mass assignment | no-mass-assignment-from-request | `challenge-04/` |
| 5 | **if** | Stored XSS | no-dangerous-xss-sinks | `challenge-05/` |
| 6 | **cf** | Weak crypto | no-weak-crypto-algorithms | `challenge-06/` |
| 7 | **df** | Untrusted components | no-untrusted-component-sources, no-xxe-unsafe-xml-parser | `challenge-07/` |
| 8 | **cf** | Plaintext passwords | no-plaintext-password-storage | `challenge-08/` |
| 9 | **if** | SQL + LDAP injection | no-sql-string-concatenation, no-ldap-filter-injection | `challenge-09/` |
| 10 | **ec** | Race conditions | no-toctou-outside-lock | `challenge-10/` |

**Validate wiring:** `python skills/abd-secure-code/scripts/validate_batch_wiring.py`
