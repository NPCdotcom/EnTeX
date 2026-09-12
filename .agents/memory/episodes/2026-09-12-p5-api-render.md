---
id: 2026-09-12-p5-api-render
date: 2026-09-12
scope: project
tags: [implement, P5, H4, api, fastapi, rfc9457, feature/npc]
---

# Episode: P5 Do of plan `api-render` (roadmap step 2, second half)

## Input

User:「2で進みましょう。」— chose option 2 of my proposal: go straight to P5 of `api-render`, then run the P6 Check for `pipeline-and-cli` and `api-render` together. Same branch `feature/npc`. PR #10 turned out to be merged (02:47, merge commit) before this turn, so the new commits went into a new PR #12 (diff = 5 commits since merge-base 3c0e0b9).

## Done (TDD)

- **Red** `tests/test_api.py` covering AC1–AC5 (TestClient with lifespan; fake latexmk variants: failing / capturing `.tex` / sleeping), plus `tests/test_renderer.py::test_latexmk_timeout_is_a_render_timeout_error`.
- **Green**
  - `errors.RenderTimeoutError(RenderError)` with its own `GENERIC_MESSAGE`; `renderer.render()` raises it on `TimeoutExpired`.
  - `src/entex/api/settings.py`: frozen `Settings` (+ validation), `from_env()` reading api.md §3.5 vars.
  - `src/entex/api/problems.py`: `Problem`/`ProblemIssue` (pydantic, source of `schemas/api/problem.schema.json`), `ProblemType` table (`ALL_TYPES`, 13 slugs incl. `render-timeout`, `not-found`, `internal-error`), `ProblemError`, `problem_from_entex_error` (logs author/operator details server-side), `resolve_request_id` (UUID-only echo), exception handlers overriding FastAPI/Starlette defaults and a catch-all.
  - `src/entex/api/routes.py`: `read_ir_body` async dependency (415/413/400), sync `def render` with `BoundedSemaphore` (503 + Retry-After), `mkdtemp` per request, PDF as bytes, `Content-Disposition` with `filename` + `filename*`, log files → `logging` then `rmtree` (kept when `ENTEX_KEEP_FAILED_JOBS`); `health` (toolchain via which/kpsewhich); `doc-types` list (skips broken, warns) and detail (raw schema.json, 404 problem).
  - `src/entex/api/app.py`: `create_app(settings=None)`, lifespan, `X-Request-ID` middleware, custom OpenAPI (components `Problem`/`ProblemIssue`/`Envelope`, default `HTTPValidationError` removed), `python -m entex.api.app` regenerates `schemas/api/`.
  - Dockerfile `CMD` → uvicorn; `make docker-serve`, `make schemas`; README §API; schemas/README rows; api.md §3.3/§3.4/§9/次 and renderer.md error table updated (status untouched).
- **Verification**: `make lint`, `ruff format --check`, `make test` → 217 passed (TeX host, 0 skipped). Manual: `uvicorn entex.api.app:app` on host + curl → 200 `application/pdf` 61,367 B in 2.1 s, both filename params, health ok, doc-types 1 item, 422/400/415 Problem Details, work dir empty afterwards. No Docker in this env → CI tex job is the Docker check.
- **Record**: api-render AC1–AC5 ticked with test names, Do row, Progress row, Open questions resolved; project-state (P5, active plan api-render, proposal P6 Check for both); plans/README; nav.

## Decisions

- Body parsing lives in an `async def` dependency (needs `await request.body()`); the render handler stays sync `def` as designed. Noted in api.md §3.4.
- `X-Request-ID` echoed only when it parses as a UUID; otherwise generated (no reflection of arbitrary strings).
- `/v1/doc-types` hides broken packages (warning log); `/v1/doc-types/{slug}` surfaces them as `500 package-broken`.
- 503 concurrency test made deterministic by pre-acquiring the semaphore instead of racing two threads.
- Starlette 1.6 `httpx`→`httpx2` TestClient deprecation warning left as-is (tests pass); recorded in plan Open.

## Commits (feature/npc)

`7caeaa2 feat:latexmkの時間切れをRenderTimeoutErrorとして…` · `9a578dd feat:POST /v1/renderほかのFastAPIを追加し…` · `c03247e chore:コンテナのCMDをuvicornにし…` · `3506a38 docs:READMEにAPI節を追加し…` · + record commit.

## Next

- P6 `review-conduct` for both plans (single review doc), then user merges PR #12.
- `@coderabbitai review` posted on PR #12.
