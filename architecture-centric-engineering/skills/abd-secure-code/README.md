---
catalogue_summary: "OWASP-aligned secure coding rules and Python, Java, and JavaScript scanners — write security-sensitive production code and prove it with mechanical checks before merge."
---

# abd-secure-code

## Overview

Packages Secure Code Warrior guidance into **24 checkable rules** and **72 language scanners** (Python, Java, JavaScript). Use alongside **abd-clean-code** during the GREEN phase or on security-focused slices (auth, persistence, file handling, crypto, rendered output).

Training corpus and regression fixtures remain in the sibling **`secure-code-warrior`** repository (`context/`, `fixtures/`). Configure `inputs/corpus-root.json` if your checkout path differs.

## How it fits together

```ascii
story / AC / failing test
           |
           v
  rules (OWASP themes) -----> secure production code
           |
           v
  scanners (py / java / js) -> scanner-report/abd-secure-code.md
           |
           v
  secure-code-review-checklist.md
```

## Source

- [SKILL.md](SKILL.md)
- Family: `architecture-centric-engineering` (deploy with `deploy-skills.ps1`)
- Corpus: `secure-code-warrior` repo (`inputs/corpus-root.json`)
