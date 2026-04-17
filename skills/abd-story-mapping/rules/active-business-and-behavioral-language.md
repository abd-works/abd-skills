---
scanner: active-business-and-behavioral-language
---

# Rule: Active Business and Behavioral Language

**Scanner:** `scanners/active-business-and-behavioral-language-scanner.py` — **`ActiveBusinessAndBehavioralLanguageScanner`**


Use **active** business language focused on **user/system behavior**: clear action verbs, not technical implementation or passive constructions.

## DO

- Use **active voice** with business language and **base verb forms** (infinitive/imperative): e.g. `User --> submit order`, `System --> validate payment`, `Customer --> place order`, `Admin --> approve request`.
- Prefer **action verbs** that describe behavior: submit, view, validate, send, display, place, edit, create, load, save, invoke, process, generate, update — as fits the story.
- Prefer **user/system stories** over raw technical tasks. Rephrase technical wording into business behavior (e.g. `System --> store user data` rather than “set up database schema”). When technical work is required, use `story_type: technical` and keep it minimal.
- When technical stories are necessary, mark with **`story_type: technical`** and keep them focused.

## DON'T

- **Passive or vague:** not “Order is submitted” — use `User --> submit order`. Not “Payment gets validated” — use `System --> validate payment`.
- **Implementation/task language** as the main story: avoid “write code”, “create class”, “set up CI/CD”, “configure database” as the behavior — express **business outcome** instead where possible.
- **Development-task verbs** for primary stories: implement feature, create module, refactor code, fix bug, build system — unless framed as real behavioral outcomes with `story_type` as appropriate.
