# Scanners — abd-secure-code (enterprise)

## Architecture

```text
scanners/
  common/
    pattern_catalog.py      # Single source of truth — all regex patterns by rule + language
    scan_utils.py             # Violation builder, skip logic, context-window gating
    catalog_scanner.py        # Special handlers (plaintext password, safe yaml)
    generate_scanners.py      # Regenerate language entrypoints after catalog edits
  python/
    code_scanner.py           # Base + AST helpers
    no_*_scanner.py           # Thin wrappers (SQL adds AST pass)
  java/
    java_code_scanner.py
    no_*_scanner.py
  javascript/
    js_code_scanner.py        # Node.js + browser / React / Vue / Angular
    no_*_scanner.py
```

**After editing `pattern_catalog.py`:** scanners pick up changes at runtime — no regen required unless entrypoint structure changes. Run `python scanners/common/generate_scanners.py` when adding a new rule stem.

## Running

```bash
python run_scanners.py \
  --skill-root .cursor/skills/abd-secure-code \
  --workspace /path/to/project \
  --language python   # repeat for java, javascript
```

## Rules covered (19)

| Rule stem | CWE / OWASP |
| --- | --- |
| no-sql-string-concatenation | CWE-89, A03 |
| no-os-command-injection | CWE-78, A03 |
| no-eval-dynamic-code-execution | CWE-94, A03 |
| no-dangerous-xss-sinks | CWE-79, A03 |
| no-ldap-filter-injection | CWE-90, A03 |
| no-plaintext-password-storage | CWE-256, A02 |
| no-weak-crypto-algorithms | CWE-327, A02 |
| no-hardcoded-secrets | CWE-798, A02 |
| no-predictable-session-token | CWE-330, A07 |
| no-insufficient-login-rate-limiting | CWE-307, A07 |
| no-unsafe-deserialization | CWE-502, A08 |
| no-mass-assignment-from-request | CWE-915, A08 |
| no-untrusted-component-sources | CWE-829, A06 |
| no-unsafe-file-upload-handling | CWE-434, A04 |
| no-path-traversal-in-paths | CWE-22, A01 |
| no-sensitive-error-disclosure | CWE-209, A05 |
| no-xxe-unsafe-xml-parser | CWE-611, A05 |
| no-secrets-in-log-output | CWE-532, A09 |
| no-toctou-outside-lock | CWE-367, concurrency |

## Batch wiring

Green belt (`e0523`) and exercise challenges map to rules in `inputs/batch-wiring.json`. Per-challenge fixtures: `fixtures/green-belt/e0523/challenge-NN/`. Validate with `scripts/validate_batch_wiring.py`.

## Regression fixtures

- `fixtures/insecure-sample/src/` — expect failures on applicable rules
- `fixtures/secure-sample/src/` — clean baseline; expect zero violations
- `fixtures/green-belt/e0523/challenge-NN/src/` — one vulnerability class per green belt challenge

## Limitations

Heuristic pattern/AST checks complement SAST/DAST — they do not replace dependency CVE scanning, penetration testing, CSP/TLS configuration review, or rate limiting design. Context-gated patterns (e.g. `Math.random` only near token/session keywords) reduce false positives but require human review at boundaries.
