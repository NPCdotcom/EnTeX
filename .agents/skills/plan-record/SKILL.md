---
name: plan-record
description: Create implementation plans under .agents/plans after design gates and user confirmation. Use when slicing work into Do units—not for writing specs.
---

# Plan Record

**Role**: `plan_slicer` · **P4**  
**Format**: [`../lib-doc-frontmatter/SKILL.md`](../lib-doc-frontmatter/SKILL.md)

## Before write

**Blockers & prerequisites**: [`references/blockers-and-prerequisites.md`](references/blockers-and-prerequisites.md)

## Write steps

1. Choose path by `scope_level` — [`references/plan-paths-and-scope.md`](references/plan-paths-and-scope.md)
2. Copy [plans/_template.md](../../plans/_template.md); fill Scope hierarchy + Goal
3. Set `related_design`, `related_requirements`, `parent_hierarchy`
4. Agent recommendations + `>` user thinking
5. Index row: [`assets/plans-readme-row-template.md`](assets/plans-readme-row-template.md) → update [plans/README.md](../../plans/README.md)

Do not write `docs/design/` or `docs/requirements/` — **design-record**.
