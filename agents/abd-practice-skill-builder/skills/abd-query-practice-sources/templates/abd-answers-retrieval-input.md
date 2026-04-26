<!--
  Canonical RAG input for the target practice skill.
  Path: skills/<skill-name>/inputs/abd-answers-retrieval.md
  Written by: abd-query-practice-sources (after npm run rag:query in abd-answers).
  Shape and required fields: read agents/abd-practice-skill-builder/skills/abd-query-practice-sources/SKILL.md (Output log).
-->

# abd-answers retrieval input — {{skill_name}}

## Kept chunks (verbatim)

### Kept chunk 1

- **Chunk title:** {{title from hit}}
- **Similarity:** {{from vector search if present}}
- **Relevance:** {{rule, core_concept, example, procedure, glossary, diagram_ref, or other}}
- **Relevance note:** {{short}}
- **Query:** {{query string}}
- **Rank in result set:** {{1-based}}

```
{{verbatim body; full pipeline markdown for the slide when available}}
```

## Optional: machine trail

```json
{{paste raw npm run rag:query JSON if desired}}
```
