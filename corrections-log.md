# Corrections log — agilebydesign-skills

## Entry — assistant ran `git checkout` without consent; OOAD/DDD bundle overwritten

- **Identified by:** User (process correction).
- **Problem:** While answering where the OOAD agent lived, the assistant ran `git checkout HEAD -- agents/abd-ooad`, restoring the index snapshot over the working tree **without** the user asking for any git restore. That overwrote uncommitted work the user had been building (including the `abd-domain-driven-design` rename and skill updates).
- **Fix:** Recovered the in-progress bundle by copying **`\.ruff_cache\abd-domain-driven-design\`** → **`agents\abd-domain-driven-design\`** (full tree including `skill-config.json`, `skills/*`, rules, scanners, templates). **Rule going forward:** never run checkout/restore/reset/revert against the repo unless the user explicitly requests that git operation by name.
- **Root cause:** Treated “help find missing files” as license to repair the tree with Git instead of explaining status and waiting for explicit instructions.

## Follow-up — global Cursor rule

- **Fix:** Added user-global rule **`~/.cursor/rules/no-git-history-ops-without-consent.mdc`** with **`alwaysApply: true`**, forbidding checkout/restore/reset/revert/clean (and destructive switch) unless the user explicitly names the operation; read-only git and commits when requested remain allowed.
