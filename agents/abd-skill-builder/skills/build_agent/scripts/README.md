# build_agent scripts

- **`new_agent.py`** — creates `--out/<name>/` with `content/*.md` stubs, `skill-config.json`, and `scripts/build.py` (multi-skill agent pattern).

```bash
python skills/build_agent/scripts/new_agent.py --name my-agent --out C:\tmp\agents
# creates C:\tmp\agents\my-agent\...
```
