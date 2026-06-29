# Context

**Pull:** Before any delivery stage — prepare and query workspace memory so agents have retrieval-ready context.
**Follow-on:** [shaping.md](shaping.md)

## Purpose

Build and maintain **retrieval-ready workspace memory** — convert source material, chunk it for retrieval, embed it, and search it. Optionally extract context from running applications and sandbox external dependencies for isolated exploration. Context skills run before and alongside every stage; they are not a one-time step.

## Outcomes

- source material indexed
- semantic search available
- workspace memory current
- running applications extractable (when applicable)

## Team role

**All roles** — any agent or practitioner who needs to retrieve context before running a skill.

## Practice skills

| Order | Skill | Role | Notes |
| --- | --- | --- | --- |
| 1 | `abd-context-to-markdown` | Any | Convert PDF, DOCX, PPTX source files to Markdown |
| 2 | `abd-context-chunk` | Any | Split converted Markdown into retrieval-sized chunks |
| 3 | `abd-context-db-embed` | Any | Embed chunks into a local FAISS vector store |
| 4 | `abd-context-db-ask` | Any | Semantic search over embedded chunks |
| 5 | `abd-context-semantic-index` | Any | Index scattered source content by the kind of question it answers |
| 6 | `abd-context-app-sandbox` | Any | Stub external dependencies so an application can run in isolation |
| 7 | `abd-context-app-extractor` | Any | Extract context (screens, routes, structure) from a running application |

## Entry conditions

- Source material exists (documents, code, notes, prior artifacts).

## Expected outputs

- Indexed memory store ready for `search_memory` calls by any skill.

## Exit gate

1. `search_memory "<query>"` returns relevant chunks from source material.
2. Workspace memory is current with latest source changes.
