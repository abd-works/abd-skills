# Migrated to plugin — notes

Reference for turning ABD family packages into installable plugins (Cursor Marketplace, Open Plugin Spec, `npx skills`).

---

## Terminology in this repo

| Term here | Meaning |
| --- | --- |
| **Family package / plugin** | Repo-root folder (`delivery/`, `story-driven-delivery/`, …) deployed via `deploy_family_package.py` |
| **Cursor plugin** | Directory with `.cursor-plugin/plugin.json` — Marketplace / one-step install |
| **Open Plugin Spec** | Vendor-neutral `.plugin/plugin.json` ([vercel-labs/open-plugin-spec](https://github.com/vercel-labs/open-plugin-spec)) |
| **Stage spec** | `delivery/content/stages/*.md` — which practice skills run in which delivery stage |

**OpenAI ChatGPT plugins are deprecated.** Old `.well-known/ai-plugin.json` + OpenAPI is not the target. Use Cursor plugins, Open Plugin Spec, or GPT Actions instead.

---

## What “true plugin” means online (2026)

| Platform | Manifest | Bundle |
| --- | --- | --- |
| [Cursor Marketplace](https://cursor.com/docs/reference/plugins) | `<plugin>/.cursor-plugin/plugin.json` | skills, **rules**, agents, **commands**, hooks, MCP |
| [Open Plugin Spec v1.0.0](https://github.com/vercel-labs/open-plugin-spec) | `.plugin/plugin.json` | skills, MCP (core); rules, agents, commands, hooks (optional) |
| [`npx skills`](https://github.com/vercel-labs/skills) | optional `.claude-plugin/marketplace.json` | discovers individual `SKILL.md` unless manifest declares a bundle |

Cursor layout (native):

```text
my-plugin/
├── .cursor-plugin/
│   └── plugin.json
├── rules/          # .mdc
├── skills/         # */SKILL.md
├── agents/
├── commands/
├── hooks/hooks.json
└── mcp.json
```

Open Plugin minimal layout:

```text
hello-plugin/
├── .plugin/
│   └── plugin.json
└── skills/
    └── greet/
        └── SKILL.md
```

---

## Does Open Plugin Spec work in VS Code and Cursor?

**The spec is cross-tool; each editor must implement it.** Not one folder guaranteed everywhere today.

### Cursor

- Native format: **`.cursor-plugin/plugin.json`**
- Docs: [Plugins reference](https://cursor.com/docs/reference/plugins)
- Open Plugin says hosts with a vendor manifest should prefer it but **must also** read `.plugin/plugin.json` — Cursor’s full Open Plugin v1 fallback is not clearly documented
- **Safest for Cursor:** ship `.cursor-plugin/plugin.json`

### VS Code

- Different system today: extensions + Copilot chat instructions (`package.json`, `.github/` instructions)
- Open Plugin support was discussed for VS Code **April 2026** release (RFC on open-plugin-spec repo) — rolling out, not identical to Cursor
- This repo already deploys to VS Code via `deploy_family_package.py --ide vscode` → `.github/`

### What works in both today

| Piece | Cursor | VS Code |
| --- | --- | --- |
| Open Plugin bundle (`.plugin/plugin.json`) | Uncertain — use `.cursor-plugin/` | Incoming / different packaging |
| Individual `SKILL.md` | Yes (`.cursor/skills/`) | Yes (`npx skills`, agent skill paths) |
| **Family deploy** (`deploy_family_package.py`) | Yes → `.cursor/` | Yes → `.github/` |
| Rules/commands as plugin bundle | Cursor plugins | `.instructions.md` / prompts via deploy |

**Practical strategy**

1. Keep `deploy_family_package.py` for engagement workspaces (Cursor + VS Code).
2. Add **`.cursor-plugin/plugin.json`** per family for Cursor Marketplace.
3. Optionally add **`.plugin/plugin.json`** for future Open Plugin hosts.
4. Treat **skills** as the portable core; rules, commands, hooks may need per-host wiring.

---

## Standard family package layout (today)

From `scripts/normalize_family_packages.py` and `scripts/deploy_family_package.py`:

```text
<family>/
├── agents/
├── skills/
├── content/
├── instructions/    # .mdc / .instructions.md → .cursor/rules or .github/
├── prompts/         # .prompt.md → .cursor/commands
├── lib/
├── scripts/
└── README.md
```

Deploy:

```powershell
python scripts/deploy_family_package.py --package <family> --to <workspace>
# or
& scripts/deploy-skills.ps1 -Force
```

Cursor vs VS Code mapping:

| Family slot | Cursor deploy | VS Code deploy |
| --- | --- | --- |
| `instructions/` | `.cursor/rules/` | `.github/*.instructions.md` |
| `prompts/` | `.cursor/commands/` | `.github/prompts/` |
| `skills/` | `.cursor/skills/` | (skills path per agent) |
| `content/` | `.cursor/content/` | `.github/content/` |

---

## Gap: internal packages vs Marketplace plugins

Families are **deploy packages**, not yet **Cursor Marketplace plugins**.

| Requirement | Families today |
| --- | --- |
| `.cursor-plugin/plugin.json` | Missing on all families |
| Root `.cursor-plugin/marketplace.json` | Missing |
| `rules/` folder name | Uses `instructions/` (same content, different name for Cursor auto-discovery) |
| `commands/` folder name | Uses `prompts/` |
| `hooks/hooks.json` | Missing |
| `mcp.json` | Missing (optional) |
| `npx skills` **bundle** install | Per-skill only (`npx skills add agilebydesign/agilebydesign-skills@<name>`) |

---

## Per-family snapshot (five practice + delivery + skill-builder)

| Package | Skills / agents | Thin spots for plugin packaging |
| --- | --- | --- |
| **delivery** | 3 agents, 4 skills, some instructions + prompts | No manifest, no hooks |
| **story-driven-delivery** | 8 skills, 2 `.mdc` instructions | No agents, no prompts, minimal README |
| **user-experience-design** | 3 skills | Empty `instructions/` and `prompts/`, no skill READMEs |
| **architecture-centric-engineering** | 9 skills, 4 instruction files | No prompts; not all skills have package-level rules |
| **skill-builder** | 1 agent, 5 skills, author instructions | Meta tooling; no prompts/hooks |

**Practice skill content** for delivery stages is largely done — see `delivery/content/stages/*.md`. Remaining work is **packaging**, not missing SKILL.md for stage tables.

---

## Checklist: migrate one family to Cursor plugin

1. Add `<family>/.cursor-plugin/plugin.json`:

   ```json
   {
     "name": "story-driven-delivery",
     "version": "1.0.0",
     "description": "Story mapping through ATDD and diagram sync.",
     "author": { "name": "abd.works" },
     "skills": "./skills",
     "rules": "./instructions",
     "commands": "./prompts",
     "agents": "./agents"
   }
   ```

2. Add repo root `.cursor-plugin/marketplace.json` listing all families (see [cursor/plugins](https://github.com/cursor/plugins)).

3. Add optional `.plugin/plugin.json` (copy or symlink manifest fields) for Open Plugin portability.

4. Add `hooks/hooks.json` where automation helps (e.g. story-graph change → drawio render).

5. Expand family `README.md` (usage, config, test steps).

6. Test local plugin load; submit via [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish).

7. Keep `deploy_family_package.py` — plugin layout can mirror the same source tree or be generated in CI.

---

## Optional: `npx skills` marketplace manifest

For bundle discovery by the skills CLI:

```json
{
  "metadata": { "pluginRoot": "./" },
  "plugins": [
    {
      "name": "story-driven-delivery",
      "source": "story-driven-delivery",
      "skills": ["./story-driven-delivery/skills/*"]
    }
  ]
}
```

Place at `.claude-plugin/marketplace.json` or per skills CLI docs. Individual skills already install with:

```bash
npx skills add agilebydesign/agilebydesign-skills@abd-story-mapping -y
```

---

## Related files in this repo

- `scripts/deploy_family_package.py` — deploy to engagement workspace
- `scripts/normalize_family_packages.py` — standard slot layout
- `skill-builder/skills/abd-skill-catalog/scripts/family_catalog.py` — plugin slot discovery for AI Garden catalog
- `skill-builder/skills/abd-skill-catalog/scripts/kanban_layout.py` — stage × plugin kanban from `delivery/content/stages/`
- `delivery/content/stages/README.md` — stage index and ripple rules
- `skills.sh` — publish skills to agentskillhub.dev index

---

## Links

- [Cursor Plugins reference](https://cursor.com/docs/reference/plugins)
- [Cursor Marketplace publish](https://cursor.com/marketplace/publish)
- [Open Plugin Spec](https://github.com/vercel-labs/open-plugin-spec)
- [vercel-labs/skills CLI](https://github.com/vercel-labs/skills)
- [Open Plugin feature comparison (gist)](https://gist.github.com/johnlindquist/217aaa5023879dfa9bc654c7ad0260)
