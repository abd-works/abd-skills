# Rule: Hub retrieval discipline

**Scanner:** Manual review

## DO

- **Log what you keep** — If you would quote or paraphrase the hub in a rule, that text appears under **`### Kept chunk N`** in **`inputs/abd-answers-retrieval.md`** as a **verbatim** fenced body (full pipeline markdown when available), not only a summary table cell — so authoring does not need a **second** query.
- **Dedupe** — Same chunk hit twice → one **Kept chunk** (same **Source location** / slide body).
- **Tag honestly** — **Relevance** reflects how you will **use** the chunk (rule vs example vs diagram_ref), not a generic **`other`** to skip thinking.

## DO NOT

- **Invent hub claims** with no matching **Kept chunk** (verbatim body) in the retrieval log.
- **Design a chunking strategy** for the hub in this step; only **query** and **record**.
- **Author the target practice package** in this step — no **`rules/*.md`**, **`SKILL.md`**, **`templates/`**, or **`bundle_rules_into_skill_md.py`** on the target. **`Relevance: rule`** means the chunk will back a rule **later** in **abd-author-practice-skill**, not "create **rules/** now."

**Source:** Practice-skill builder convention (abd-query-practice-sources).
