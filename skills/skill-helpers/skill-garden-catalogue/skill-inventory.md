# Skill Garden — Inventory

> Auto-generated catalogue of **43** deployed skills.
> Re-run `generate_catalogue.py` to refresh.

## Context To Memory

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-chunk-markdown](context-to-memory/abd-chunk-markdown/) | Chunk Markdown | Split converted Markdown into retrieval-sized chunks with evidence labels, guided by a structure-based chunking spec. Use when the user wants to "chunk documents", "split for RAG", "draft a chunking … |
| [abd-convert-to-markdown](context-to-memory/abd-convert-to-markdown/) | Convert to Markdown | Convert office documents (PDF, PPTX, DOCX, XLSX, etc.) to navigable Markdown with real headings, sections, and tables. Use when the user wants to convert a document or folder of documents to … |
| [abd-embed-vectors](context-to-memory/abd-embed-vectors/) | Embed Vectors | Embed text chunks into a local FAISS vector index for semantic search. Use when the user wants to "embed chunks", "build a vector index", "create embeddings", or prepare chunked content for RAG … |
| [abd-search-memory](context-to-memory/abd-search-memory/) | Search Memory | Semantic search over a local FAISS vector index built from document chunks. Use when the user says "use memory", "search memory", "what does memory say", "from our content", "what do we have on … |

## Delivery

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-delivery-planning](delivery/abd-delivery-planning/) | You want to build, present, or revise a delivery plan after reading context. | Delivery plans only: context, risks, strategies, staged runs and checkpoints (not stories, tests, or code). |
| [abd-delivery-war-room](delivery/abd-delivery-war-room/) | Reduce repeated paste handoffs between orchestrator and team-member threads by keeping state on disk under the engagement root. | Experimental file-based war room for handoffs between  and :  under the engagement workspace with , , and  / . Not wired into the delivery-lead or team-member agents until re-integrated from first … |

## Domain Driven Design

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-domain-language](domain-driven-design/abd-domain-language/) | Build a shared, rigorous vocabulary for each module â€” the terms, behaviors, and rules that domain experts and modelers agree on â€” so that every conversation, document, and downstream artifact … | Build a shared, rigorous vocabulary for each module â€” the terms, behaviors, and rules that domain experts and modelers agree on â€” so that every conversation, document, and downstream artifact … |
| [abd-module-partition](domain-driven-design/abd-module-partition/) | Produce a root index () plus per-module files under  â€” each containing scope, core terms, and source file references (not verbatim copies). | Produce a root index () plus per-module files under  â€” each containing scope, core terms, and source file references (not verbatim copies). No classes, no anchors, no UML, no stereotypes. |
| [class-responsibility-collaborator](domain-driven-design/abd-class-responsibility-collaborator/) | This skill takes domain concepts from a completed Ubiquitous Language and produces a structured CRC model: for each concept, what it is responsible for, who it collaborates with, and what must always … | For every domain concept: assign responsibilities, name collaborators, and declare invariants — all in one structured pass before object-model. |
| [ubiquitous-language](domain-driven-design/abd-ubiquitous-language/) | The purpose of this skill is to create a robust domain model that describes domain concepts in a structured, plain-English form — before anyone commits to classes, methods, or properties. | Enrich a module file with structured, plain-English concept blocks so the team has a readable object model before committing to classes. |
| [key-abstractions](domain-driven-design/abd-key-abstractions/) | A shared vocabulary names the pieces of the domain, but it doesn't tell you which concepts carry the weight — which ones anchor the model, own specific responsibilities, and enforce the rules that … | Group UDL terms into named Key Abstractions with prose definitions and verbatim source extracts, elevating a flat term list into defined domain building blocks. |
| [object-model](domain-driven-design/abd-object-model/) | Build a typed object model for a module. | Build a typed object model for a module. A CRC model makes it faster but is not required. Use when a module needs a typed domain surface before writing production code, or when a module has reached … |
| [scenario-walkthrough](domain-driven-design/abd-scenario-walkthrough/) | Walk concrete scenarios through the CRC model. | Produce domain-walkthrough.md: indented scenario walks where every step maps to a class and responsibility from crc.md; lifecycle guards and invariants come from the CRC lifecycle fields. Fix gaps … |

## Engineering

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-acceptance-test-driven-development](story-driven-delivery/abd-acceptance-test-driven-development/) | Write tests first. | Write tests first. Write code to pass them. |
| [abd-clean-code](engineering/abd-clean-code/) | Write production code that implements story behavior using domain language, clean functions, explicit dependencies, and observable design. | Production code that matches story behavior: clean structure, domain language, scanner-backed quality bars (Python/JS). |
| [mern-technical-architecture](engineering/mern-technical-architecture/) | Generate production MERN web applications using a domain-first architecture — organizing by business capability, sharing domain logic across tiers, enforcing Clean Architecture layer purity, and … | Domain-first MERN web applications: domain modules, shared logic, Clean Architecture layers, story-driven tests, scanner-verified compliance. |

## Idea Shaping

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-cost-of-delay](idea shaping/abd-cost-of-delay/) | Teams routinely prioritize work by gut feel, stakeholder loudness, or first-in-first-out — all of which ignore how much value decays while items wait to be delivered. | Quantify urgency × value for backlog items; score CD3 and rank to prioritize by economic impact of delay. |
| [abd-impact-mapping](idea shaping/abd-impact-mapping/) | Impact mapping is a strategic discovery technique that links broader goals to finer-grained goals, then to actors, their observable behaviour changes, and deliverable options (often epics or … | Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources. |
| [abd-opportunity-canvas](idea shaping/abd-opportunity-generation/) | This skill exists so you do not start "building a solution" while people are thinking about a different problem, a different customer, or a different definition of success. | Frame an opportunity, align on vision, and make assumptions and validation explicit before committing build. |
| [abd-simple-validated-learning](idea shaping/abd-simple-validated-learning/) | Opportunities, ideas, and initiatives often carry many unverified assumptions — about customers, value, feasibility, and economics — that the organisation has not yet checked. | Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build. |

## Skill Builder

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-author-practice-skill](skill-builder/abd-author-practice-skill/) | Teams need practice skills that people and agents can follow without improvising or drifting away from what the sources actually say. | Turn collected hub evidence into a finished practice skill: clear instructions and checkable do-and-don't norms that stay true to what you retrieved. |
| [abd-build-practice-scanners](skill-builder/abd-build-practice-scanners/) | Written DO / DO NOT rules are easy to ignore or misread. | Turn written rules into checks a machine can run, so drift is caught early instead of debated in chat. |
| [abd-practice-skill-manual](skill-builder/abd-practice-skill-manual/) | SKILL.md is the compact source of truth; many readers still want a browser-friendly walkthrough with room for diagrams, step layout, and quoted evidence. | Ship a readable HTML companion for a practice: longer walkthroughs, figures, and sources so people can study the method without parsing SKILL.md alone. |
| [abd-query-practice-sources](skill-builder/abd-query-practice-sources/) | Before anyone writes instructions or rules for a practice, you need a single, honest record of what the hub actually contains on that topic: what you read, where it lives, and how each piece supports … | Pull defensible excerpts from the content hub so a new practice can cite real sources, not guesswork: one auditable log of what you kept and why it matters. |
| [abd-skill-catalog](skill-builder/abd-skill-catalog/) | You added, renamed, or retired a skill or agent and the AI Garden is stale. | Regenerate the browsable AI Garden (skills + agents HTML + outline.md) from repo packages. |

## Skill Helpers

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-commit-msg](skill-helpers/commit-msg/) | User types  or requests a commit | Commit messages from scope and changed files; no story_graph (/commit and similar). |
| [correct-output](skill-helpers/correct_output/) | This skill governs what to do when generated output is wrong. | Fix the deliverable first, log corrections, iterate until right — only then improve the source. |
| [deploy-skill-to-cursor](skill-helpers/deploy-skill-to-cursor/) | You added or changed a skill under  and want Cursor and/or VS Code to load it without maintaining a second copy. | Junction-link a repo skill into Cursor/VS Code — skill folder, rules, instructions, and commands. |
| [execute-skill-using-skills-rules](skill-helpers/execute-skill-using-skills-rules/) | execute-skill-using-skills-rules | Run scanners, validate output against rules, fix failures; quality gate before and after work. |
| [skill-garden-catalogue](skill-helpers/skill-garden-catalogue/) | You want a single-page overview of all available skills. | Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML index page. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to … |
| [track-task](skill-helpers/track_task/) | Track task (checkbox progress) | Checkbox markdown task lists for pipelines or ad-hoc steps under the engagement workspace. |

## Story-Driven Delivery

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-acceptance-criteria](story-driven-delivery/abd-acceptance-criteria/) | Build acceptance criteria per story, that explain what must be true when users and systems interact: observable triggers (WHEN), expected outcomes (THEN), chained effects (AND), and explicit … | WHEN/THEN acceptance criteria for story-graph.json; ships rules and scanners for execute-skill-using-skills-rules. |
| [abd-specification-by-example](story-driven-delivery/abd-specification-by-example/) | Write Given/When/Then scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do. | Given/When/Then scenarios with real domain values; plain or outline (data tables) templates. |
| [abd-story-mapping](story-driven-delivery/abd-story-mapping/) | A story map in the Jeff Patton sense is a single shared picture of the product: you organize understanding into a small stack of nested levels—epics (broad capability areas), sub-epics (flows or … | Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources. |
| [abd-thin-slicing](story-driven-delivery/abd-thin-slicing/) | Define prioritized increments. | Thin-sliced MVIs and backlog order from a story map; writes thin-slicing templates. |
| [drawio-story-sync](story-driven-delivery/drawio-story-sync/) | drawio-story-sync | story-graph.json to Draw.io story maps; validated load/save and diagram sync. |
| [miro-story-sync](story-driven-delivery/miro-story-sync/) | miro-story-sync | story-graph.json to Miro story maps; validated load and REST-driven board sync. |
| [story-graph-ops](story-driven-delivery/story-graph-ops/) | Turning a story map in any form into concrete graph JSON—create/update nodes until the file matches intent. | CRUD story-graph.json via CLI/scripts, validate, persist; no hand-written JSON drift. |

## Utilities

| Skill | Challenge | Solution |
| --- | --- | --- |
| [abd-proposal-respond](utilities/abd-proposal-respond/) | User wants to respond to an RFP, Q&A, or proposal requirements | RFP and proposal response: ingest to memory (abd-context-to-memory), strategy, batched Q&A with RAG. |
| [research-compare-approach](utilities/ai-research-assistant/research-compare-approach/) | Given a solution landscape (from research-solution-landscape) and the | Critically compare the user's approach against researched alternatives. Identifies strengths, weaknesses, trade-offs, and legitimate white space. Reads the user's codebase ONLY to understand what … |
| [research-problem-validation](utilities/ai-research-assistant/research-problem-validation/) | Given a problem statement (usually extracted from a hypothesis), determine | Research whether a stated problem is real and worth solving. Searches online and model knowledge for who is talking about the problem, who says it is NOT a problem, competing problems in the same … |
| [research-solution-landscape](utilities/ai-research-assistant/research-solution-landscape/) | Given a validated problem, map how people are actually solving it — the | Map the landscape of competing solutions for a validated problem. Searches online and model knowledge for categories of approaches, key tools and frameworks, trade-offs, and which segments each … |
