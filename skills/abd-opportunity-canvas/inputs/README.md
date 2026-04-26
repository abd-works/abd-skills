# inputs/

**`abd-answers-retrieval.md`** — evidence log for **authoring and revising** this practice package, filled with **abd-query-practice-sources** (see `agilebydesign-skills/agents/abd-practice-skill-builder/skills/abd-query-practice-sources/SKILL.md`). Each retained excerpt needs a verbatim body, source, **Relevance** (`rule` | `core_concept` | `example` | `procedure` | `glossary` | `diagram_ref` | `other`), **Query**, and **Rank**.

Template starter: `agents/abd-practice-skill-builder/skills/abd-query-practice-sources/templates/abd-answers-retrieval-input.md`

**Practitioners running an opportunity canvas** do not need this folder.

---

## Refreshing `abd-answers-retrieval.md` (package maintainers)

From the **abd-answers** repo root, after reading **abd-query-practice-sources**:

```bash
npm run rag:query -- "<query>" --k 8
```

Raise **`--k`** if results are thin. Record each excerpt you keep with metadata as that skill specifies.

- **Full index (no folder filter):** omit **`--folders`**.
- **Agile Practices tree in Pinecone:** `--folders "01 Agile Practices"` (this matches **`memoryFolder`** for that embed; see **abd-answers** `scripts/embed-agile-practices-pinecone.ts`). Do **not** use `data/assets/01 Agile Practices` as **`--folders`** — that is the source-asset path on disk, not the indexed folder string.
- **Pinecone 429:** retry after quota reset, or copy verbatim from **abd-answers** pipeline markdown for the same source files.

Orchestration: `agilebydesign-skills/agents/abd-practice-skill-builder/AGENTS.md` (retrieve → author stages).
