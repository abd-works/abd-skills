
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

1. The **skill** states which rule docs apply, which scanner names or CLI commands to run, what “green” looks like, and retry/repair behavior.
2. **agile_bots** still runs validators and scanners.
3. **`execute_using_rules`** (or equivalent) documents the loop in MD and **executes through the CLI**—not a second implementation in prose only.

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
        - use C:\dev\agilebydesign-skills\skills\workspace_skill to check, set, get

    - context_tracker NEW > determines context sources
        - default is <workspace>/context/* then  *context*.*
        - can be added to chat ask if cant find; track
        - create simple context_tracker skill to set and get list oif files and or folders
    - track_task > track stage of progress
        - C:\dev\agilebydesign-skills\skills\track_task


abd-delivery-lead own:
- flow definition, stage order, stage meanings, stage outcomes
- handoff rules between stages
- creating abd-team-member agents and assigning them a stage in the flow and associated skills
- cross phase validation ant interaction across builder agents, 


--abd-team-member --
- the abd-delivery-lead instantiates abd-team-member agents who all have the job to progressively add generated context into a more structured form following the Agile by design delivery approach. 

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
    - track that steps > C:\dev\agilebydesign-skills\skills\track_task 
- load skill context > eg make sure to folllow the directgions of the relevant abd-story-practice skll, if more than one look aty both and orchestrate ptractoice skills

2 - Build and Validate
- execution-using-rules > 
    - make sure relevant abd-story-practice skll (eg stroy mapping) has the latest rules 
    - generate output (graph and template) using rules from abd-story-practice skll (eg stroy mapping)
    - validate AI and scanner using rules/scanners from abd-story-practice sklls (eg stroy mapping)
    - work with human in loop review logging mistakes and corrections
    C:\dev\agilebydesign-skills\skills\execute_using_rules
    - building the Story graph
        path <workspace>
        bot story_bot
        story_graph.create_epic name:"My Product"
        story_graph."My Product".create_sub_epic name:"Onboarding"
        story_graph."My Product"."Onboarding".create_story name:"User signs up"

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

- each rulke may have 1 scanner ; scanners use code to detect vilations

RENDERING


- instructions to call CLI to render drawio diagram for this skill
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\render\render_story_map_outline_drawio.json

SYNCHRONIZER output back from drawio back to json
C:\dev\agile_bots\bots\story_bot\behaviors\shape\content\synchronize




- render the Story graph
shape.render.renderDiagram
path <workspace>
bot story_bot

--> C:\dev\agilebydesign-skills\skills\execute_using_rules



C:\dev\agile_bots\src\scanners



abd-team-menbers use the

buid using template to json from skill phase

render to markdown based on templartes from phase skill

val;idate using rules retry or repair logic







