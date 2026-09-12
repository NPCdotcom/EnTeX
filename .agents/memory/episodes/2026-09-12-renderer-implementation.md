---
id: 2026-09-12-renderer-implementation
date: 2026-09-12
scope: project
tags: [renderer, P4, P5, H4, H5, cli, circle-monthly-report]
---

# Episode: plan-record + implement renderer (roadmap step 1)

## Input

User (cloud agent session): "このプロジェクトの内容を把握したうえで、P3の設計に従って実装に入ってください。" — treated as the explicit re-authorization the previous session's handoff required (nav/next_actions, project-state conditions).

## Done

- Pulled `origin/main` (local snapshot was behind: renderer.md / 要件.md / 要求.md had landed).
- **P4** `plan-record`: `.agents/plans/algorithms/ir-validate-and-derive.md` (H5, FR1–4) and `.agents/plans/programs/render-and-cli.md` (H4, FR5–8, NFR1–2), both `status: agreed` citing the user instruction as PM confirmation. Index row in `.agents/plans/README.md`. `docs/project-state.yaml` → P5, `allowed_actions` unlocked.
- **P5** implementation (5 modules per renderer.md, plus two helper modules):
  - `src/entex/errors.py` — `EnTeXError.user_message` hierarchy: `PackageError`, `EnvelopeError`, `IRValidationError(issues)`, `DerivationError`, `RenderError(log_path, detail)`.
  - `src/entex/packages.py` — locate/load `packages/<slug>/` (slug validated before path join), `default_packages_dir()`.
  - `src/entex/ir/schema.py` — pydantic models for `schema.json` (11 types, attributes, `Expr`); expr reference check (declared-before, numeric, optional→default required) rejects forward refs / cycles at package load.
  - `src/entex/ir/validate.py` — per-type walker; Japanese messages with `label`, row/item positions; NFC; defaults; unknown-key suggestion (difflib).
  - `src/entex/ir/loader.py` — envelope → package → content; `Envelope` pydantic model is the source of `schemas/ir/envelope.schema.json` (sync test).
  - `src/entex/ir/derive.py` — sum/where, count, add, sub in declaration order.
  - `src/entex/tex/escape.py` — single-pass `str.translate`; `escape_content` touches only `text`/`rich_text`.
  - `src/entex/renderer.py` — Jinja2 with `\VAR{}` `\BLOCK{}` `%#`, `StrictUndefined`, filters `group_digits`/`ja_month`/`ja_date`; context converted to `SimpleNamespace` (avoids Jinja `dict.items` trap); `build_tex` escapes internally; `render` runs `latexmk -lualatex` with `TEXINPUTS` including `style/`, raw log only to `out/.../latexmk.log`.
  - `src/entex/cli.py` — `entex render <json> [--out] [--packages-dir] [--tex-only]`; exit 0/1/2/3.
  - `packages/circle-monthly-report/template.tex.j2` + `style/circle-monthly-report.sty` (provisional layout: ltjsarticle A4, tabularx+booktabs, △ for negative money).
- Tests: 126 with TeX / 115 + 11 skipped without. FR7 tested on host via a fake `latexmk` on PATH. Real PDFs rendered and eyeballed (installed the Dockerfile's apt packages on the host since Docker was unavailable).
- Docs: README (CLI), packages READMEs, schemas/README, docs/README, renderer.md Open items → decisions.

## Decisions (recorded in plans)

- Content validation = hand-written walker over the schema (案2), pydantic only for static models. Reason: Japanese label-based messages and stable behaviour vs pydantic error-type strings.
- Escaping lives inside `build_tex` so no caller can bypass it.
- `RenderError` stays one generic message; detail/log server-side.

## Open / risks

- Branch name is `cursor/renderer-cli-render-172b` (cloud-agent template) — does not match AGENTS.md's `issue/owner/topic`; hooks were not enabled locally so nothing blocked it. Decide at merge.
- `make docker-test` / `make tex-smoke` not run (no Docker here); CI tex job covers it.
- NFR1 test in CI: measures the warm second run; threshold overridable via `ENTEX_NFR1_SECONDS`.
- Real report form still not obtained; all layout is provisional inside the package.

## Next

- P6 `review-conduct` on the PR; then charter §11 step 2 (API).
