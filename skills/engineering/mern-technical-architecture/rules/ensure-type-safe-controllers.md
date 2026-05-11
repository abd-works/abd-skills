---
scanner: type_safety_scanner.py
---

# Rule: Ensure Type-Safe Controllers

Controllers in the `server/` tier must compile without implicit `any` types or missing property errors. When controllers access extended Express `Request` properties (e.g., `req.user`, `req.session`), they must include the necessary type declarations.

## Express Type Augmentation

When a controller accesses properties not in the base Express `Request` type, include a **global type augmentation** at the top of the controller file:

```typescript
// packages/todo-lists/server/todoLists.controller.ts

import { Request, Response } from 'express';

declare global {
  namespace Express {
    interface Request {
      user?: { id: string };
    }
  }
}
```

This ensures `req.user` is typed correctly and `tsc --noEmit` passes without errors.

## Lambda Parameter Types

When `strict` or `noImplicitAny` is enabled in `tsconfig.json`, all callback parameters must have explicit types. Use the domain types from `shared/`:

```typescript
// CORRECT — explicit type from shared domain
import { Task } from '@taskflow/todo-lists-shared';

const tasks = dto.tasks.map((t: TaskDTO) => Task.create({ ... }));
todoList.tasks.map((task: Task) => ({ ... }));

// WRONG — implicit any parameter
const tasks = dto.tasks.map(t => Task.create({ ... }));
```

## DO

- Include `declare global { namespace Express { ... } }` when accessing `req.user`, `req.session`, or any custom middleware-injected property.
- Type all lambda/callback parameters explicitly when `noImplicitAny` or `strict` is enabled.
- Place the type augmentation in the controller file that uses it (or in a shared `types.d.ts`).
- Use domain types from `shared/` for parameters rather than `any`.

## DON'T

- Access `req.user` or other extended properties without a type declaration — this causes TS2339.
- Leave callback parameters untyped under `strict` mode — this causes TS7006.
- Use `(req as any).user` to bypass type checking — augment the type instead.
- Suppress errors with `// @ts-ignore` instead of providing proper types.
