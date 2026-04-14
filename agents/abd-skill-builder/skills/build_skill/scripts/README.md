# build_skill script

**New skill package** (template + `library/base` + `scripts/base` from this repo):

```bash
# from abd-skill-builder repo root
python skills/build_skill/scripts/build_skill.py --name my-skill --out ../my-skill
```

**Merge `AGENTS.md` / validation** — run at **repo root** (no wrapper here):

```bash
python scripts/base/build.py
```

**Optional — any skill root** (pass **`--skill-root`**; default is cwd):

```bash
python skills/build_skill/scripts/set_workspace.py --skill-root /path/to/skill [<path>]
python skills/build_skill/scripts/check_skill_layout.py --skill-root /path/to/skill
python skills/build_skill/scripts/build_pipeline_plan.py --skill-root /path/to/skill
```

Targets that use **`set_workspace`** / **`build_pipeline_plan`** must ship **`scripts/base/`** (vendored from this repo). **`check_skill_layout`** only needs **`SKILL.md`** (and optionally **`skill-config.json`**, **`content/parts/`**, **`rules/`**).
