---
scanner: no_hardcoded_secrets_scanner.py
category: cf
---

# Rule: No hardcoded secrets

Secrets, API keys, private keys, connection strings, and long-lived tokens must not live in source control. Configuration belongs in environment variables, a secret manager (Vault, AWS Secrets Manager, Azure Key Vault), or runtime injection — never as string literals in application code (CWE-798, OWASP A02).

## DO

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

## DO NOT

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
