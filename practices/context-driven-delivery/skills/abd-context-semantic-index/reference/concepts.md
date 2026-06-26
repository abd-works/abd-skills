# Semantic Context Chunker — Core Concepts

## What this skill does

Engagements accumulate context from many places — requirements documents, code repositories, design files, meeting notes, technical specs — and nobody knows what they actually have until someone reads it all. This skill scans the full corpus, tags every piece by the kind of context it provides — Story, Domain, Architecture, UX — and produces a coverage index so teams and agents know what evidence exists and where the gaps are, before any deeper analysis begins.

## Context index

The primary output is **tagged, chunked content** — every piece of source material broken into retrieval-sized segments and labelled by the kind of context it provides. The **context index** is the companion report that shows what you ended up with: "31 pieces of domain context, 23 story, 12 architecture, 8 UX — and here is exactly where each one lives." The chunks feed downstream retrieval; the index tells you what you have and where the gaps are.

## Four views

Every piece of source content provides context for at least one of four views:

- **Story** — what users and systems do: interactions, behaviors, processes, journeys, acceptance criteria, scenarios, flows.
- **Domain** — what the system knows and enforces: business vocabulary, data structures, rules, invariants, entity relationships, state transitions.
- **Architecture** — what the system is made of: components, platforms, technology choices, deployment, integration points, cross-cutting concerns, patterns, non-functional targets.
- **UX** — what the user sees and touches: screens, layouts, navigation, controls, wireframes, mockups, accessibility.

A single chunk can inform **multiple views** — for example, a paragraph describing an order submission form touches both Story (the user journey) and UX (the form layout).

## Hierarchical tags

Each view has a small set of tags that locate content at a **broad orientation level** — enough to know what area it belongs to, not enough to constitute full modeling. Story tags identify capability areas (epics) and actors, not individual stories. Domain tags identify modules and key abstractions, not every term and relationship. Architecture tags identify platforms, components, and mechanism types. UX tags identify screens and regions. The full vocabulary lives in **`references/four-view-taxonomy.md`**. Deeper structuring — decomposing epics into stories, extracting domain terms, mapping component interactions, specifying UI controls — is what downstream analysis is for, not this tagging pass.

## Chunking (when needed)

Most files are tagged as-is. When a file is large enough that it covers multiple topics (roughly over 1,500 characters), it gets split into 1–2 page segments so each piece can be tagged independently. Smaller files pass through intact — they still receive view tags but are not subdivided. The chunking is a means to accurate tagging, not the point of the skill.

## Coverage report

After chunking and tagging, the skill produces a report that groups every chunk by view, then by hierarchy level. This makes gaps visible: if the Story view shows no chunks under a known epic, the source corpus is missing behavioral content for that area. The report also lists pass-through files and any chunks that could not be tagged.
