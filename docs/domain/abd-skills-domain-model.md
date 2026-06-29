---
state: domain-model
---

# Module: abd-skills

Scope: How abd-skills are organised on disk — what an AbdSkill is made of (references, rules, scanners, templates), how a PracticeSkill belongs to a single Practice that carries one Perspective and its own References shared with every skill in that practice, how a Human drives an AiChatAgent that follows AbdSkills and may delegate to a Subagent or invoke a Cli, and the first-class managed state that the context-driven-delivery skill maintains across a session. Also covers the polymorphic ContextPerspectiveGraph base and the four practice-specific graph types — StoryGraph, DomainGraph, ArchGraph, and UxGraph — together with their node hierarchies, file persistence, CLI, and scanner base. Excludes the kanban delivery practice.

**Core terms**:
- abd skill
- practice skill
- context-driven delivery skill
- practice
- perspective
- reference
- rule
- scanner
- template
- fidelity level
- human
- ai chat agent
- subagent
- agent
- cli
- session
- session checklist
- session journal
- correction
- context index
- context index row
- vector index
- chunk
- chunk embedding
- extraction overview
- sandbox
- dependency stub
- semantic index
- context perspective graph
- context perspective node
- graph file
- graph cli
- graph scanner
- story graph
- story node
- epic
- sub-epic
- story group
- story
- acceptance criterion
- scenario
- step
- example
- increment
- domain graph
- domain node
- domain module
- key abstraction node
- domain concept node
- responsibility
- collaborator
- arch graph
- arch node
- ux graph
- ux node
- screen
- ux interaction

**Key Abstractions (term grouping)**:
- **AbdSkill**: abd skill, practice skill, context-driven delivery skill, practice, perspective, reference, rule, scanner, template, fidelity level
- **AiChatAgent**: human, ai chat agent, subagent, agent, cli
- **Context-Driven Delivery**: session, session checklist, session journal, correction, context index, context index row
- **Context Extraction**: vector index, chunk, chunk embedding, extraction overview, sandbox, dependency stub, semantic index
- **ContextPerspectiveGraph**: context perspective graph, context perspective node, graph file, graph cli, graph scanner
- **StoryGraph**: story graph, story node, epic, sub-epic, story group, story, acceptance criterion, scenario, step, example, increment
- **DomainGraph**: domain graph, domain node, domain module, key abstraction node, domain concept node, responsibility, collaborator
- **ArchGraph**: arch graph, arch node
- **UxGraph**: ux graph, ux node, screen, ux interaction

---

# Core Domain

## **AbdSkill**

### **AbdSkill**

AbdSkill(SkillName, FilePath)
------
name: SkillName
rootPath: FilePath
	Invariant: every AbdSkill lives in its own folder named after the skill and containing SKILL.md at the root
references: Reference
rules: Rule
scanners: Scanner
templates: Template
outputFilename: FileName
	Invariant: declared in SKILL.md; the deliverable the AiChatAgent writes when following this skill
supportedModes: SkillMode
	Invariant: optional — present only on skills that declare modes in their SKILL.md; mode names are local to the declaring skill (e.g., abd-story-mapping declares outline / full; abd-story-specification declares outline / scenario; abd-architecture-specification declares document / template); skills without modes leave this absent

### **PracticeSkill : AbdSkill**

PracticeSkill(SkillName, FilePath, Practice, FidelityLevel)
------
practice: Practice
fidelityLevel: FidelityLevel
	Invariant: present for phase practice skills (under the practice's skills/ folder) and bound to exactly one fidelity level; absent for SupportSkill (under the practice's skills/supporting/ folder)
----
effectiveReferences(): Reference
	Practice
	Invariant: returns this skill's own references plus its practice's references — both are accessible to the skill
perspective(): Perspective
	Practice
	Invariant: a practice skill's perspective is its practice's perspective — never declared independently on the skill

### **SupportSkill : PracticeSkill**

SupportSkill(SkillName, FilePath, Practice)
------
fidelityLevel: FidelityLevel
	Invariant: empty for SupportSkill — support skills live under the practice's skills/supporting/ folder and are callable at any fidelity level
----
### **Practice**

Practice(PracticeName, FilePath, Perspective)
------
name: PracticeName
rootPath: FilePath
	Invariant: every practice lives at practices/<practice-name>/
perspective: Perspective
	Invariant: a practice carries exactly one perspective
references: Reference
	Invariant: every skill in this practice can refer to these references in addition to its own
skills: PracticeSkill
	Invariant: practice skills live under the practice's skills/ folder and skills/supporting/ folder
agents: AbdAgent

### **Reference**

Reference(ReferenceName, FilePath)
------
name: ReferenceName
filePath: FilePath
	Invariant: a reference is a knowledge file the skill or practice owner must read before generating — it lives under the owner's reference/ folder

### **Rule**

Rule(RuleName, FilePath)
------
name: RuleName
filePath: FilePath
	Invariant: a rule lives under the skill's rules/ folder and declares PASS and FAIL examples the skill's output must satisfy

### **Scanner**

Scanner(ScannerName, FilePath)
------
name: ScannerName
filePath: FilePath
	Invariant: a scanner lives under the skill's scanners/ folder and is a runnable check that validates a produced output

### **Template**

Template(TemplateName, FilePath)
------
name: TemplateName
filePath: FilePath
	Invariant: a template lives under the skill's templates/ folder and supplies the canonical structure for the skill's output

### **FidelityLevel** «enum»

CONTEXT | SHAPING | DISCOVERY | EXPLORATION | SPECIFICATION | ENGINEERING
------
	Invariant: values are fixed and ordered — CONTEXT is the earliest entry point, ENGINEERING is the latest; a PracticeSkill carries exactly one value; a SupportSkill carries none


### references

**Ref — abd-skills repository layout**
Source: c:/dev/abd-skills
Locator: common/, practices/<practice>/, practices/<practice>/skills/, practices/<practice>/skills/supporting/, practices/<practice>/reference/, practices/<practice>/agents/
Extract: whole

**Ref — abd-context-driven-delivery skill body**
Source: c:/dev/abd-skills/practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md
Locator: whole file — defines perspective files, specialist agents, the read-gate set
Extract: whole

**Ref — common skill workflow contract**
Source: c:/dev/abd-skills/common/skill-workflow.md
Locator: whole file — defines the read-gates, output file resolution, validate pass
Extract: whole

**Ref — skill index**
Source: c:/dev/abd-skills/common/skill-index.md
Locator: whole file — enumerates every skill, its perspective, its fidelity level, its output filename
Extract: whole

**Ref — domain perspective declaration**
Source: c:/dev/abd-skills/practices/domain-driven-design/reference/domain-perspective.md
Locator: whole file — shows how a practice declares its perspective and lists its phase skills by fidelity
Extract: whole

### decisions made

- *AbdSkill* is the base class for every skill in the repository. Every skill, regardless of where it lives, has a SKILL.md, optional references, rules, scanners, and templates, and a declared output filename.
- *PracticeSkill* inherits everything from AbdSkill and adds two facts: it belongs to a Practice, and it has a FidelityLevel. Its perspective is read off its Practice — never declared on the skill itself.
- *PracticeSkill.effectiveReferences()* is named as a method rather than overriding the references property because the merging behaviour is not a redefinition of own references but a derived view combining own and practice references — both are still navigable separately.
- *ContextDrivenDeliverySkill* is a first-class subtype of AbdSkill with its own member set. It owns the workspace-level ContextIndex, holds the fixed roster of specialist AbdAgents it routes to, and exposes the operations that drive the full delivery loop: startSession, routeToSpecialist, advanceRow, recordCorrection, and runConsistencyCheck. It is not a PracticeSkill — it has no perspective and no fidelity level — but it is far richer than a plain AbdSkill.
- *Context-gathering skills* (`abd-context-to-markdown`, `abd-context-chunk`, `abd-context-db-embed`, `abd-context-db-ask`, `abd-context-app-extractor`, `abd-context-app-sandbox`, `abd-context-semantic-index`) are plain AbdSkill instances, not modelled as a separate subtype. Their fidelity is hard-coded as CONTEXT and they have no perspective binding to any practice. They are not file-producers in the generic sense — each creates a specific named artifact: `abd-context-to-markdown` produces converted Markdown, `abd-context-chunk` produces Chunks (modelled in KA Context-Driven Delivery), `abd-context-db-embed` produces a VectorIndex (modelled), `abd-context-db-ask` queries the VectorIndex, `abd-context-app-extractor` produces an ExtractionOverview (modelled), `abd-context-app-sandbox` produces a runnable Sandbox (modelled), `abd-context-semantic-index` produces a SemanticIndex (modelled).
- *Practice.agents* is included because every practice folder observably contains an `agents/` subfolder with agent definition files. Agents are owned by their practice.
- *Perspective* values are DOMAIN, STORIES, UX, ARCHITECTURE. Each value corresponds to one practice: DOMAIN → domain-driven-design, STORIES → story-driven-delivery, UX → user-experience-design, ARCHITECTURE → architecture-centric-engineering.
- *FidelityLevel* is a fixed ordered enum with six values — CONTEXT, SHAPING, DISCOVERY, EXPLORATION, SPECIFICATION, ENGINEERING — defined by `common/stages/` and enumerated in `common/skill-index.md`. A PracticeSkill carries exactly one value; SupportSkills carry none.
- *SupportSkill* is modelled as a subtype of PracticeSkill. It belongs to a Practice (and therefore inherits its perspective via Practice) but its fidelityLevel is empty — support skills are callable at any fidelity level. The PracticeSkill parent invariant on fidelityLevel is loosened to "present for phase skills, absent for SupportSkill" so the subtype is a proper Liskov substitution; SupportSkill's own block restates the constraint as an override invariant on the inherited fidelityLevel property.
- *outputFilename* is the canonical filename declared in SKILL.md (e.g., `domain-model.md`). The actual output folder is resolved at runtime by the AiChatAgent following `common/skill-workflow.md` — it is therefore not a property of the AbdSkill itself.
- *Reference*, *Rule*, *Scanner*, *Template* are modelled as separate concepts rather than untyped file collections because each plays a distinct role in the skill's contract: references inform, rules constrain, scanners validate, templates shape.
- *supportedModes* is an optional property — not every skill has modes. The handful that do declare their mode names in SKILL.md front matter under `context-fidelity[].mode`. Skills without modes leave the property absent.
- *SkillMode* is a typed string primitive — not a shared enum. Mode names are local to the skill that declares them and have no meaning outside it. The AiChatAgent treats the value as a parameter when following a skill that declares modes; no SkillMode class block is introduced.

---

## **AiChatAgent**

### **AiChatAgent**

AiChatAgent()
------
usingSkill: AbdSkill
	Invariant: a chat agent uses at most one AbdSkill at a time as its active instruction set
spawnedSubagents: Subagent
----
useSkill(AbdSkill): void
	Reference, Rule
	Invariant: before generating output the chat agent must read every file in the skill's rules/, reference/, and common/ folders — including its practice references when the skill is a PracticeSkill. The common/ folder contains shared material (workflows, grill protocols, validation steps) that every AbdSkill depends on and must not be skipped.
spawnSubagent(AbdSkill, AbdAgent?): Subagent
	Invariant: a subagent is given an AbdSkill to use; an AbdAgent persona is optional (e.g. diagramming subagents need no persona)
invoke(Cli, CliArgs): CliOutput

### **Human**

Human()
------
----
invokeSkill(AbdSkill, AiChatAgent): void

### **Subagent : AiChatAgent**

Subagent(AbdSkill, AbdAgent?)
------
persona: AbdAgent [0..1]
	Invariant: when present, the subagent acts under this AbdAgent persona for its lifetime

### **AbdAgent**

AbdAgent(AgentName, FilePath)
------
name: AgentName
filePath: FilePath
	Invariant: an AbdAgent definition lives at practices/<practice>/agents/<agent>.md and supplies the persona instructions a subagent loads when spawned

### **Cli**

Cli(CliName, FilePath, CommandString)
------
name: CliName
filePath: FilePath
	Invariant: lives under common/scripts/ or the owning skill's scripts/ folder
command: CommandString
	Invariant: the shell command the AiChatAgent constructs and runs to invoke this CLI (e.g., `python scripts/build_skill_index.py`)
----
run(CliArgs): CliOutput
	Invariant: executes the command with the supplied arguments and returns the output; callers treat CliOutput as the observable result of the invocation

### references

**Ref — context-driven-delivery skill body**
Source: c:/dev/abd-skills/practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md
Locator: "Routing" section — names ChatAgent / specialist / AGENT.md / subagent
Extract: whole

**Ref — agent definitions folder**
Source: c:/dev/abd-skills/practices/context-driven-delivery/agents/
Locator: business-expert.md, product-owner.md, ux-designer.md, engineer.md, abd-context-to-memory.md
Extract: whole

**Ref — common scripts**
Source: c:/dev/abd-skills/common/scripts/
Locator: whole folder — build_skill_index.py and other runnable utilities
Extract: whole

### decisions made

- *AiChatAgent* is the AI agent the human chats with directly (e.g., Cursor's chat). It sits at the centre of the runtime chain: it follows a skill, spawns subagents, or invokes a CLI.
- *Subagent : AiChatAgent* — a subagent is functionally another chat agent spawned by the parent via the Task tool; substitutable wherever an AiChatAgent is required. A subagent may optionally act under an AbdAgent persona, but not every subagent needs one (e.g. diagramming or scripting subagents).
- *AbdAgent* is the persona definition file — the static `agents/<agent>.md` document. It is distinct from Subagent, which is the runtime spawned to use it. Specialist agents (business-expert, product-owner, ux-designer, engineer) each bind to one perspective via their owning practice; the context-to-memory agent has no perspective binding.
- *Cli* replaces the earlier *Script* concept. A CLI is a first-class runnable with an identity (name), a location (filePath), a shell command to invoke it, and a typed output. The AiChatAgent constructs arguments and calls `invoke(Cli, CliArgs): CliOutput` — the output is the observable result. *CliArgs* and *CliOutput* are typed primitives; no separate class blocks.
- *Human.invokeSkill* takes both the AbdSkill and the AiChatAgent because the human directs a specific chat agent to follow a skill — it is not the only way skills get invoked (agents spawn subagents with skills autonomously), but it is the Human's own operation on the model.
- *Session*, *SessionChecklist*, *SessionJournal*, *Correction*, *ContextIndex* are first-class concepts modelled in a separate KA (Context-Driven Delivery). The AiChatAgent creates and mutates them when following the `abd-context-driven-delivery` skill; they are not modelled as members of AiChatAgent itself.
- *No `ConsistencyCheck`, `Routing`, `Grilling`, `Spawning`, `ReadGate`, `EntryPointDetermination`, or `GridCell` class is introduced.* These are actions the AiChatAgent takes while following a skill — not entities. They are recorded as narrative lines in the SessionJournal but the narrative entries themselves are not first-class concepts; the journal is.

---

## **Context-Driven Delivery**
### **ContextDrivenDeliverySkill : AbdSkill**
------
contextIndex: ContextIndex
	Invariant: one workspace-level index shared across all sessions — read before resolving any output path
specialistAgents: AbdAgent
	Invariant: the fixed set of specialist agents this skill routes work to — one per perspective (domain, stories, ux, architecture) plus the context-to-memory agent
----
startSession(SessionTopic, FidelityLevel): ContextDrivenDeliverySession
	Invariant: creates the session folder, pre-populates the checklist from the confirmed entry point, and opens the journal — must not proceed until the entry point is confirmed by the human
routeToSpecialist(SkillName): Subagent
	AbdAgent
	Invariant: selects the specialist agent bound to the skill's perspective, spawns a subagent under that persona, and passes it the named AbdSkill
advanceItem(FreeText, ChecklistState): void
	Invariant: transitions a checklist line to checked only after the human accepts the specialist output; transitions to skipped only with explicit human confirmation
recordCorrection(Correction): void
	Invariant: appends the correction to the session journal and marks the affected checklist item unchecked so the specialist is re-run
runConsistencyCheck(): void
	Invariant: invoked between stages; inspects the outputs produced so far for contradictions before the next specialist is routed

### **ContextDrivenDeliverySession**

ContextDrivenDeliverySession(SessionTopic, Timestamp, FilePath, FidelityLevel)
------
topic: SessionTopic
startedAt: Timestamp
rootPath: FilePath
	Invariant: every session folder lives at <workspace>/docs/cdd-sessions/<date>-<topic>/
entryPoint: FidelityLevel
	Invariant: the user confirms the entry point; the AiChatAgent never assumes it
checklist: SessionChecklist
journal: SessionJournal

### **SessionChecklist**

SessionChecklist(FilePath)
------
filePath: FilePath
	Invariant: file is named cdd-session-checklist.md and lives in the session's root path
items: FreeText
	Invariant: markdown checkbox lines (`- [ ]` / `- [x]` / `- [-]`) — pre-populated from the confirmed entry point; one line per skill invocation or consistency-check action in scope

### **SessionJournal**

SessionJournal(FilePath)
------
filePath: FilePath
	Invariant: file is named cdd-session-journal.md and lives in the session's root path
corrections: Correction
	Invariant: corrections are session-local — they guide re-runs within this session and travel with the prompt context when affected specialists are re-spawned

### **Correction**

Correction(CorrectionKind, FreeText, FreeText, FreeText)
------
kind: CorrectionKind
	Invariant: DO indicates a positive rule (always do X); DO_NOT indicates a prohibition (never do Y)
rule: FreeText
wrongExample: FreeText
	Invariant: records what was done incorrectly in this session
correctExample: FreeText
	Invariant: records what it should have been
affectedItem: FreeText
	Invariant: identifies the checklist line that is reset to unchecked until the corrected specialist output is reviewed and accepted

### **ContextIndex**

ContextIndex(FilePath)
------
filePath: FilePath
	Invariant: lives at <workspace>/cdd-context-index.md — workspace-level, not session-level
rows: ContextIndexRow
	Invariant: every row corresponds to one artifact whose actual path diverges from its canonical path under common/folder-conventions.md

### **ContextIndexRow**

ContextIndexRow(ArtifactType, FilePath, FilePath, FreeText)
------
artifactType: ArtifactType
	Invariant: identifies what kind of artifact this row covers (e.g., domain-model, story-map, glossary)
canonicalPath: FilePath
	Invariant: the path the skill would have written to by default per common/folder-conventions.md
actualPath: FilePath
	Invariant: differs from canonicalPath — divergence is the reason the row exists
notes: FreeText

### references

**Ref — context-driven-delivery skill body**
Source: c:/dev/abd-skills/practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md
Locator: sections "Progress tracking", "Session journal", "Non-standard paths", "Corrections"
Extract: whole

**Ref — session-journal template**
Source: c:/dev/abd-skills/practices/context-driven-delivery/skills/abd-context-driven-delivery/templates/session-journal.md
Locator: whole file — defines Q→A lines, Ran lines, Consistency lines, Open section, Corrections section, restart guide
Extract: whole

**Ref — context-scaffold session folder template**
Source: c:/dev/abd-skills/common/context-scaffold/cdd-sessions/YYYY-MM-DD-topic/
Locator: cdd-session-checklist.md, cdd-session-journal.md — the canonical per-session files
Extract: whole

**Ref — context-scaffold cdd-context-index template**
Source: c:/dev/abd-skills/common/context-scaffold/cdd-context-index.md
Locator: whole file — defines the workspace-level table shape Artifact | Canonical path | Actual path | Notes
Extract: whole

### decisions made

- *ContextDrivenDeliverySession* is the first-class concept and names the KA. A session is bounded by its folder under `docs/cdd-sessions/<date>-<topic>/`; it owns its checklist and journal.
- *SessionChecklist.items* is a collection of plain markdown checkbox lines — not a class. The text of the line is the only identity a checklist item needs. Consistency-check lines and skill-invocation lines are distinguished by reading the text, not by a type field.
- *ChecklistState* values are UNCHECKED, CHECKED, SKIPPED.
- *SessionJournal* has no `entries` collection. Q→A lines, Ran lines, Consistency lines, and Open notes are narrative records of actions and are not modelled as first-class concepts. Corrections are the only structured collection because they have schema (rule + wrongExample + correctExample) and they influence subsequent agent behaviour by triggering a re-run.
- *Correction.affectedItem* ties a correction to the checklist line that must be reset — necessary because re-running the affected cell is the whole point of recording a correction.
- *CorrectionKind* values are DO and DO_NOT.
- *ContextIndex* sits in this KA even though it is workspace-level (not per-session) because it is managed by the ContextDrivenDeliverySkill and its read-gate is declared in that skill body.
- *ArtifactType* is a typed primitive. Values are open-ended and are not enumerated as a constrained enum.
- No `JournalRunLine`, `JournalQuestionAnswer`, `JournalConsistencyEntry`, `JournalOpenEntry`, `ConsistencyCheck`, `Routing`, `EntryPointDecision`, or `GridCell` class is introduced. These are actions the AiChatAgent takes while following the CDD skill, not entities.

---

## **Context Extraction**

### **VectorIndex**

VectorIndex(FilePath)
------
rootPath: FilePath
	Invariant: a local FAISS-based vector index produced by abd-context-db-embed and queried by abd-context-db-ask; this is the durable agent memory store
embeddings: ChunkEmbedding
	Invariant: each embedding traces back to exactly one Chunk by chunkIdentifier
embeddingModel: EmbeddingModelName
	Invariant: queries succeed only when the asker uses the same embedding model the index was built with

### **Chunk**

Chunk(ChunkIdentifier, FilePath, FreeText, EvidenceLabel)
------
identifier: ChunkIdentifier
sourceMarkdownPath: FilePath
	Invariant: the markdown file the chunk was split from must have been produced by abd-context-to-markdown or live on disk in the same shape
content: FreeText
evidenceLabel: EvidenceLabel
	Invariant: every chunk carries an evidence label so retrieval results can be traced back to their origin

### **ChunkEmbedding**

ChunkEmbedding(ChunkIdentifier, EmbeddingVector)
------
chunkIdentifier: ChunkIdentifier
	Invariant: matches the identifier of exactly one Chunk
vector: EmbeddingVector
	Invariant: produced by the VectorIndex's embeddingModel; semantic search compares query vectors against this one

### **ExtractionOverview**

ExtractionOverview(FilePath)
------
filePath: FilePath
	Invariant: produced by abd-context-app-extractor at extraction-overview.md and records structured per-page context for a live application

### **Sandbox**

Sandbox(FilePath)
------
rootPath: FilePath
	Invariant: produced by abd-context-app-sandbox — a runnable copy of the application with external dependencies stubbed at the earliest interface boundary; every screen must be reachable via the smoke test the skill installs
stubs: DependencyStub
	Invariant: every external service identified in the source codebase has at least one DependencyStub at its earliest interface boundary

### **DependencyStub**

DependencyStub(DependencyName, FilePath)
------
dependencyName: DependencyName
	Invariant: matches the external service or library being stubbed
filePath: FilePath
	Invariant: lives inside the Sandbox rootPath and intercepts calls at the earliest interface boundary so the sandbox runs without the real dependency

### **SemanticIndex**

SemanticIndex(FilePath)
------
filePath: FilePath
	Invariant: produced by abd-context-semantic-index at context-chunking-report.md — a coverage index labelling source content by context kind (Story, Domain, Architecture, UX) before deeper analysis begins

### references

**Ref — context-gathering skill descriptions**
Source: c:/dev/abd-skills/practices/context-driven-delivery/skills/
Locator: SKILL.md description fields for abd-context-to-markdown, abd-context-chunk, abd-context-db-embed, abd-context-db-ask, abd-context-app-extractor, abd-context-app-sandbox, abd-context-semantic-index
Extract: whole — each description names the artifact the skill produces or queries

### decisions made

- *Context Extraction* is a separate KA from Context-Driven Delivery. The skills that produce these artifacts live in the same practice folder but the artifacts themselves — indexes, chunks, sandboxes — belong to a distinct concern: preparing raw context for consumption, not driving a delivery session.
- *VectorIndex*, *Chunk*, *ChunkEmbedding*, *ExtractionOverview*, *Sandbox*, *DependencyStub*, *SemanticIndex* are placeholder-level entries at this fidelity. Internal structure will be deepened when the individual context-extraction skills are modelled in detail.
- *EmbeddingVector*, *EmbeddingModelName*, *ChunkIdentifier*, *EvidenceLabel*, *DependencyName* are typed primitives — no separate class blocks.

---

## **ContextPerspectiveGraph**

### **ContextPerspectiveGraph**

ContextPerspectiveGraph(GraphName, FilePath)
------
name: GraphName
rootPath: FilePath
	Invariant: every practice graph serialises to a single JSON file at this path — the file is the single source of truth
topLevelNodes: ContextPerspectiveNode
	Invariant: the roots of the graph tree; all other nodes are reachable by traversing children
----
findByName(NodeName): ContextPerspectiveNode
	Invariant: searches the full tree; returns the first node whose name matches
allNodes(): ContextPerspectiveNode
	Invariant: depth-first traversal of the full tree
save(GraphFile): void
	Invariant: delegates persistence to GraphFile; never writes directly to disk
load(GraphFile): ContextPerspectiveGraph
	Invariant: delegates deserialisation and structural validation to GraphFile

### **ContextPerspectiveNode**

ContextPerspectiveNode(NodeName, NodeType)
------
name: NodeName
nodeType: NodeType
	Invariant: allowed values are declared by the owning graph subtype; NodeType is a typed string, not a shared enum
children: ContextPerspectiveNode
	Invariant: allowed child types for each parent type are constrained by the graph subtype's type schema — not enforced at this base level
sequentialOrder: SequenceNumber [0..1]
	Invariant: present when ordering is significant within the parent's child list; absent for unordered children
behavior: FreeText [0..1]
	Invariant: optional human-readable description of what this node represents in delivery context
----
addChild(ContextPerspectiveNode): void
	Invariant: child's nodeType must be in the allowed child types for this node's nodeType in the owning graph
rename(NodeName): void
	Invariant: new name must be unique among siblings

### **GraphFile**

GraphFile(FilePath)
------
filePath: FilePath
	Invariant: the JSON file on disk that backs one ContextPerspectiveGraph
contentSha: ShaHex
	Invariant: SHA of the current file content — used for optimistic concurrency; recalculated on every load
----
load(): ContextPerspectiveGraph
	Invariant: validates structure on load; raises on malformed content
save(ContextPerspectiveGraph, ShaHex?): void
	Invariant: acquires an advisory lock for the duration of the write; if ShaHex is supplied, rejects the write if the file has changed since that SHA was captured (optimistic concurrency); releases lock on completion or error
sha(): ShaHex
	Invariant: returns the current content SHA without loading the full graph — used to capture a baseline before editing

### **GraphCli**

GraphCli(CliPath)
------
cliPath: FilePath
	Invariant: path to the CLI entry script (e.g., story_graph_cli.py)
----
read(FilePath): ContextPerspectiveGraph
	Invariant: loads and validates the graph file; exits non-zero on structural error — the canonical validation command
write(FilePath, ContextPerspectiveGraph, ShaHex?): void
	Invariant: serialises and saves via GraphFile; honours optimistic concurrency when ShaHex is supplied
names(FilePath): NodeName
	Invariant: returns the flat list of all node names in the graph — useful for coverage checks
search(FilePath, FreeText): ContextPerspectiveNode
	Invariant: returns all nodes whose name contains the search text
sha(FilePath): ShaHex
	Invariant: returns the content SHA of the file without loading the graph structure
filter(FilePath, NodeName): ContextPerspectiveGraph
	Invariant: returns a sub-graph rooted at the named node

### **GraphScanner**

GraphScanner(ScannerName)
------
name: ScannerName
	Invariant: scanner name matches the rule file it enforces
----
scan(ContextPerspectiveGraph): ScanResult
	Invariant: every scanner traverses the graph and emits violations — never modifies the graph
	Invariant: a scanner that needs graph structure imports from the owning graph's domain module, not from a peer graph type

### references

**Ref — story-graph-ops SKILL.md**
Source: c:/dev/abd-skills/practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md
Locator: CLI section, concurrency section, scanner section
Extract: whole

**Ref — story_graph_ops/nodes.py**
Source: c:/dev/abd-skills/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py
Locator: StoryNode ABC — name, sequential_order, behavior, children, save, rename
Extract: base class section

**Ref — story_graph_file.py**
Source: c:/dev/abd-skills/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_file.py
Locator: whole file — validated load/save, SHA, advisory lock
Extract: whole

### decisions made

- *ContextPerspectiveGraph* is the polymorphic base for every practice graph. The four concrete subtypes (StoryGraph, DomainGraph, ArchGraph, UxGraph) share file persistence, CLI shape, and scanner base — modelled here so the pattern is named once.
- *GraphFile* owns all concurrency concerns: advisory locking and SHA-based optimistic concurrency. The graph itself knows nothing about files; GraphFile knows nothing about node semantics.
- *GraphCli* defines the command shape shared across all practice CLIs. Each practice subtype may add subcommands but must honour the base six (read, write, names, search, sha, filter).
- *NodeType* is a typed string primitive, not a shared enum. Allowed values are declared per graph subtype in their own type schema. Enforcing the schema is the job of the subtype's GraphScanner, not this base class.
- *GraphScanner* imports from the owning graph's domain module. Scanners for StoryGraph import from story_map / story_scanner; scanners for DomainGraph import from the domain module. Cross-graph imports are prohibited.

---

## **StoryGraph**

### **StoryGraph : ContextPerspectiveGraph**

StoryGraph(GraphName, FilePath)
------
increments: Increment
	Invariant: the ordered release plan — separate from the epic/story tree; each increment references stories by name
----
allStories(): Story
	Invariant: depth-first traversal returning every Story node regardless of nesting depth
filterByIncrement(Increment): Story
	Invariant: returns stories whose name appears in the increment's storyReferences

### **StoryNode : ContextPerspectiveNode**

StoryNode(NodeName, StoryNodeType)
------
----
save(): void
	Invariant: persists this node's mutations to the owning StoryGraph file via GraphFile
rename(NodeName): void
	StoryGraph
	Invariant: unique among siblings; propagates the rename to any Increment.storyReferences that reference the old name

### **Epic : StoryNode**

Epic(NodeName)
------
children: StoryNode
	Invariant: allowed child types are SubEpic and StoryGroup

### **SubEpic : StoryNode**

SubEpic(NodeName)
------
children: StoryNode
	Invariant: allowed child types are SubEpic (recursive) and StoryGroup

### **StoryGroup : StoryNode**

StoryGroup(NodeName)
------
children: StoryNode
	Invariant: allowed child type is Story only

### **Story : StoryNode**

Story(NodeName, ActorName)
------
storyType: ActorName
	Invariant: the actor from the "Actor --> Story Name" syntax; identifies who benefits from this story
acceptanceCriteria: AcceptanceCriterion
scenarios: Scenario
testClass: TestClassName [0..1]
testMethods: TestMethodName
fileLink: FilePath [0..1]
	Invariant: path to the test file that implements this story's scenarios

### **AcceptanceCriterion**

AcceptanceCriterion(WhenText, ThenText)
------
when: WhenText
then: ThenText
andClauses: FreeText
evidence: FreeText [0..1]
	Invariant: cites the source artifact and line number that justifies this criterion

### **Scenario : StoryNode**

Scenario(NodeName)
------
children: StoryNode
	Invariant: allowed child types are Step and Example

### **Step : StoryNode**

Step(FreeText)
------
text: FreeText
	Invariant: a single Given/When/Then/And line; leaf node with no children

### **Example : StoryNode**

Example(NodeName)
------
columns: ColumnName
	Invariant: the header row of the example table
rows: FreeText
	Invariant: each row is an ordered list of cell values aligned to columns; leaf node with no children

### **Increment**

Increment(IncrementName, Priority)
------
name: IncrementName
priority: Priority
	Invariant: 1-based integer; position in the ordered release plan; kept in sync with list position on reorder
storyReferences: NodeName
	Invariant: ordered list of story names in this increment; names must match Story.name values in the graph

### **StoryGraphCli : GraphCli**

StoryGraphCli(CliPath)
------
----
filter(FilePath, NodeName, IncludeLevel?): StoryGraph
	Invariant: extends base filter — IncludeLevel controls how deep into the story content to include (domain_concepts, acceptance, scenarios, examples, tests, code); absent means full content

### references

**Ref — story_graph_ops/nodes.py**
Source: c:/dev/abd-skills/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py
Locator: Epic, SubEpic, StoryGroup, Story, Scenario, Step, Example, Increment class definitions
Extract: whole

**Ref — story-graph-ops SKILL.md**
Source: c:/dev/abd-skills/practices/story-driven-delivery/skills/supporting/story-graph-ops/SKILL.md
Locator: CLI section, markdown conversion scripts, concurrency section
Extract: whole

### decisions made

- *StoryGraph* extends ContextPerspectiveGraph. Its NodeType values are EPIC, SUB_EPIC, STORY_GROUP, STORY, SCENARIO, STEP, EXAMPLE — not a shared enum; the type schema is enforced by StoryGraph's scanners.
- *Increment* is a separate collection on StoryGraph, not a node in the tree. It references stories by name and carries its own ordered priority. Reordering increments mutates the array and renumbers priority.
- *AcceptanceCriterion* is not a StoryNode — it has no children and no sequential position in the tree. It is a value attached to a Story.
- *Story* carries no reference to DomainGraph. The connection between stories and domain concepts is intentionally absent at this fidelity — it will be modelled as an explicit concept in a later pass.
- *StoryGraphCli* adds the IncludeLevel parameter to filter, which controls content depth. The six base commands are inherited unchanged.
- *TestClass*, *TestMethodName*, *ActorName*, *ColumnName*, *Priority*, *SequenceNumber*, *ShaHex*, *TestClassName*, *WhenText*, *ThenText*, *IncrementName* are typed primitives.

---

## **DomainGraph**

### **DomainGraph : ContextPerspectiveGraph**

DomainGraph(GraphName, FilePath)
------
----
allConcepts(): DomainConceptNode
	Invariant: returns every DomainConceptNode in the graph regardless of module or KA nesting
findModule(ModuleName): DomainModule
findKeyAbstraction(KaName): KeyAbstractionNode

### **DomainNode : ContextPerspectiveNode**

DomainNode(NodeName, DomainNodeType)
------
----

### **DomainModule : DomainNode**

DomainModule(ModuleName)
------
children: DomainNode
	Invariant: allowed child type is KeyAbstractionNode only

### **KeyAbstractionNode : DomainNode**

KeyAbstractionNode(KaName)
------
children: DomainNode
	Invariant: allowed child types are DomainConceptNode and TermNode

### **DomainConceptNode : DomainNode**

DomainConceptNode(ConceptName)
------
responsibilities: Responsibility
inheritsFrom: ConceptName [0..1]
	Invariant: names the parent concept in the same graph; single inheritance only
module: ModuleName [0..1]
	Invariant: denormalised reference to the owning module — present when the concept is accessed outside its module context
children: DomainNode
	Invariant: allowed child types are PropertyNode and OperationNode

### **Responsibility**

Responsibility(FreeText)
------
name: FreeText
collaborators: Collaborator
	Invariant: the other concepts this responsibility requires to do its work

### **Collaborator**

Collaborator(ConceptName)
------
name: ConceptName
	Invariant: matches the name of another DomainConceptNode in the same graph

### **DomainGraphCli : GraphCli**

DomainGraphCli(CliPath)
------
----
render(FilePath, FilePath): void
	Invariant: reads the domain model markdown at the first path and writes a DrawIO class diagram to the second path; one DrawIO tab per KA

### references

**Ref — story_graph_ops/domain.py**
Source: c:/dev/abd-skills/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py
Locator: DomainConcept, Responsibility, Collaborator
Extract: whole

**Ref — domain_concept_node.py**
Source: c:/dev/abd-skills/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/domain_concept_node.py
Locator: DomainConceptNode — position tracking in the graph
Extract: whole

**Ref — drawio_domain_cli.py**
Source: c:/dev/abd-skills/practices/domain-driven-design/skills/supporting/drawio-domain-sync/scripts/drawio_domain_cli.py
Locator: whole — CLI entry point for domain model rendering
Extract: whole

### decisions made

- *DomainGraph* is partially implemented. The node types (MODULE, KEY_ABSTRACTION, CONCEPT, TERM, PROPERTY, OPERATION) follow the domain-model.md format. DomainGraphCli currently provides a render command (markdown → DrawIO); the base GraphCli read/write/names pattern is not yet implemented for this graph type.
- *KeyAbstractionNode* is named with the Node suffix to avoid collision with the domain term Key Abstraction used throughout the abd-skills model — the node is the graph representation of a KA, not the KA concept itself.
- *DomainConceptNode.inheritsFrom* is a name reference, not a pointer — consistent with the markdown format where inheritance is declared as `ClassName : BaseClass`.
- *Responsibility* and *Collaborator* are not DomainNodes — they have no children and do not participate in the graph tree. They are value objects attached to a DomainConceptNode.
- *TermNode* (a leaf node representing a ubiquitous language term) is named but not given a full class block at this fidelity.

---

## **ArchGraph**

### **ArchGraph : ContextPerspectiveGraph**

ArchGraph(GraphName, FilePath)
------
----

### **ArchNode : ContextPerspectiveNode**

ArchNode(NodeName, ArchNodeType)
------
----

### references

**Ref — abd-architecture-outline SKILL.md**
Source: c:/dev/abd-skills/practices/architecture-centric-engineering/skills/abd-architecture-outline/SKILL.md
Locator: whole — defines the artifacts (system context, mechanisms, modules) that will become node types
Extract: whole

### decisions made

- *ArchGraph* is not yet implemented. The KA is created as a placeholder so the polymorphic graph hierarchy is complete. Node types are expected to cover: SYSTEM, MECHANISM, MODULE, PRINCIPLE, DECISION — matching the architecture-outline and architecture-blueprint skill outputs.

---

## **UxGraph**

### **UxGraph : ContextPerspectiveGraph**

UxGraph(GraphName, FilePath)
------
----
allScreens(): Screen
allInteractions(): UxInteraction

### **UxNode : ContextPerspectiveNode**

UxNode(NodeName, UxNodeType)
------
----

### **Screen : UxNode**

Screen(ScreenName)
------
children: UxNode
	Invariant: allowed child types are SectionNode and DataFieldNode

### **UxInteraction**

UxInteraction(ScreenName, ScreenName, FreeText)
------
fromScreen: ScreenName
toScreen: ScreenName
	Invariant: both names must match Screen.name values in the owning UxGraph
label: FreeText
	Invariant: describes the trigger (e.g., "tap Continue", "submit form")

### references

**Ref — abd-ux-information-architecture SKILL.md**
Source: c:/dev/abd-skills/practices/user-experience-design/skills/abd-ux-information-architecture/SKILL.md
Locator: whole — defines the IA artifact (site map, navigation, content model) that maps to UxGraph node types
Extract: whole

### decisions made

- *UxGraph* is partially sketched. Screen and UxInteraction are the two first-class node types visible in the IA skill output. SectionNode and DataFieldNode are anticipated but not given full class blocks at this fidelity.
- *UxInteraction* is not a UxNode — it is a directed edge between two screens. It does not participate in the tree hierarchy; it is a separate collection on UxGraph analogous to Increment on StoryGraph.

---
