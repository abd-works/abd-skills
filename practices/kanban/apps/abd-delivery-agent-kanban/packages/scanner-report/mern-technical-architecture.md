# Scanner Report — mern-technical-architecture

**Workspace:** packages
**Date:** 2026-06-04 23:13:18

---

## Scanner Execution Status

### 🟨 Overall Status: GOOD - Minor Issues

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 12 | Scanners ran without errors |
| 🟩 Clean Rules | 11 | No violations found |
| 🟥 Rules with Errors | 1 | Found 6 error violation(s) |

**Total Rules:** 12
- **Rules with Scanners:** 12
  - 🟩 **Executed Successfully:** 12

---

### Scanner Results

| Status | Rule | Violations |
|--------|------|------------|
| 🟥 ERRORS | Test Scripts Scanner | 6 |
| 🟩 CLEAN | Dependency Declarations Scanner | 0 |
| 🟩 CLEAN | Domain Structure Scanner | 0 |
| 🟩 CLEAN | Entity Behavior Scanner | 0 |
| 🟩 CLEAN | Interface Implementation Scanner | 0 |
| 🟩 CLEAN | Layer Purity Scanner | 0 |
| 🟩 CLEAN | Package Names Scanner | 0 |
| 🟩 CLEAN | Share Domain Logic Scanner | 0 |
| 🟩 CLEAN | Test Isolation Scanner | 0 |
| 🟩 CLEAN | Test Structure Scanner | 0 |
| 🟩 CLEAN | Type Safety Scanner | 0 |
| 🟩 CLEAN | Domain Language Scanner | 0 |

---

## Violations

### 🟥 Test Scripts Scanner — 6 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\sandbox\.cursor\skills\mern-technical-architecture\packages\scripts` | Missing scripts/test.sh. Run Vitest unit/component tests. Create it at the workspace root so tests are runnable without memorising npm script names. | error |
| 2 | `C:\dev\sandbox\.cursor\skills\mern-technical-architecture\packages\scripts` | Missing scripts/test.ps1. Run Vitest unit/component tests (Windows). Create it at the workspace root so tests are runnable without memorising npm script names. | error |
| 3 | `C:\dev\sandbox\.cursor\skills\mern-technical-architecture\packages\scripts` | Missing scripts/test-e2e.sh. Run Playwright E2E tests. Create it at the workspace root so tests are runnable without memorising npm script names. | error |
| 4 | `C:\dev\sandbox\.cursor\skills\mern-technical-architecture\packages\scripts` | Missing scripts/test-e2e.ps1. Run Playwright E2E tests (Windows). Create it at the workspace root so tests are runnable without memorising npm script names. | error |
| 5 | `C:\dev\sandbox\.cursor\skills\mern-technical-architecture\packages` | playwright.config.ts is missing. Without it, Playwright picks up Vitest test files and fails with ESM/CJS errors. Create playwright.config.ts with testMatch: '**/*_e2e.spec.ts'. | error |
| 6 | `C:\dev\sandbox\.cursor\skills\mern-technical-architecture\packages` | vitest.config.ts is missing. Without it, Vitest picks up *_e2e.spec.ts Playwright files and fails. Create vitest.config.ts with include patterns for *_server.test.ts and *_client.test.tsx only. | error |
