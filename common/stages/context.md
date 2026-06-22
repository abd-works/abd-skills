# Context

**Pull:** Before any delivery stage — prepare and query workspace memory so agents have retrieval-ready context.
**Follow-on:** [shaping.md](shaping.md)

## Purpose

Build and maintain **retrieval-ready workspace memory** — convert source material, chunk it for retrieval, embed it, and search it. Context skills run before and alongside every stage; they are not a one-time step.

## Outcomes

- source material indexed
- semantic search available
- workspace memory current

## Team role

**All roles** — any agent or practitioner who needs to retrieve context before running a skill.

## Practice skills

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Context to Memory** | `abd-convert-to-markdown` | Any | Convert PDF, DOCX, PPTX source files to Markdown |
| 2 | **Context to Memory** | `abd-chunk-markdown` | Any | Split converted Markdown into retrieval-sized chunks |
| 3 | **Context to Memory** | `abd-embed-vectors` | Any | Embed chunks into a local FAISS vector store |
| 4 | **Context to Memory** | `abd-search-memory` | Any | Semantic search over embedded chunks |
| 5 | **Context to Memory** | `abd-semantic-context-chunker` | Any | Index scattered source content by the kind of question it answers |

## Entry conditions

- Source material exists (documents, code, notes, prior artifacts).

## Expected outputs

- Indexed memory store ready for `search_memory` calls by any skill.

## Exit gate

1. `search_memory "<query>"` returns relevant chunks from source material.
2. Workspace memory is current with latest source changes.
