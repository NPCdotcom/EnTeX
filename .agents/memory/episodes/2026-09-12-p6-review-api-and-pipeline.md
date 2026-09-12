---
id: 2026-09-12-p6-review-api-and-pipeline
date: 2026-09-12
scope: project
tags: [review, P6, H4, api, pipeline, feature/npc]
---

# Episode: P6 Check of `pipeline-and-cli` + `api-render` (one combined review)

## Input

Continuation of user's 「2で進みましょう。」(option 2 = do api-render P5 first, then one combined Check). api-render P5 was already done and pushed (PR #12, CI green incl. Docker tex job run 34669721284). This turn ran the Check.

## Done

- `review-reference`: read both plans, api.md §1 FR-A1..A8 / NFR-A1..A4, diffs `7955490..b561475` (PR #10 implementation part) and `3c0e0b9..711c88e` (PR #12). Re-ran `ruff check` + `pytest` → 217 passed / 0 skipped on the TeX host. `rg circle-monthly-report src/` → 0 hits (invariant check).
- `review-conduct` (V-model RTM): every FR/NFR and all 10 plan ACs map to at least one automated test with file:line. Design invariants (4) hold. Verdict **pass**: Critical 0 / Warning 1 / Suggestion 6.
  - **W1** `routes.py:80-85` — chunked body without `Content-Length` is fully buffered by `await request.body()` before the 413 check; uvicorn has no body-size limit (checked `uvicorn --help`). Verified empirically that chunked oversize still yields 413. Fix: `request.stream()` with early abort. Schedule with the auth plan (before public deploy).
  - S1 api.md §3.1 "新しい例外型は増やさない" contradicts §3.3/§9 (`RenderTimeoutError`) · S2 `RenderResult` lacks `title` → API calls `load_package` twice · S3 no test for the `internal-error` safety net · S4 `is_valid_slug` uses `match`+`$` (fold into old S2 `fullmatch` decision) · S5 no direct tests for `Settings` validation · S6 NFR-A1 not measured with 4 concurrent renders; Starlette httpx→httpx2 deprecation.
- `review-record`: wrote `docs/reviews/2026-09-12-api-and-pipeline-p6-review.md`; Check rows + `done` progress rows in both plans; plans README → "Check pass"; api.md 「次」 ticked; project-state → P6 with proposal "merge PR #12 (user) → roadmap step 3 (second doc-type) P3 design".

## Decisions

- Verdict pass without conditions; W1 is not an AC violation (NFR-A3 response is correct) and is deferred to the auth/public-deploy plan.
- No drive-by fixes made during the review (per `review-conduct` Do-not list).
- PR #12 marked ready for review (CI green + Check pass); merging remains the user's decision.

## Next

- User: merge PR #12.
- Roadmap step 3 (second doc-type) P3 design; fold in S2 (`RenderResult.title`) and use `/v1/doc-types` as the charter §6 judgment signal.
- W1 + S1 small patch; S4 with old S2 (`fullmatch` + one line in ir-type-vocabulary.md).
