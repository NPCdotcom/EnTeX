# EnTeX — Agent Guide

> Kit: [.agents/README.md](.agents/README.md) · Tiers: [.agents/docs/CONTEXT_TIERS.md](.agents/docs/CONTEXT_TIERS.md)

## PM (IDE + external memory)

**No Subagents** · **No Hermes** · Memory: `.agents/memory/`

| Layer | Canonical |
|-------|-----------|
| L0 gate | `rules/secretary-gate` · `rules/no-subagents` |
| Every turn | `pm-turn-start` → `role-execute` → `pm-turn-end` · [PM_ROUTING.md](.agents/docs/PM_ROUTING.md) · `nav.yaml` |
| Loop2 | [PM_ROUTING.md](.agents/docs/PM_ROUTING.md) §Loop2 · `project-state.yaml` |

Roles: [CURSOR_ROLES.md](.agents/docs/CURSOR_ROLES.md) · Catalog: `skills/role-skill-catalog`

User chat: **Japanese** · Kit canon: **English** — [LANGUAGE_POLICY.md](.agents/docs/LANGUAGE_POLICY.md)

---

## Project

| Field | Value |
|-------|-------|
| Name | **EnTeX** |
| Description | Collaborative project (GitHub). Docs, schemas, and design shared in-repo. |
| Stack | TBD · runtime target: **WSL Ubuntu** |
| Members | NPC (`NPCdotcom`) · Aster (`astel_isk`) |

## Stack docs

| Topic | Link |
|-------|------|
| Language / runtime | TBD (WSL Ubuntu) |
| Framework | TBD |
| Style | TBD |

## Lifecycle

[PROJECT_LIFECYCLE.md](docs/PROJECT_LIFECYCLE.md) · `docs/project-state.yaml` · `.agents/memory/index.yaml`

## Shared paths

| Path | Purpose |
|------|---------|
| `docs/` | Requirements, design, ADR, glossary |
| `schemas/` | Shared schemas |
| `design/` | Design artifacts (non-doc) |
| `.agents/` | Shared agent kit (skills, rules, plans, memory scaffolding) |

## Principles

- Deterministic boundaries; share docs/schemas/design via git
- Agent kit assets are **tracked** (not gitignored) for collaborator sync
- Application secrets and generated runtimes stay local
