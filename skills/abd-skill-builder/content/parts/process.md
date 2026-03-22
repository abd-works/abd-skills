# Process — abd-skill-builder

**Pipeline:** Standards + authoring checklist → **Scaffold or migrate** → Pass Operator

| # | Phase | Actor | Ref |
|---|--------|-------|-----|
| 1 | Read standards & work **[authoring checklist](library/authoring-checklist.md)** (ask / AI-suggest / track) | Human / AI | [index](library/skill-repo-standards.md), [full §3](library/skill-standards-section-3.md) |
| 2a | **Scaffold** new skill directory | Code | [scaffold](phases/scaffold.md) |
| 2b | **Or migrate** existing skill — delta report, user picks fixes | Human / AI | **[migrate to standards](phases/migrate.md)** |
| 3 | Run Operator (`compileall`, `build.py`, scanners) | Code | (agentic-skill-builder `operator`) |
