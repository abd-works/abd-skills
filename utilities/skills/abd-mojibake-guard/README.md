# abd-mojibake-guard

Scan and fix UTF-8 mojibake after doc creation and before commit.

## Overview

Wraps abd-skills encoding scripts: `scan_encoding.py` for scan/fix, `deploy-mojibake-guard.sh` for CI and pre-commit installation. Agents run **scan → fix → check-staged** around document work and commits.

## How it fits together

```
doc create / bulk edit  →  scan  →  fix (if needed)  →  scan again
                              ↓
                         before commit  →  check-staged
                              ↓
                    optional: install-guard (CI + hook)
```
