# Secure code review checklist

Use after implementing or reviewing a change. Mark each row **pass**, **fail**, or **n/a** with a one-line note.

| OWASP | Rule | Pass / Fail | Notes |
| --- | --- | --- | --- |
| A03 Injection | No SQL string concatenation | | |
| A03 Injection | No OS command injection | | |
| A03 Injection | No eval / dynamic code execution | | |
| A03 Injection | No dangerous XSS sinks | | |
| A03 Injection | No LDAP filter injection | | |
| A02 Cryptographic failures | No plaintext password storage | | |
| A02 Cryptographic failures | No plaintext sensitive data at rest | | |
| A02 Cryptographic failures | No weak crypto algorithms | | |
| A02 Cryptographic failures | No hardcoded secrets | | |
| A07 Authentication failures | No predictable session token | | |
| A07 Authentication failures | No insufficient login rate limiting | | |
| A07 Authentication failures | No client-side auth trust | | |
| A07 Authentication failures | No JWT none algorithm | | |
| A08 Integrity | No unsafe deserialization | | |
| A08 Integrity | No mass assignment from request | | |
| A06 Supply chain | No untrusted component sources | | |
| A04 Insecure design | No unsafe file upload handling | | |
| A01 Broken access control | No path traversal in paths | | |
| A04 Insecure design | No excessive response data | | |
| A05 Misconfiguration | No sensitive error disclosure | | |
| A05 Misconfiguration | No XXE in unsafe XML parser | | |
| A09 Logging failures | No secrets in log output | | |
| A09 Logging failures | No missing security event logging | | |
| Concurrency | No TOCTOU outside lock | | |

## Scanner commands

Run **each language** present in the engagement workspace:

```powershell
$runner = "<engagement>/.cursor/skills/execute-skill-using-skills-rules/scripts/run_scanners.py"
$skill  = "<engagement>/.cursor/skills/abd-secure-code"
$ws     = "<engagement-root>"

python $runner --skill-root $skill --workspace $ws --language python
python $runner --skill-root $skill --workspace $ws --language java
python $runner --skill-root $skill --workspace $ws --language javascript
```

Report: `<workspace>/scanner-report/abd-secure-code.md`

## Batch wiring

Green belt and exercise challenges map to rules in `inputs/batch-wiring.json`. Corpus paths resolve via `inputs/corpus-root.json` (default: sibling `secure-code-warrior` repo). Validate:

```powershell
python architecture-centric-engineering/skills/abd-secure-code/scripts/validate_batch_wiring.py
```

---

## Example (filled — Pet registration API review)

| OWASP | Rule | Pass / Fail | Notes |
| --- | --- | --- | --- |
| A03 Injection | No SQL string concatenation | pass | All queries use `$1` bindings in `user.repository.ts` |
| A03 Injection | No OS command injection | n/a | No shell invocation in this slice |
| A03 Injection | No eval / dynamic code execution | pass | No dynamic code paths |
| A03 Injection | No dangerous XSS sinks | pass | React default escaping; no `dangerouslySetInnerHTML` |
| A03 Injection | No LDAP filter injection | n/a | No LDAP in slice |
| A02 Cryptographic failures | No plaintext password storage | pass | Argon2id via `hashPassword()` before insert |
| A02 Cryptographic failures | No weak crypto algorithms | pass | No MD5/SHA1 for passwords |
| A02 Cryptographic failures | No hardcoded secrets | pass | Stripe key from `process.env` |
| A07 Authentication failures | No predictable session token | pass | express-session CSPRNG id |
| A07 Authentication failures | No insufficient login rate limiting | pass | `loginRateLimiter` on POST `/login` |
| A08 Integrity | No unsafe deserialization | pass | JSON + Zod only |
| A08 Integrity | No mass assignment from request | fail → fixed | Was `User.create(req.body)`; now `registrationSchema.parse` |
| A06 Supply chain | No untrusted component sources | pass | Lockfile + `npm ci` only |
| A04 Insecure design | No unsafe file upload handling | n/a | No uploads in slice |
| A01 Broken access control | No path traversal in paths | n/a | No filesystem paths from user input |
| A05 Misconfiguration | No sensitive error disclosure | pass | 500 returns generic message + `requestId` |
| A05 Misconfiguration | No XXE in unsafe XML parser | n/a | No XML parsing |
| A09 Logging failures | No secrets in log output | pass | Login logs omit password field |
| Concurrency | No TOCTOU outside lock | n/a | No shared balance updates |

**Reviewer:** Alex · **Date:** 2026-05-25 · **Scope:** POST `/api/register`
