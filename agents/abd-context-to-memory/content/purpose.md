Orchestrate **convert → chunk → embed → search** by coordinating this agent's skills. Decide **when** each stage runs, whether to use a **strategy pass** (review `context_chunking_spec.yaml` before chunk + embed) or **straight-through**, and hold cross-stage quality (real headings before chunking, sane splits after chunking).

Per-stage procedures: **`skills/abd-*/SKILL.md`** and each skill's **`references/`**.
