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
| Description | Form input → fixed-format PDF via LaTeX, for people who do not write TeX. Charter: [docs/design/product/charter.md](docs/design/product/charter.md) |
| Stack | Python 3.12+ · FastAPI · pydantic · Jinja2 · Typer · LuaLaTeX+luatexja (container only) · React (later) |
| Dev env | WSL2 Ubuntu + Docker single image `entex-dev` · clone under WSL FS (`~/EnTeX`), not `/mnt/c` |
| Members | NPC (`NPCdotcom`) · Aster (`astel_isk`) |

## Stack docs

| Topic | Link |
|-------|------|
| Language / runtime | Python 3.13 in image (`python:3.13-slim`) · `pyproject.toml` · run TeX-dependent code via `make docker-*` |
| Framework | FastAPI (API, roadmap step 2) · Typer CLI (`src/entex/cli.py`, step 1) · Jinja2 → `.tex` · latexmk `-lualatex` |
| Style | Ruff (`line-length 100`, `E F I B UP`) · LF endings (`.gitattributes`) · `.editorconfig` |

## Design invariants (from charter)

- `renderer` must not know where the IR came from (`data-import` stays separable).
- Adding a doc-package must require **zero** changes under `src/entex/` — judged when the 2nd doc-package lands.
- Users never see TeX, including error logs.
- "テンプレート" = the `.tex.j2` file only; the whole bundle is a "パッケージ".

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
