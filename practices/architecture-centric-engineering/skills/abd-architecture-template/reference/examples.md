# Architecture Template (Reference Document) — Examples

## Per-mechanism mode (4+ mechanisms)

```
# <ArchitectureName> Architecture Reference

## Table of Contents
- [Overview](#overview)
- [Architecture Layers](#architecture-layers)
- [Mechanism: Error Handling](#mechanism-error-handling)
- [Mechanism: Caching](#mechanism-caching)
- [Mechanism: Persistence](#mechanism-persistence)
- [Testing Architecture](#testing-architecture)
- [References](#references)

## Overview
One paragraph: name the architecture, the guiding principles, the mechanisms covered.

## Architecture Layers
Reuse the layer block from the architecture's source of truth verbatim.

## Mechanism: Error Handling
### Principles & Patterns
- Principle: errors raised at the boundary, never swallowed.
- Pattern: Result<T, DomainException>; controller maps to HTTP status.
### File Structure
packages/<domain>/shared/Errors.ts
packages/<domain>/server/error-mapper.ts
### Participants  (class diagram)
[Mermaid classDiagram]
### Flow  (sequence diagram)
[Mermaid sequenceDiagram]
### Walkthrough Example
1. Repository fails to parse a Mongo doc...
2. Service catches with .mapErr(...)
3. Controller maps DomainException -> 422
   (code sample follows the project's coding standard)
   (test sample follows the project's testing standard)
### Testing the mechanism
- Domain tier: every application-service method has one failure scenario.

## Mechanism: Caching
... same shape ...
```

---

## The shape of a good mechanism section

```
## Mechanism: <Name>

### Principles & Patterns
- Principle: <one sentence the architecture refuses to break>
- Pattern: <named, repeatable shape that satisfies the principle>

### File Structure
<fenced folder tree showing where this mechanism's code lives>

### Participants
<Mermaid classDiagram OR a Markdown table>
| Class / Module | Layer | Responsibility | Collaborators |

### Flow
<Mermaid sequenceDiagram for ONE representative scenario>

### Walkthrough Example
1. <step naming participant>
2. <step naming participant>
...
```code (follows the project's coding standard)```
```test (follows the project's testing standard)```

### Testing the mechanism
- Tier: <project's tier name>
- Doubles / helpers: <which test doubles verify it>
```
