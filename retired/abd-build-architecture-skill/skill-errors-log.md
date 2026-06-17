# Skill errors log — abd-build-architecture-skill

### Code and test standards hard-coded to abd-clean-code / abd-acceptance-test-driven-development

- **Context:** Rule `inherit-clean-code-and-atdd-by-reference.md` (now renamed), Agent Instructions, Build steps, Validate, description blocks, ide-files
- **DO / DO NOT:** The generated skill must **inherit** the **project's chosen coding and testing standard** — whichever the project has agreed. `abd-clean-code` and `abd-acceptance-test-driven-development` are the defaults in an agilebydesign-skills-anchored project but are not hard requirements. Do **not** name them as if no other standard could apply.
- **Example (wrong):** Rule was named `inherit-clean-code-and-atdd-by-reference.md` and described inheriting specifically those two skills with no conditional phrasing. Agent Instructions and Validate sections stated these skills without "typically" or "when in scope" qualifiers.
- **Example (correct):** Rule renamed to `inherit-project-coding-and-testing-standards-by-reference.md`. Content now says "Whichever guides are in scope (in an agilebydesign-skills-anchored project these will typically be `abd-clean-code` and `abd-acceptance-test-driven-development`; in another project they may be a different skill, a style guide, or a corporate standard)". Build step 4 says "(typically abd-clean-code and abd-acceptance-test-driven-development when those are in scope)". Validate says "typically... when those are in scope". The ide-files say "When `abd-clean-code` and `abd-acceptance-test-driven-development` are in scope, those are the standards; otherwise name whichever guides the project uses."
- **Likely source:** prompt gap
- **Status:** confirmed

---

### External dependency on mern-technical-architecture

- **Context:** Agent Instructions step 1 in SKILL.md
- **DO / DO NOT:** The skill must be self-contained. Worked examples live **inside this skill** in `templates/generated-SKILL.md` — not as a relative link to a sibling skill's files.
- **Example (wrong):** Agent Instructions step 1 originally pointed to `../mern-technical-architecture/SKILL.md` as the closest worked example of the generated skill shape.
- **Example (correct):** Agent Instructions step 1 now reads: "The shape of the **target skill** this skill produces lives in [`templates/generated-SKILL.md`](templates/generated-SKILL.md). Read it once before generating a new skill so the shape stays consistent — that template is the worked example of what comes out, and it is self-contained inside this skill." Current SKILL.md has this correct text.
- **Likely source:** prompt gap
- **Status:** confirmed

---

### Instructions named specific skills to read, not what information to gather

- **Context:** Agent Instructions step 1 and Build steps 1–2 in SKILL.md
- **DO / DO NOT:** When an instruction step needs information, describe **what information** the agent must have in front of it, not **which sibling skill produces it**. Sibling skills are one possible source alongside ADRs, wiki pages, and decision docs.
- **Example (wrong):** Agent Instructions step 1 originally said: "Read the two input skills first. Open the output of **abd-architecture-description** for the layered description and **abd-architecture-mechanisms** for the list of mechanisms." — frames the work as fetching from specific sibling skills.
- **Example (correct):** Agent Instructions step 1 now says: "You need an **architecture-mechanism reference document** in front of you... It can be a fresh document, an ADR set, a wiki page that has already been used by humans on real code, or output produced by a sibling skill." — source-agnostic description of what information is needed. Current SKILL.md has this correct text.
- **Likely source:** prompt gap
- **Status:** confirmed

---

### "When to use" bullets described inter-skill pipeline plumbing

- **Context:** `When to use this skill` section
- **DO / DO NOT:** `When to use` bullets must describe **situations a practitioner actually faces** — drift, new projects, recurring review failures, onboarding pain — not pipeline plumbing like "you have output from skill X and need to feed it into skill Y".
- **Example (wrong):** Earlier draft had a bullet: "You have a finished `abd-architecture-specification` output and want to turn it into an active code-generator for the team."
- **Example (correct):** All five current bullets describe practitioner situations: "actual code keeps drifting", "standing up a new project", "code review for the same concerns", "multiple sibling stacks", "onboarding engineer can read the architecture document but still cannot produce a correct module". No sibling-skill names in When to use.
- **Likely source:** prompt gap
- **Status:** confirmed
