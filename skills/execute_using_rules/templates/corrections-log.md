# Corrections log — structure

**Canonical spec:** The field table and snippets below are the **single** definition for corrections — [**SKILL.md**](../SKILL.md) **What you can do → item 4** links here instead of duplicating the table.

**Purpose:** During review, **do not edit skill sources** until the **correct output** is confirmed. Record each problem here first; complete **item 4 — fix the output** before **item 4 — fix the skill**. Full narrative: [**SKILL.md**](../SKILL.md) item 4.

---

## Where to create the file

- Under **`active_skill_workspace`** from **`skill-config.json` → `workspace`** (engagement / project tree).
- **Not** inside the skill install directory.

**Example paths** (pick one convention per engagement):

- `docs/corrections-log.md`
- `.skill-builder/corrections-log.md`

---

## One entry per problem — fields

| Field | Content |
| --- | --- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **DO / DO NOT** | The rule as it should be stated |
| **Example (wrong)** | What the output actually did |
| **Example (correct)** | What it should have done — fill **only after** the right output is confirmed |
| **Scanner or validator** | If applicable: **`scanner:`** in rule frontmatter, **`scanners/...-scanner.py`**, or host **`build.build_pipeline`** step |
| **Likely source** | One of: `prompt gap` · `rule not read` · `edge case` · `automation gap` |

**Duplicate violations:** If the **same guidance** was violated again, add another **Example (wrong)** under the **same entry** instead of opening a new entry.

---

## Markdown shape (whole file)

Use a heading per entry; keep a **Status** line so you know if the **output** phase (item 4) is done for that entry.

```markdown
# Corrections log

Engagement: <name or path>
Skill / phase: <what was being reviewed>

---

## Entry: <short label>

- **Status:** open | confirmed
- **Rule:** `rules/<stem>.md` or rule id
- **DO / DO NOT:** <plain statement>
- **Example (wrong):**
  <what the model or artifact did>
- **Example (correct):**
  <leave blank until confirmed; then fill>
- **Scanner or validator:** <e.g. `scanners/foo-scanner.py` or `build.build_pipeline[1]`>
- **Likely source:** prompt gap | rule not read | edge case | automation gap

---

## Entry: <next problem>

...
```

---

## Single entry — copy-paste snippet

```markdown
## Entry: <label>

- **Status:** open
- **Rule:**
- **DO / DO NOT:**
- **Example (wrong):**
- **Example (correct):**
- **Scanner or validator:**
- **Likely source:**

```

When the regenerated output is right: set **Status** to **confirmed**, fill **Example (correct)**, then you may promote fixes in **item 4 — fix the skill** (sources + **`bundle_rules_into_skill_md.py`** / full validation).

---

## Wrong vs right (process)

| Wrong | Right |
| --- | --- |
| Log a problem and **immediately** edit **skill sources** or **`rules/`** before output is validated | Log → re-generate → iterate on **output** until correct → then fill **Example (correct)** |
| Patch **Bundled rules** or **`AGENTS.md`** to “pass” review | Edit **`rules/`** (and other sources as needed), run **`bundle_rules_into_skill_md.py`**; use the target repo’s own merge only if it maintains **`AGENTS.md`** / **`built/`** |
