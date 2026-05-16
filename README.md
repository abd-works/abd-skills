# Agile by Design Practice Skills

Reusable agent skills from [Agile by Design](https://agilebydesign.com), covering everything from story mapping to clean code.


 PHASE ────────────  IDEATION                          DISCOVERY
                     ──────────────────────────────    ──────────────────────────────────────────────
 Story-Driven        abd-story-mapping                 abd-story-mapping (complete)
 Delivery            (outline / skeleton mode)
                     Rough story skeleton;             Full actor → epic → feature → story map;
                     actors, epic headings only        ~80% of scope; shared cross-team narrative



 Domain-Driven       abd-module-partition              abd-domain-terms
 Design
                     Bounded context /                 Canonical domain vocabulary:
                     module boundaries                 things, state, actions, rules

 UX                  —                                 —

 Engineering         —                                 —

 ←─── SDD / DDD: choose order or run in parallel — each must always reflect the other ──────────────►
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ▶ THIN SLICING  (abd-thin-slicing)  — cross-cutting; not owned by any single track or phase
   Groups stories from the map into vertical delivery slices that cross all layers;
   spine (min. viable) first; subsequent slices ordered by value / risk / learning.
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


 PHASE ────────────  EXPLORATION                       SCENARIOS                 ATDD                  ENGINEERING
                     ──────────────────────────────    ──────────────────────    ──────────────────    ──────────────────
 Story-Driven        abd-acceptance-criteria           abd-specification-        abd-atdd              —
 Delivery                                              by-example
                     WHEN / THEN / AND / BUT;          Given / When / Then       Write tests RED
                     behavioral lang, per story        with concrete domain      first; impl makes
                     Bridges story intent to           examples; living          them GREEN
                     testable expectations             documentation

 Domain-Driven       abd-ubiquitous-language           abd-crc                   abd-object-model      
 Design                                                                                                 
                     Ubiquitous language               Class / Responsibility    Object model          
                     aligned to story map;             / Collaborator cards;     defines structure     
                     domain terms consistent           responsibilities,         and collaborations    
                     across AC                         collaborators per story

 UX                  —                                 —                         —                     —

 Engineering         —                                 —                         —                     —
 

 ←─── SDD / DDD: choose order or run in parallel — each must always reflect the other ──────────────►
## Skills

### [abd-story-mapping](skills/abd-story-mapping/SKILL.md)

Build Patton-style story maps: epics, sub-epics, stories, verb–noun naming, and actors via story_type.
Outputs `story-map.md` and `story-map.txt` templates with identical tree coverage.

### [abd-thin-slicing](skills/abd-thin-slicing/SKILL.md)

Produce thin-sliced delivery increments: vertical MVIs, spine vs optional paths, and marketable increment names.
Writes `thin-slicing.md` and `thin-slicing.txt` from a story map with full increment and story coverage.

### [abd-acceptance-criteria](skills/abd-acceptance-criteria/SKILL.md)

Write exploration-phase acceptance criteria for story-graph.json using WHEN/THEN/AND/BUT behavioral language.
Ships Markdown rules and Python scanners for mechanical checks alongside human review.

### [abd-specification-by-example](skills/abd-specification-by-example/SKILL.md)

Produce concrete Given/When/Then scenarios with real domain values, bold concept names, and italic values.
Supports plain scenarios (inline values) and outline format (shared steps, multiple data rows).

### [abd-acceptance-test-driven-development](skills/abd-acceptance-test-driven-development/SKILL.md)

Write tests first, then drive code to pass them. Creates executable Given-When-Then test files from behavioral context—specs, AC, stories, or rough descriptions.

### [abd-clean-code](skills/abd-clean-code/SKILL.md)

Write production code using domain language, clean functions, explicit dependencies, and observable design.
Covers single-responsibility, intention-revealing names, guard-clause flow, domain exceptions, and DRY structure.

---
# Helper Skills

Install  any / each of these to make youre skills more robust

### [execute-skill-using-skills-rules](skills/execute-skill-using-skills-rules/SKILL.md)

Run codescanners when validating output from skills, and enforce quality steps.
Enable correction-improvement log when fixing ai mistakes.

### [Workspace](guidance/workspace/README.md)

Engagement root **`skill-config.json` → `active_skill_workspace`** — guided by **`guidance/workspace/`** (rule + **`/workspace`** command + scripts), not a packaged skill.

### [track_task](skills/track_task/SKILL.md)

Track multiple-step skills or multi-skill workflows you create with markdown checkboxes for skill or agent-pipeline phases, per-phase steps, or ad-hoc lists.
Stored under the engagement workspace.


## Install

copy to `<your workspace>~/.github/skills/`


