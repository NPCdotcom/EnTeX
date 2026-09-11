---
id: 2026-09-12-dev-env-scaffold
date: 2026-09-12
scope: project
tags: [env, docker, tex, python, P0]
---

# Episode: dev environment scaffold after charter

## Input

Charter filled by NPC + Aster (案B: Web app, Python/FastAPI, LuaLaTeX+luatexja, WSL2+Docker single container; roadmap 1 CLI → 2 API → 3 second doc-type gate → 4 UI → 5 CSV).

## Done

- `pyproject.toml` (entex 0.0.1; fastapi/pydantic/jinja2/typer/uvicorn; dev: pytest/httpx/ruff; ruff excludes `.agents`)
- `src/entex/cli.py`: `entex version`, `entex doctor` (checks lualatex/latexmk/luatexja/ltjsarticle)
- `Dockerfile` (`python:3.13-slim` + texlive-luatex/lang-japanese/latex-recommended/fonts-recommended/latexmk/fonts-noto-cjk), `compose.yaml` (service `dev`, bind `.:/app`), `Makefile` (setup/test/lint/docker-*/tex-smoke)
- `tests/fixtures/smoke.tex` + `scripts/tex-smoke.sh`; `.gitattributes` LF policy; `.editorconfig`; `.dockerignore`; `.gitignore` TeX aux + `/out/`
- `packages/README.md`, `schemas/README.md` placeholders aligned with charter §8/§10
- README / AGENTS / project-state updated (gate proposal: Go)

## Verified

Inside image: doctor OK · pytest 2 passed · luatexja PDF 16194 bytes · ruff clean. Same from WSL clone `~/EnTeX` (HTTPS).

## Lessons

- Cursor Write tool emits CRLF on Windows → dash `set -eu` fails. Convert to LF before running under Linux; `.gitattributes` handles repo side.
- Container runs as root → `out/` files root-owned on WSL FS. Consider `user:` in compose later.

## Open

- P0 gate decision (user)
- WSL GitHub SSH key absent
