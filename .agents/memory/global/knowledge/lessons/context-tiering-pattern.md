---
id: lesson-context-tiering
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, refresh, context, tiers, r-3, cursor]
sources:
  - learning/product-dev/notes/refresh/r-03-context-tiers.md
  - learning/product-dev/notes/refresh/ADR-001-context-tiering.md
  - docs/CONTEXT_TIERS.md
  - learning/product-dev/notes/evaluations/r-07-b7-testprojecta-refresh.md
promoted_at: 2026-06-22
---

# Lesson — context tiering (L0–L3)

## Principle

Kit context compression uses **four load tiers**, not duplicate policy prose. **L0** = 3 always rules + short AGENTS entry (~48 lines measured). **L1** = `_chains/memory-turn` + `_chains/secretary-turn` + thin skills. **L2** = phase skills · stewardship rules. **L3** = one deep doc per turn (`PM_ROUTING`, `AIDLC_KIT_MAP`, etc.).

## Facts

- R-3 refresh (Track R): removed `project-leadership.mdc` · deprecated `SKILLS_RULES_BY_PHASE` stub
- Machine canon **English** · project templates **Japanese** (`LANGUAGE_POLICY.md`)
- Loop detail canonical: **`PM_ROUTING.md` only** — gate/MANDATORY are indexes
- B7 TestProjectA: pytest 2/2 pass · junction kit · nav reanchor cleared

## Decisions

- Do not duplicate JP+EN procedural canon
- Skill count stays 48 — thin `SKILL.md` + chains, not mass delete
- `evaluate-reference` is L2 (not every turn)

## Anti-patterns

- Re-adding full loop text to AGENTS.md or stewardship rules
- Loading L3 docs every turn
- Second Role×Skill table outside `full-catalog.md`

## Recall

R-3 refresh · CONTEXT_TIERS · _chains · PM_ROUTING English · L0 budget
