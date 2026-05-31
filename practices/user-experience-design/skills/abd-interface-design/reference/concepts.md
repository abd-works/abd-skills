# abd-interface-design — Concepts

## What is an interface implementation

A screen implementation under this skill is:

- **Functional**: every affordance does what its AC say it should do. Errors render, validations run, transitions to other screens fire when their triggers fire.
- **Production-grade**: real code in the chosen framework (React, Vue, WPF, etc.), structured the way the host project structures other features, with the project's lint, format, and test conventions.
- **Faithful to upstream**: the regions, affordances, labels, AC, and visual decisions match the approved lo-fi and hi-fi. No new vocabulary, no new affordances, no new visual styles.
- **Accessible**: meets the host project's accessibility floor (typically WCAG 2.2 AA for web). Keyboard reachable, focus visible, labels associated with inputs, errors announced, colour-independent state cues.
- **Measurable**: the behaviours described by AC are covered by tests, and any performance constraints declared by the host project (frame budget, response time, payload size) are met.

It is not a redesign and it is not a refactor of unrelated code.

---

## Carry-over from upstream

The initial IA, lo-fi, and hi-fi are inputs. Their regions, affordances, labels, acceptance criteria, typography roles, colour roles, density, and spacing scale are settled. The implementation maps each of those into the chosen framework's primitives — it does not redecide them.

## Production-grade and functional

The code is not a "demo" or "shell". Every affordance on the screen does what its AC say it does. State management uses the project's existing patterns. Side effects are real or properly mocked at boundaries the project already has. The code passes the project's lint, format, and type-check gates without being silenced.

## Memorable differentiation

The committed aesthetic direction from the hi-fi survives into the running code: the typographic roles are real CSS variables, design tokens, or theme values; the colour roles are real values, not generic defaults; the density and spacing scale are real spacing tokens. The running screen looks like the mockup, not like an untouched component library.

## Accessibility in implementation

Implementation-level accessibility is concrete: each input has a programmatic label (`<label for>` or framework equivalent), focus order matches reading order, focus styles are visible (not removed by `outline: none` with no replacement), errors are programmatically associated with their inputs (`aria-describedby`), state is announced when it changes (`aria-live` where appropriate), and the entire screen is keyboard reachable.

## Performance constraints

If the host project declares performance constraints (initial paint, time-to-interactive, frame budget for animations, bundle size budget), the implementation meets them. If it does not declare them, the implementation does not regress whatever the project's current baseline is.

## Traceability — AC to test to running screen

Each acceptance criterion is implemented as a working behaviour and is covered by a test that asserts that behaviour, using the project's existing test framework. The test names reference the criterion (story title and clause number) so a reviewer can map each test back to the source AC.

---

## The shape of a good interface implementation

```
src/screens/game-directory-prompt/
  GameDirectoryPrompt.tsx           # the screen component
  GameDirectoryPrompt.styles.ts     # styles using project tokens
  validatePath.ts                   # logic for AC clauses
  __tests__/GameDirectoryPrompt.test.tsx
                                    # one test per AC clause, named:
                                    #   "Validate COH Game Directory — AC 1"
                                    #   "Prompt for Game Directory if Invalid — AC 3"
```

The running screen renders the regions and affordances from the hi-fi, uses the declared typography and colour roles via project tokens, satisfies every AC clause, and passes the project's lint / format / type-check / accessibility / performance gates.
