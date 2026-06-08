# Rule: Many-to-many signals a new concept

**Scanner:** Manual review

A passing model introduces a linking concept when two classes have a many-to-many relationship. The linker carries the relationship state. A failing model embeds direct many-to-many associations between two classes without a linking concept.

## DO

An Agent can have many Skills, and a Skill can be held by many Agents. Introduce a linking concept:

```markdown
### **AgentCapability**

AgentCapability(Agent, Skill, ProficiencyLevel)
------
agent: Agent
skill: Skill
proficiency: ProficiencyLevel
	Invariant: proficiency must be assessed before assignment
----
upgrade(ProficiencyLevel): AgentCapability
```

The relationship state (proficiency, assessment date) lives on the linker.

## DO NOT

Direct many-to-many without a linker:

```markdown
### **Agent**

Agent(AgentName)
------
skills: Skill        ← many skills, but where does proficiency live?
----
addSkill(Skill): Agent

### **Skill**

Skill(SkillName)
------
agents: Agent        ← many agents, mirroring the other side
```

This hides relationship state and creates a modeling smell. Where does proficiency go? Who owns it?

**Source:** Engagement convention (domain-model skill).
