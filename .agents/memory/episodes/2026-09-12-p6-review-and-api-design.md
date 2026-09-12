---
id: 2026-09-12-p6-review-and-api-design
date: 2026-09-12
scope: project
tags: [review, P6, api, P3, H4, pipeline, feature/npc]
---

# Episode: P6 review of PR #8 + P3 design for API (roadmap step 2)

## Input

User accepted the proposed order「推奨案（A: P6 review → B: API P3 design incl. C: shared pipeline function）」and specified the branch name `feature/npc` (overrides both the cloud-agent `cursor/…-172b` template and AGENTS.md's `issue/owner/topic`; hooks are not active in this environment so nothing blocked it).

## Done

- **P6 `review-conduct`** on `main@7955490` (PR #8 merged): `docs/reviews/2026-09-12-renderer-cli-p6-review.md`.
  - RTM FR1–FR8 / NFR1–2 ↔ renderer.md ↔ plan ACs ↔ tests with file:line. All pass. CI run 34665860832 (incl. Docker tex job with pytest) success; local `ruff` + 126 pytest pass.
  - Verdict **pass**. Warnings: **W1** JSON file stem flows unsanitised into the latexmk job name (`-dash.json`, `pct%hash#.json` → exit 2 with the generic message; reproduced on host). **W2** missing `template.tex.j2` → `RenderError`/exit 2 although plan says package defects are exit 3; `packages.py` docstring claims an existence check that `load_package()` does not do.
  - Suggestions: S1 renderer.md IF table drifted from implementation; S2 `pattern` uses `re.search`; S3 `TEXINPUTS` trailing separator; S4 the 3-step pipeline lives in `cli.py`.
  - Check rows added to both plans; renderer.md「次」ticked; `docs/project-state.yaml` → P6, `gate_status.current: pending`, proposal = Act items + API P3 gate.
- **P3 `design-record`** `docs/design/programs/api.md` (H4, `status: draft`):
  - `entex.pipeline.render_ir()` / `prepare()` shared by CLI and API; job-name rule owned by pipeline (fixes W1); W2 fixed in `load_package()`.
  - HTTP: `POST /v1/render` → `application/pdf`; `GET /v1/health`; optional `GET /v1/doc-types*`. Errors as RFC 9457 Problem Details (`application/problem+json`, Japanese `detail`, `issues[]` for `IRValidationError`); 400/422/500/503/413 mapping; FastAPI default 422 handler overridden.
  - Execution: sync `def` handlers (Starlette threadpool), `BoundedSemaphore`, per-request temp dir, PDF returned as bytes, latexmk log → server logging only.
  - Terminology alignment recorded (RFC 9457, RFC 9110 400/422, RFC 6266/8187 `filename*`, FastAPI async docs, Starlette threadpool).
  - P4 split proposal: `pipeline-and-cli` (incl. W1/W2/S1) then `api-render`.
- Indexes: `docs/README.md`, `schemas/README.md` pointer.

## Decisions

- Review verdict pass; W1/W2 are **not** fixed in this PR (review must not drive-by refactor); they are folded into the proposed `pipeline-and-cli` plan.
- API requirements kept inside api.md §1 (no separate 要件.md) — flagged as Open for the user.

## Open / risks

- `feature/npc` violates AGENTS.md branch rule and the repo's `pre-push` hook (`^[0-9]+/(aster|npc)/…`); the user's local hook would reject pushing this name. Chosen explicitly by the user.
- `pyproject.toml` pins `pydantic>=2.7` but current FastAPI needs `>=2.9` — align in `api-render`.
- Layout UAT still blocked on the real Word form.

## Next

- User: Go on api.md (→ `agreed`) and on the P4 split → `plan-record` ×2.
- Post `@coderabbitai review` on the PR.
