
I want to convert agile\_bots to skill.md ; agent.md approach 


We need to build these agents and skills by porting existing C:\dev\agile_bots content and src code.

## Migration architecture (agents/skills in Markdown, agile_bots CLI unchanged)

### What migration means

- **From:** `behavior.json`, `bot_config.json`, and scattered JSON as the source of truth for *procedural* steps (what to do, required context, guardrails tied to `shape.build` / `shape.validate`, etc.).
- **To:** `AGENT.md` / `SKILL.md` (plus `content/`, `rules/`) as the source of truth for *instructions*. **agile_bots** stays the **mechanical** layer for **build, validate, render, sync, and scan** through the existing CLI.

### Layering (three buckets)

| Layer | Owns | Lives in |
|--------|------|----------|
| **Orchestration** | Stage order, handoffs, which team-member covers which stage, when to involve the human | `abd-delivery-lead` agent MD |
| **Common delivery mechanics** | Workspace, context roots, task tracking, generic CLI invocation pattern (`execute_using_rules`, future `render-output`, etc.) | Shared helper skills (`workspace_skill`, `track_task`, `context_tracker`, `execute_using_rules`, …) |
| **Practice + shape** | What good output *is* for that stage, templates, shape-specific validate/render notes | One practice skill per stage (e.g. `abd-story-mapping`) |

**Common vs shape-specific:** pull *common* flow from agile_bots **build → validate → render** at the level of *workflow*, not by copying action-specific JSON prose into skills. Put **behavior/action-shaped** specifics (story-mapping vocabulary, outline rules, etc.) in the **practice skill**.

### JSON vs Markdown (what moves where)

- **Keep JSON (or YAML) as data only**, not instructions: `story-graph.json`, template/schema snippets that tools consume, DrawIO/render config, etc.
- **Move to Markdown:** required context, key questions, definition of done, guardrails (e.g. under `guardrails/required_context/`), rule *text* → `<skill>/rules/*.md`. Scanners remain **code** in agile_bots (or a shared package), **invoked via CLI**, **referenced by name** from the skill.

**Minimal bot config** in agile_bots (e.g. default `WORKING_AREA`, bot identity) can remain so `cli_main.py` / MCP keep resolving the graph. Procedural steps do **not** need to stay in `behavior.json` as the spine.

### Validate and scan from instructions

1. The **practice skill** (e.g. `abd-story-mapping`) owns **`rules/*.md`**, bundled rule prose in **`SKILL.md`**, and **`scanners/*-scanner.py`** bound via rule frontmatter (`scanner:`).
2. **`execute_using_rules`** documents the loop and **runs it through the CLI**: AI pass on the deliverable **plus** mechanical scanners — see `skills/execute_using_rules/SKILL.md`.
3. **Scanner driver:** `python <execute_using_rules>/scripts/run_scanners.py --skill-root <path-to-practice-skill> --workspace <engagement-folder>`.
4. **Workspace graph path:** scanners load `story-graph.json` from `<workspace>/story-graph.json` or `<workspace>/docs/story/story-graph.json` (see `scanner_runner.load_workspace_graph_json`).
5. **Serialized graph lifecycle (no agile_bots required):** use **`story-graph-ops`** — create or edit `story-graph.json`, then validate with `story_graph_cli.py read --file <path>` and `PYTHONPATH` including `skills/story-graph-ops/scripts`. Do not treat hand-written JSON as done until that read passes.
6. **Green:** all configured scanners exit 0; fix violations and re-run. Log corrections per `execute_using_rules` correction process when rules are missed.

### Sequencing (implementation slices)

1. **Inventory** each `behavior.json` action: tag content as orchestration, common CLI flow, practice-specific, or data artifact.
2. **Draft** practice skill MD with sections: Setup / Build / Validate / Render / Sync—each ending with **exact CLI** steps already used today.
3. **Port** `required_context` and `key_questions` into MD; deprecate JSON copies after parity.
4. **Define** `abd-delivery-lead` agent: stages, which skill loads per stage, handoff checklist—without story_bot behavior IDs as the lifecycle spine.
5. **Reserve** JSON under skills for templates and machine configs; avoid new **procedural** JSON.

---

---abd-delivery-lead-----
@agilebydesign-skills/agents/abd-context-engine/agents/abd-delivery-lead 
- single agile-delivery agent as the controller for the lifecycle
- orchesration of delivery flow of work in its agent.md, use skills to help
- kick start delivery flowtake a shot att fiishing this plan

    - workspace-skill > agent determines workspace asks if not set
        - use agents/abd-context-engine/skills/workspace_skill to check, set, get

    - context_tracker NEW > determines context sources
        - default is <workspace>/context/* then  *context*.*
        - can be added to chat ask if cant find; track
        - create simple context_tracker skill to set and get list oif files and or folders
    - track_task > track stage of progress
        - agents/abd-context-engine/skills/track_task


abd-delivery-lead own:
- flow definition, stage order, stage meanings, stage outcomes
- handoff rules between stages
- creating abd-team-member agents and assigning them a stage in the flow and associated skills
- cross phase validation ant interaction across builder agents, 


--abd-team-member --
- the abd-delivery-lead instantiates abd-team-member agents who all have the job to progressively add generated context into a more structured form following the Agile by design delivery approach. 

**Mechanical stack for structured artifacts (e.g. discovery producing `story-graph.json`):** **`story-graph-ops`** (validate graph file) → **`execute_using_rules`** `run_scanners.py` with **`--skill-root`** = the stage’s **practice skill** (e.g. `abd-story-mapping`) and **`--workspace`** = engagement folder containing the graph. This is the correct approach when an abd-team-member is *not* inside agile_bots; agile_bots CLI remains an alternate path when the workspace is a bot.

*abd-team-member-agent* area instantiated for each stage in delivery flow 
- discovery
- prioritization
- exploration
- scenarios
- acceptance tests
- code

each team member agent is equipped with
- unique abd-story-practice(s) skill required to provide best practices on *what* to deliver using a practice that helps achieve outcome for stage of delivery of flow they are responsible for
    - discovery >  abd-story-mapping
    - prioritization > abd-thin-slicingload - exploration > abd-story-acceptance-criteria
    - scenarios >abd-spec-by-example
    - acceptance test creation > abd-acceptance-test-driven-development
    - develop > abd-clean-code

- the  team-member agents will use a set of *abd-team-member-helper-skills* > how to deliver in a consisten way across stages and skills

Source common flow instructions from C:\dev\agile_bots\base_actions\build, render, valdate flow of aciton NOT action specific instructions

team-member agents flow 
1 - Set Up
-------
- workspace-skill > get workspage as needed
- abd-context-tracker > find where the context sources are
- track tasks 
    - track that steps > agents/abd-context-engine/skills/track_task 
- load skill context > eg make sure to folllow the directgions of the relevant abd-story-practice skll, if more than one look aty both and orchestrate ptractoice skills

2 - Build and Validate
- **Practice skill** (e.g. `abd-story-mapping` for discovery) defines *what good looks like* — rules, templates, naming — in `SKILL.md` + `rules/`.
- **Build the artifact on disk:**
  - Prefer **`story-graph-ops`** for `story-graph.json`: produce JSON (generator script, careful edit, or import from `story_map`), then **`story_graph_cli.py read --file …`** so structure is valid before scanners run. Skill root: `skills/story-graph-ops`.
  - **Alternative** when working *inside* **agile_bots** with `story_bot`: use the existing bot/CLI story graph API (e.g. `story_graph.create_epic` …) if the engagement is wired to that workspace — same file format, different entry point.
- **`execute_using_rules`** (repo: `skills/execute_using_rules`) — scanner pass:
  - `python scripts/run_scanners.py --skill-root <practice-skill-dir> --workspace <engagement-folder>`
  - Example (discovery / story mapping): `--skill-root …/skills/abd-story-mapping --workspace …/your-project` (folder must contain `story-graph.json` or `docs/story/story-graph.json`).
- **AI pass + scanner pass** together: read bundled rules, judge the deliverable, then run `run_scanners.py`; iterate until both are acceptable; use corrections log when fixing mistakes.

3 - Render and Edit
- render-output NEW SKILL 
    - render from json to md; drawio
    - Human edits and makes changes
    - synch changes back to graph on save of rendered document or oncommand



Example: Discovery
Discovery definition (in abd-orchestration)  *was shape in story bot*
----------------------
- loads a stege in the flow for discovery  
    - it requires access to purpose of discovery, overview, definition of done, inputs, questions the builder asks itself to determine if done
    SEE
    - abd-delivery-lead bootstraps abd-team-member to be a discovery team member agent 

C:\dev\agile_bots\bots\story_bot\behaviors\shape\guardrails\required_context\key_questions.json
C:\dev\agile_bots\bots\story_bot\behaviors\shape\behavior.json 

C:\dev\agile_bots\bots\story_bot --> contains instructions / prompts/ content for agent and skills



Dicovery team member agent
-----
internally boot straps abd-helpers skill  --> how to generate COMMON ACROSS ALL builder agents (SEE ABOVE)
abd-delivery agent injects abd-story-mapping skill --> what to generate UNIQUE SET by team member


Story-mapping skill
--------------------
convert to skill md file ./ files()

instructions for build, validate, and render specifc to this skill , eg section in md per - keep focuses on what not build/ validatre/ render process that is in gnerator skill
C:\dev\agile_bots\bots\story_bot\bot_config.json

BUILDING
- details on how to story map;
C:\dev\agile_bots\bots\story_bot\behaviors\shape\behavior.json   --> what is a story map how to use story cli to read and write 
C:\dev\agilebydesign-skills\backup\abd-maps-models-specs\content\parts\library\story-map.md --> some good stroy map stuff ignoitre extra stuff and extra fileds stick to core SM epics, epics, stories, as , steps , acror

**Portable pipeline (abd-team-member / discovery without agile_bots runtime):**
- **`story-graph-ops`** (`skills/story-graph-ops`): mechanical lifecycle for `story-graph.json` — CLI `story_graph_cli.py` (`read`, `names`, `search`, `write`); always finish with **`read`** after writes.
- **`execute_using_rules`** + **`abd-story-mapping`**: `run_scanners.py --skill-root …/abd-story-mapping --workspace <folder with story-graph.json>`.
- Converting from Markdown/text story maps: generate JSON, validate with story-graph-ops, then run practice skill scanners.

-template for what a story graph looks like when built by this skill-template (json)
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\story_graph\story-graph-outline.json 

then immediately render templatges (sio use can look at it)

-template for when stroy graph rendered by this skill (we want our skills to have templates as well)
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\render\templates\story-map.md
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\render\templates\story-map.txt
- scripts to render output from json
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\render\templates\render_story_map_md.py
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\render\templates\render_story_map_txtx.py


- building the Story graph
path <workspace>
bot story_bot
story_graph.create_epic name:"My Product"
story_graph."My Product".create_sub_epic name:"Onboarding"
story_graph."My Product"."Onboarding".create_story name:"User signs up"

VALIDATING
each skill needs rules C:\dev\agile_bots\bots\story_bot\behaviors\shape\rules  --> move these to markdown in <Skill>/rules,  building skills will build all th skills into skill file

- each rule may have 1 scanner ; scanners use code to detect violations
- **Run scanners** via `execute_using_rules` `run_scanners.py` with `--skill-root` = that practice skill directory (not agile_bots). Scanners import **`story_map` / `story_scanner`** from **`story-graph-ops/scripts`** on `PYTHONPATH` (the driver sets this).

RENDERING


- instructions to call CLI to render drawio diagram for this skill
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\render\render_story_map_outline_drawio.json

SYNCHRONIZER output back from drawio back to json
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\synchronize




- render the Story graph
shape.render.renderDiagram
path <workspace>
bot story_bot

--> agents/abd-context-engine/skills/execute_using_rules



C:\dev\agile_bots\src\scanners



abd-team-menbers use the

buid using template to json from skill phase

render to markdown based on templartes from phase skill

val;idate using rules retry or repair logic







