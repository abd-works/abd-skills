# Build Architecture Skill — Examples

## Generated skill folder structure

```
architecture-centric-engineering/skills/<arch-name>-technical-architecture/
├── SKILL.md                          # one section per layer + Build/Validate
├── inputs/
│   └── architecture-reference.md     # copied from abd-architecture-specification
├── templates/
│   ├── domain-module.template.txt    # the full folder tree the generated skill emits
│   └── domain-module/                # (optional) sub-templates per layer
├── rules/
│   ├── maintain-layer-purity.md      # from "Domain never imports infrastructure"
│   ├── implement-domain-entities-correctly.md
│   ├── handle-errors-at-boundary.md  # from Error Handling principle
│   ├── cache-via-side-car.md         # from Caching principle
│   ├── use-repository-for-persistence.md
│   ├── use-domain-language.md    # inherited from project's coding standard
│   └── test-story-driven.md          # inherited from project's testing standard
├── ide-files/
│   ├── <arch-name>-technical-architecture.mdc
│   ├── <arch-name>-technical-architecture.instructions.md
│   └── <arch-name>-technical-architecture.prompt.md
└── scanners/
    └── README.md                     # listed targets; populated as scanners are written
```

---

## Shape of a good generated skill

```
<arch>-technical-architecture/
├── SKILL.md
│   ├── Purpose                       (paragraph + bullet principles)
│   ├── When to use                   (5 triggers)
│   ├── Agent Instructions            (Read reference → Templates → Rules → Scanners → Verify)
│   ├── What is <Arch>?               (one-sentence positioning + 4 principles)
│   ├── Core concepts                 (Layers table + key abstractions)
│   ├── Example                       (one filled mini-module)
│   ├── The shape of a good module    (folder tree)
│   ├── Build                         (numbered steps; mechanism-by-mechanism)
│   ├── Validate                      (checklist)
│   └── bundled rules block
├── inputs/architecture-reference.md  (the contract; copied)
├── templates/                        (one .template.txt per language tier or per mechanism)
├── rules/                            (one per principle from the reference, plus inherited rules)
├── ide-files/                        (.mdc, .instructions.md, .prompt.md — body parity)
└── scanners/                         (per-language; optional; only referenced if present)
```
