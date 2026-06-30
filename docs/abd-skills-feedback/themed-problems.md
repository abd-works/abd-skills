# Themed Problems — abd-skills feedback from the pml-midtier reverse-engineer session

**Source:** every Correction block in `../cdd-session-journal.md` (lines 105–384, plus the Consistency Check finding at lines 151–195).
**Purpose:** consolidate the recurring problem patterns the session surfaced so each can be examined against `c:\dev\abd-skills` separately. **No solutions in this file** — countermeasures live in `self-grill-and-countermeasures.md` and `diagnose.md`.

---

## At a glance — 11 themes, 3 cross-cutting concerns

| # | Theme | Where the pain showed up |
|---|---|---|
| 1 | Orchestrator self-routing fails for "existing application" entry | Discovery proposed instead of Context; sandbox-skill attachment ignored |
| 2 | Grill discipline is fragile | Questions asked after generation; multiple at once; not first searched from skills/rules |
| 3 | Folder & granularity conventions drift | `docs/sessions/` vs `cdd-sessions/`; multi-step skill plans collapsed into one checklist line |
| 4 | Proxy / midtier semantics not native to story & spec skills | AC and spec describe external behavior; two-phase pattern missing; vague verbs at boundaries |
| 5 | Spec example tables drift from the domain model | Test-infra table names; sentence-filled cells; opaque "behavior" columns |
| 6 | Scanners give false confidence; AI verification missing | Column-only checks; no cell-content check; no system+op explicitness check |
| 7 | Stubs and fixtures duplicated by hand instead of referenced | Fixtures hand-rebuilt; display strings hardcoded from stub values |
| 8 | Domain code map conventions inconsistent across system roles | Wrong heading concept; type-def buried in table; client columns used for proxy/mediator |
| 9 | Story map ↔ graph ↔ spec ↔ test alignment is a cleanup pass, not a gate | Spec headings invented; graph patched without MD; empty stubs to inflate counts |
| 10 | Diagram / template tooling silently fails on HTML entities | `str.replace` no-op on draw.io `&#10;` placeholders; no post-write placeholder scan |
| 11 | Semantic ↔ implementation drift surface (e.g. HTTP 401 vs 403) | Structural checks pass while real correctness gap sits unowned |

**Cross-cutting concerns observable across multiple themes:**

- **C1 — "Single source of truth" is repeatedly violated.** The domain model is canonical (Themes 5, 6, 8), the stubs/data/ directory is canonical (Theme 7), the story map is canonical (Theme 9), and one `domain-model.md` is canonical for multi-layer code maps (Theme 8). Each theme reinvents this rule locally instead of inheriting one general one.
- **C2 — "Validate before generate" / "gate not cleanup" is repeatedly violated.** Entry point (Theme 1), grilling (Theme 2), spec rule conformance (Theme 6), and story alignment (Theme 9) are all easier to enforce as gates than to retrofit afterwards.
- **C3 — Scanners are necessary but not sufficient.** Scanners check structure they were designed for, miss what they weren't (Theme 6). Multiple corrections explicitly call out scanner gaps (table names; cell content; system+op explicitness; story map ↔ graph divergence; post-write placeholder scan).

---

## Theme 1 — Orchestrator self-routing fails for "existing application" entry

**Pattern.** The CDD orchestrator recommended **Discovery** as the entry point because code research artifacts already existed. The user pointed out that an existing running application without runtime extraction means the entry point is **Context** (sandbox + extract), not Discovery. The `abd-context-app-sandbox` skill was even attached to the opening message, which should have been an immediate signal.

**Observed in journal:**
- Lines 105–115: "DO NOT recommend Discovery as the entry point for an existing application without first checking whether the Context phase (sandbox + extract) has been completed."
- Lines 109–111: "DO treat an attached skill as a strong signal."
- Lines 113–115: "DO NOT wait for the user to point out missed entry point rules."

**Adjacent failures:**
- Lines 141–143: Handoff corrections were read but not applied in the same turn — generation began before grilling, despite the explicit DO-NOT correction.

---

## Theme 2 — Grill discipline is fragile

**Pattern.** The session journal shows three distinct failure modes for grilling:

1. **Grill after generate** — questions surfaced after the output was already written, requiring re-runs. (Lines 125–127.)
2. **Multiple questions at once** — all grill prompts dumped in one response, putting the sequencing burden on the user. (Lines 145–147.)
3. **Grill the user without first checking skill + rules + existing outputs** — user-time wasted on questions whose answers were in the skill's `## Grill prompts`, in each `rules/*.md` FAIL example, or in existing skill outputs. (Lines 198–208.)

**Observed:** All three corrections explicitly added in this session, demonstrating that the existing `common/grill-me-with-practice-skill.md` did not prevent them on its own.

---

## Theme 3 — Folder & granularity conventions drift

**Pattern A — Folder naming drift.** The canonical session folder is `cdd-sessions/`, but rules and documentation in multiple places still say `docs/sessions/...`. Result: agents reference the wrong path. (Lines 117–119.)

**Pattern B — Skill plan granularity collapse.** A skill that embeds a multi-step CDD plan (e.g. `abd-context-app-sandbox`'s sandbox-mini-discovery) had three distinct skill runs collapsed into a single checklist item, losing per-skill traceability and checkable atoms. (Lines 121–123.)

---

## Theme 4 — Proxy / midtier semantics not native to story & spec skills

**Pattern.** The skills `abd-story-acceptance-criteria` and `abd-story-specification` were written for systems that own their behavior. When applied to a midtier (proxy / mediator), they produced ACs and specs that:

- Described what the **external** system does instead of what the **midtier** sends and returns. (Lines 129–133.)
- Jammed the whole flow into one When clause instead of using the two-phase **When → Then → When → Then** shape (app calls midtier → midtier forwards → external responds → midtier returns). (Lines 231–234.)
- Used **Given** to describe stub behavior rather than declare what domain entities exist in the external system. (Lines 235–242.)
- Used vague verbs ("fetches", "verifies", "detects", "validates", "runs the order sequence") at boundary-crossing steps, omitting the **target system** and **operation name**. (Lines 243–250.)
- Failed to bold every external system name uniformly and put every operation in backticks. (Lines 251–254.)

**Net effect:** specs that are not testable as midtier specs — they assert outcomes that belong to a system the midtier does not own.

---

## Theme 5 — Spec example tables drift from the domain model

**Pattern.** Scenario-outline example tables in midtier specs contained:

- **Table names** that were test-infrastructure labels (`CartCreationSetup`, `MavenirAccountSetup`, `RegistrationOutcome`, `VoucheraStub`, `PaymentStatusSetup`, `WaitingPsimState`, `PayUpFrontSetup`) rather than domain concepts from `domain.json`. (Lines 213–216.)
- **Column names** that described narrative stub behavior (`mavenir_stub_behavior`, `amplify_behavior`, `duplicate_guard`, `cart_response`, `billing_action`, `gateway_poll_behavior`, `payment_method_outcome`, `psim_action`, `mavenir_guard_behavior`) rather than domain attributes. (Lines 221–223, 373–377.)
- **Cell values** that were prose sentences (e.g. *"respond HTTP 409 Conflict (cart already exists)"*) instead of atomic data values. (Lines 217–219.)
- **Opaque single-column responses** (`mavenir_stub_response`, `payment_method_stub`) that bundled a full external response into one cell. (Lines 379–381.)

**Root cause:** for every external service, the **service-specific domain model module** (`docs/domain/model/modules/{service}-domain-model.md`) is the authoritative source of stub field names — but specs were authored without that lookup. (Lines 383.)

---

## Theme 6 — Scanners give false confidence; AI verification missing

**Pattern.** Scanners ran clean while real rule violations sat in the artifact. Specifically:

- `example-tables-domain-scanner.py` validates **column** names against `domain.json` but does **not** validate **table** names. Test-infra labels passed silently. (Lines 225–229.)
- `then-asserts-concrete-output-scanner.py` checks **step text** for `{token}` / *italic* / "quoted" values but does **not** check **example-table cell contents** — sentence-filled cells passed silently. (Lines 225–229.)
- **No scanner exists** for the system+operation explicitness rule at boundary-crossing steps. (Lines 254–255.)
- **No scanner exists** for table NAME ↔ domain concept matching. (Line 229.)
- **No scanner exists** for story-map MD ↔ story-graph JSON ↔ spec heading bidirectional alignment. (Lines 345–369.)
- **No verification step** runs after writing a diagram file to confirm `{...}` placeholders are gone. (Lines 137–139.)

**Reinforced corrective rule:** "DO NOT rely solely on scanners to validate rule compliance. AI review MUST independently verify rule compliance by reading the domain model and comparing structure, names, columns, AND cell values against it." (Lines 225–227.)

---

## Theme 7 — Stubs and fixtures duplicated by hand instead of referenced

**Pattern.** Scenario fixtures used in tests were hand-typed instead of imported from the existing single-source stub data, creating two parallel sources that drift silently.

- Fixture objects manually rebuilt from `stubs/data/` exports — e.g. `PROSPECT_WITH_STARTER_CART.cart.bundle` typed by hand instead of being a reference to `stubCatalog[0]`. (Lines 259–262.)
- Display strings derived from stub values were **hardcoded** in fixtures (`'$25/mo'`) instead of being computed from the canonical constant. (Lines 263–267.)

---

## Theme 8 — Domain code map conventions inconsistent across system roles

**Pattern.** A `domain-code-map.md` artifact (which is required for documenting existing systems but easy to skip) was produced inconsistently:

- **KA heading** used the **implementation type name** (e.g. `## KA: CustomerResponse`) instead of the **canonical domain concept** (`## KA: Customer`). (Lines 274–286.)
- The **source type definition** appeared as the first **table row** instead of being part of the class heading line. (Lines 278–281, 318–322.)
- A **single column-set format** (4 columns: Member · Kind · Code location · API endpoint) was applied to a **proxy/mediator** that needed an 8-column format (Paradise in → out · External system · External endpoint · External in → out). (Lines 291–314, 324–328.)
- **Per-system code maps** for a multi-layer stack (pml-my client + pml-midtier server) were built **independently**, then reconciled post-hoc with a "Domain Alignment" section instead of being driven from one canonical `domain-model.md`. (Lines 332–341.)
- `domain-code-map.md` was **skipped** because the system was being **reverse-engineered**, not greenfield — even though existing-system documentation is exactly when it matters most. (Lines 311–314.)

---

## Theme 9 — Story map ↔ graph ↔ spec ↔ test alignment is a cleanup pass, not a gate

**Pattern.** The story map (`story-map.md`), story graph (`story-graph.json`), spec file (`specification-by-example.md`), and test file (Cypress / Jest `describe` blocks) drifted silently:

- Spec `## Story:` headings were **invented from route analysis** or prior context, not pulled from the story map. (Lines 363–365.)
- Sub-epics were added to `story-graph.json` (via a patch script) **without simultaneously** updating `story-map.md` — leaving a window of MD/JSON inconsistency. (Lines 351–353.)
- When counts mismatched, **empty stub `## Story:` sections were inserted** solely to reach an alignment count, misrepresenting coverage. (Lines 355–357.)
- Alignment was treated as a **cleanup pass at the end** instead of a **gate before generation begins**. (Lines 359–361.)

**Allowed pattern (intentional):** blank stub `## Story:` headings with no scenarios when a story genuinely cannot be exercised in the current environment (e.g. external system unavailable). (Lines 367–369.)

---

## Theme 10 — Diagram & template tooling silently fails on HTML entities

**Pattern.** A draw.io XML template (`{ROUTE_LIST}`-style placeholders) was filled with Python `str.replace`. The template uses HTML entities for newlines (`&#10;`), so the plain-text replacements **silently no-op** — zero replacements made, no exception raised, the file stayed a template. (Lines 135–139.)

**Adjacent issue:** there was no **post-write verification** that the output file no longer contains `{...}` placeholder tokens — so the failure persists undetected through the workflow.

---

## Theme 11 — Semantic ↔ implementation drift surface (HTTP 401 vs HTTP 403)

**Pattern.** During the Exploration consistency check, an authentic correctness gap was discovered: the AC for "Validate JWT and Promote Credentials" expects HTTP 401 for an expired JWT, but the implementation throws an `authorization`-typed `Err` that maps to HTTP 403. (Lines 180–194.)

**The pattern is meta**, not about 401/403 specifically:

- All five **structural** consistency checks passed.
- The **semantic** check (does the code actually do what the AC says) surfaced one real defect.
- The defect is **noted in the journal as a "recommendation to carry to Specification"** — but there is no mechanism in the skills to convert that into a tracked action item beyond a paragraph of prose.

**Risk:** these semantic findings rely on a human reading the journal and remembering to address them. The skills do not generate a ticket, an issue file, or a tracked gap entry.

---

## Cross-theme observations

### C1 — "Single source of truth" recurs

| Source of truth | Where it gets violated | Theme |
|---|---|---|
| `domain.json` / `domain-model.md` (concepts, attributes) | Spec tables; stub columns; code map headings | 5, 6, 8 |
| `stubs/data/` exports | Scenario fixtures; display strings | 7 |
| `story-map.md` | Spec `## Story:` headings | 9 |
| One canonical `domain-model.md` for multi-layer | Per-system code maps built independently | 8 |

Each theme rediscovers the same anti-pattern: a downstream artifact is **typed by hand from memory** of an upstream artifact instead of **mechanically referencing or being generated from it**.

### C2 — "Validate before generate" / "gate, not cleanup" recurs

| Decision that needs a gate | Theme |
|---|---|
| Entry-point selection (Context vs Discovery) | 1 |
| Grill questions before generating output | 2 |
| Story-map ↔ graph ↔ spec alignment before writing scenarios | 9 |
| Domain.json existence before running scanners | 5, 6 |
| Placeholder absence after writing a templated diagram | 10 |

### C3 — Scanners alone are not sufficient

Every scanner-related correction admits that scanners check what they were designed for and miss what they weren't. The session journal repeatedly says: "AI MUST independently verify by reading the domain model" (Lines 225–227). This is the right answer locally but means the **AI workflow itself** needs explicit "now read X and compare Y" steps for each rule — otherwise the AI also relies on scanner output and inherits the same blind spots.

---

## What this list is for

This file is **diagnosis only**. Two follow-on files explore countermeasures against `c:\dev\abd-skills`:

1. `self-grill-and-countermeasures.md` — for each theme, ask hard questions; answer them by reading the skills/prompts/rules/scripts in `abd-skills`; propose specific countermeasures grounded in real file evidence.
2. `code-research/` — Pass 1 Explorer + Pass 2 Deep Dive against `abd-skills`, scoped to the themes above, surfacing where the codebase already has scaffolding to extend and where new mechanisms are needed.
