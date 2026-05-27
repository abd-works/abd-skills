# Skill builder package

Practice skills for authoring ABD practice packages: query hub sources, author SKILL.md + rules, build scanners, maintain the AI Garden catalog, and publish HTML manuals.

**Orchestrator:** `agents/abd-practice-skill-builder/` (AGENTS.md pipeline).

## Deploy

```bash
python scripts/deploy_family_package.py --package skill-builder --to <workspace>
```

Or deploy all families:

```powershell
& scripts/deploy-skills.ps1 -Force
```
