---
title: api-render — POST /v1/render で IR から PDF を返す FastAPI（着手順 2）
kind: plan
status: agreed   # 2026-09-12 ユーザー Go（api.md の P4 分割案）
scope_level: program
pdca_class: S1
pdca_eligible: true
created: 2026-09-12
updated: 2026-09-12
related_design: docs/design/programs/api.md
related_requirements: docs/design/programs/api.md   # §1 FR-A1〜A8 / NFR-A1〜A4（専用の 要件.md は作らないと決定）
promoted_from: ""
parent_hierarchy:
  product: docs/design/product/charter.md
  element: docs/design/elements/ir-type-vocabulary.md
  system: ""
  framework: ""
---

# api-render

## Goal

charter §11 着手順 2「中間表現を POST すると PDF が返る」を [api.md](../../../docs/design/programs/api.md) §3 のとおり実装する。`entex.pipeline`（plan `pipeline-and-cli`）を HTTP から呼ぶ皮を作り、エラーを RFC 9457 Problem Details で返す。着手順 4（UI）の土台。

## Scope hierarchy（確定済み上位）

| Level | Path | Status |
|-------|------|--------|
| H0 product | docs/design/product/charter.md | draft（P0 ゲート Go 済み） |
| H1 element | docs/design/elements/ir-type-vocabulary.md | draft |
| H2 system | — | — |
| H3 framework | charter §7（FastAPI + uvicorn）で確定済み | agreed |
| H4 program | docs/design/programs/api.md → この plan | this plan |
| H5 algorithm | — | — |

## Scope

### In scope

- `src/entex/api/`: `app.py`（`create_app()` / `app`、`lifespan` で `Settings` とツールチェーン確認）、`routes.py`（`POST /v1/render`、`GET /v1/health`、`GET /v1/doc-types`、`GET /v1/doc-types/{doc_type}`）、`problems.py`（`EnTeXError` → Problem Details、FastAPI の `RequestValidationError` / JSON デコード失敗の上書き）、`settings.py`（api.md §3.5 の環境変数）
- `POST /v1/render`: 同期 `def`、`BoundedSemaphore` で同時実行を絞り待ち超過は `503` + `Retry-After`、本文上限超過は `413`、`Content-Type` 不一致は `415`。リクエストごとに `tempfile.mkdtemp(dir=ENTEX_WORK_DIR)`、PDF は bytes で `Response(media_type="application/pdf")`、`Content-Disposition` は ASCII `filename` + `filename*`（RFC 6266 / 8187）。`finally` で一時ディレクトリを消し、失敗時は `latexmk.log` / `render-error.log` の中身を `logging`（`request_id` 付き）へ流す。`ENTEX_KEEP_FAILED_JOBS=1` で残す
- Problem Details: api.md §3.3 の表どおり（400 / 413 / 415 / 422 / 500 / 503）。`type` は `https://entex.example/problems/<slug>`、`title` は型ごとに固定、`detail` は `user_message` または汎用文、`instance` は `urn:uuid:<request id>`（`X-Request-ID` を受け取ればそれ）。`IRValidationError` のみ拡張 `issues[]`
- `schemas/api/problem.schema.json`（pydantic モデルから生成、同期テスト）・`schemas/api/openapi.json`（`python -m entex.api.app` で生成、同期テスト）。`schemas/README.md` の「予定」を埋める
- 起動: Dockerfile `CMD ["uvicorn", "entex.api.app:app", "--host", "0.0.0.0", "--port", "8000"]`、`make docker-serve`、README §API
- ~~`pyproject.toml`: `pydantic>=2.9`~~ → ユーザー承認（2026-09-12）を受けて plan 記録と同じ PR（#10）で先に入れた
- テスト（`httpx` の `TestClient`）: `tests/test_api.py`。TeX 非依存分（422 / 400 / 偽 latexmk の 500 / 413 / 503 / health 503 / doc-types）と `@requires_tex` 分（200 PDF、health 200、NFR-A1 目安）

### Out of scope

- 認証・権限（`Authorization: Bearer` の共有トークンを含め別 plan。公開配置の前に起票）
- 生成履歴・ジョブ化・非同期応答（`job-runner`、着手順 4）
- `.tex` を返す口（`format=tex` など）
- React UI・CSV
- `type` URI の実ドメイン化（配置先決定後）

## Acceptance criteria（S1: ≤5 推奨）

- [x] AC1 (FR-A1 / FR-A6 / FR-A8): `examples/valid/` 6 件を `POST /v1/render` すると `200`、`Content-Type: application/pdf`、本文が `%PDF-` で始まり、`Content-Disposition` に `filename="circle-monthly-report.pdf"` と `filename*=UTF-8''…` の両方がある（TeX 環境）。同じ IR で CLI `--tex-only` が出す `.tex` と API 側が書いた `.tex` が一致する（偽 latexmk で `.tex` を捕まえて比較。ホストで実行可）→ `tests/test_api.py::test_render_valid_examples_return_pdf`（6 件、TeX ありホストで pass）・`test_api_and_cli_write_the_same_tex`
- [x] AC2 (FR-A2 / FR-A3): `examples/invalid/` 6 件は `422` + `application/problem+json`。`06-envelope-mismatch` は `type` 末尾 `envelope-mismatch` で `issues` 無し、`03-…` は `ir-invalid` で `issues` 2 件（`path` / `message`）。壊れた JSON・配列・文字列の本文は `400` + Problem Details。どの失敗応答にも FastAPI 既定の `{"detail": [...]}` の形が出ない → `test_invalid_examples_are_422_problems` / `test_envelope_mismatch_problem_has_no_issues` / `test_ir_invalid_problem_lists_issues` / `test_non_object_bodies_are_400_problems`（7 種の本文）/ `test_wrong_content_type_is_415_problem`。`_assert_problem` が毎回 `Problem.model_validate` と `detail` が list でないことを確認
- [x] AC3 (FR-A4 / FR-A5): 偽 latexmk で失敗させると `500` + `render-failed`、`detail` は `RenderError.GENERIC_MESSAGE`、**応答のヘッダと本文全体**に `tests/test_renderer.py::TEX_VOCABULARY` が無い。サーバ側ログ（`caplog`）に `LaTeX Error` がある。壊れた `schema.json` の `packages_dir` では `500` + `package-broken` で `detail` は汎用文（`user_message` はログのみ）→ `test_render_failure_is_500_without_tex_vocabulary`（request_id がログにも入る）/ `test_broken_package_is_500_package_broken` / `test_render_timeout_is_a_distinct_problem`（`render-timeout`、Open の推奨どおり分けた）
- [x] AC4 (FR-A7 / NFR-A2 / NFR-A3 / NFR-A4): `GET /v1/health` が TeX ありで `200 {"status":"ok"}`、なしで `503`。`ENTEX_MAX_CONCURRENT_RENDERS=1`・`ENTEX_QUEUE_WAIT_SECONDS=0` で 2 件同時に投げると 1 件が `503` + `Retry-After`。`ENTEX_MAX_BODY_BYTES=100` で `413`。成功・失敗いずれも応答後に `ENTEX_WORK_DIR` 配下にディレクトリが残らない（`ENTEX_KEEP_FAILED_JOBS=1` のときだけ失敗分が残る）→ `test_health_ok_with_toolchain` / `test_health_degraded_without_toolchain` / `test_busy_is_503_with_retry_after`（「2 件同時」はスレッド競合を避け、セマフォを先に取って 1 件が組版中の状態を決定的に再現）/ `test_too_large_body_is_413` / `test_work_dir_is_clean_after_{failure,validation_error,success}` / `test_failed_job_is_kept_when_configured`
- [x] AC5: `GET /v1/doc-types` が `[{"doc_type":"circle-monthly-report","schema_version":1,"title":…}]`、`GET /v1/doc-types/circle-monthly-report` が `schema.json` と同じ内容、未知スラッグは `404` Problem Details。`schemas/api/problem.schema.json` / `openapi.json` が生成物と一致（同期テスト）。`make lint` / `make test` 通過、CI の tex ジョブ（Docker、pytest 込み）通過。`docker run … uvicorn` で起動し `curl` で `01-typical.json` から PDF が落ちる（手動、PR 本文に記録）→ `test_doc_types_lists_packages` / `test_doc_type_detail_returns_schema_json` / `test_unknown_doc_type_is_404_problem` / `test_unknown_route_is_404_problem` / `test_problem_schema_is_in_sync` / `test_openapi_is_in_sync` / `test_openapi_declares_problem_responses`。`make lint` / `make test` 217 passed（TeX ありホスト）。手動: この環境に Docker が無いためホストの `uvicorn entex.api.app:app` に `curl` → `200 application/pdf` 61,367 バイト、往復 2.1 秒、`Content-Disposition` に `filename` と `filename*` の両方、`/v1/health` `ok`、`/v1/doc-types` 1 件、422/400/415 が Problem Details、`ENTEX_WORK_DIR` は空。CI の tex ジョブは PR #10 で確認

## Dependencies

- plan `pipeline-and-cli`（`entex.pipeline.render_ir()`。先に完了させる）
- `fastapi` / `uvicorn[standard]` / `httpx`（dev）— `pyproject.toml` に既存
- Docker イメージ `entex-dev`（CI の tex ジョブ）

## Facts

- api.md §3（IF / Problem Details 表 / 実行モデル / 設定）は agreed（2026-09-12）
- 現行 FastAPI 0.141 系は `pydantic>=2.9` を要求。開発環境の実インストールは pydantic 2.13.5 / fastapi 0.141.1
- FastAPI は `def` のパス関数を AnyIO のスレッドプール（既定 40 トークン）で実行する（api.md §6）

## Assumptions

- 1 コンテナ・uvicorn 1 プロセス。CPU 数の同時 latexmk で NFR-A1（10 秒）を守れる — 実測して plan の Do 行に残す
- PDF は数百 KB 以下で、bytes をメモリに載せてよい
- `/v1/doc-types/{doc_type}` は `schema.json` をそのまま返してよい（`expr` / `derived` を含む。UI が `derived` を入力欄から外す判断に使う）

## Open questions

- ~~`RenderError` をタイムアウトと組版失敗で `type` を分けるか（`errors.py` に `RenderTimeoutError` を足す小変更）。**推奨**: この plan で分ける。UI が「時間内に終わらなかった」を別文言にできる~~ → **分けた（Do）**: `RenderTimeoutError(RenderError)`、`type` `render-timeout`、文言はやり直しを促す。CLI は `RenderError` として捕まえ exit 2 のまま
- ~~`X-Request-ID` を受け取る場合の形式検証（任意文字列をそのままログに出さない）~~ → **UUID として解釈できるときだけ採用**、それ以外は生成（`resolve_request_id`）。`test_request_id_header_is_{echoed_when_it_is_a_uuid,replaced_when_not_a_uuid}`
- （Do で出た小さな判断）`GET /v1/doc-types` は読み込めるパッケージだけを返し、壊れたものは `logger.warning` に出して外す。`GET /v1/doc-types/{doc_type}` の方は `500 package-broken` で作者が気づける
- Starlette 1.6 が `httpx` ベースの `TestClient` に非推奨警告（`httpx2` を推奨）を出す。テストは通るので今回は追わない。CI で警告がエラー化されたら dev 依存を見直す

## Agent recommendations（計画時）

| 案 | 概要 | 推奨度 |
|----|------|--------|
| 1 | `/v1/render` だけを先に出し、`/v1/health` `/v1/doc-types*` は次の plan | △ — health が無いと配置先の readiness が組めない。doc-types は 30 行程度 |
| 2 | api.md §3.2 の 4 ルートをこの plan で出す | ✓ — 着手順 3（2 文書種目）で「新パッケージが API に自動で現れるか」を doc-types で判定できる |

**推奨**: 案2。

## User thinking（推敲）

> 2026-09-12: 「1. api.md を agreed にしてよいです。2. Go 4. 承認（pydantic>=2.9）」
> 2026-09-12: 「2で進みましょう。」— `pipeline-and-cli` の Check を先にせず、この plan の P5 へ進んで Check を 2 plan まとめて行う

## Progress assessments

| Date | Verdict | Summary |
|------|---------|---------|
| 2026-09-12 | on_track | plan 記録直後。`pipeline-and-cli` 完了後に着手 |
| 2026-09-12 | on_track | Do 完了。AC1–AC5 検証済み（217 tests、lint pass、ホスト uvicorn + curl で PDF 取得）。`pipeline-and-cli` と合わせて P6 Check 待ち。Assumption「CPU 数の同時 latexmk で NFR-A1 を守れる」は 1 件 2.1 秒（4 CPU ホスト、`01-typical`）を実測、同時 4 件の実測は未 |
| 2026-09-12 | done | Check pass（`pipeline-and-cli` とまとめて 1 回）。FR-A1〜A8 / NFR-A1〜A4 すべてテストに根拠あり。Warning 1（W1: chunked 本文の 413 判定が全文読み後。公開配置前に stream 化）、Suggestion 6。PR #12 を ready for review に |

## PDCA log

| Date | Phase | Note |
|------|-------|------|
| 2026-09-12 | Plan | api.md §5 の分割案どおり起票。認証は Out of scope に置いて別 plan |
| 2026-09-12 | Do | TDD（Red: `tests/test_api.py` 全 AC → Green → Refactor）。`src/entex/api/`: `settings.py`（`Settings` frozen dataclass、`from_env`、値の検査）、`problems.py`（`Problem` / `ProblemIssue` pydantic = `schemas/api/problem.schema.json` の正本、`ProblemType` 13 種の表 `ALL_TYPES`、`ProblemError`、`problem_from_entex_error`、FastAPI / Starlette 既定ハンドラの上書き、想定外例外の安全網）、`routes.py`（`read_ir_body` 非同期依存で 415/413/400、`render` は同期 `def` + `BoundedSemaphore` + `mkdtemp` + `finally` 削除、`health`、`doc-types` 2 本）、`app.py`（`create_app(settings=None)`、lifespan で Settings/semaphore/toolchain、`X-Request-ID` middleware、OpenAPI に `Problem` / `Envelope` を components 化し既定 `HTTPValidationError` を除去、`python -m entex.api.app` で `schemas/api/` 再生成）。`errors.RenderTimeoutError` を追加し `renderer.render()` の `TimeoutExpired` をそれに（`test_latexmk_timeout_is_a_render_timeout_error`）。Dockerfile `CMD` uvicorn、`make docker-serve` / `make schemas`、README §API、schemas/README、api.md §3.3/§3.4/§9 と renderer.md エラー表を実装に追従（`status` 据え置き）。設計との差: 本文読み取りだけ `async def` 依存（`await request.body()` のため。api.md に追記）。— files: src/entex/api/{__init__,app,problems,routes,settings}.py, src/entex/errors.py, src/entex/renderer.py, schemas/api/{problem.schema.json,openapi.json}, tests/test_api.py, tests/test_renderer.py, Dockerfile, Makefile, README.md, schemas/README.md, docs/design/programs/{api,renderer}.md（commits 7caeaa2 / 9a578dd / c03247e / 3506a38） |
| 2026-09-12 | Check | pass — [docs/reviews/2026-09-12-api-and-pipeline-p6-review.md](../../../docs/reviews/2026-09-12-api-and-pipeline-p6-review.md)。217 passed / lint pass / CI（PR #12）green。設計前提 4 項目違反なし。**W1**: `read_ir_body` は `Content-Length` 無しの chunked 本文を全文読んでから 413 にする（`routes.py:80-85`）。uvicorn 側に本文上限は無いので、公開配置（認証 plan）の前に `request.stream()` で逐次打ち切りへ（1 ファイル 10 行 + テスト 1 件）。**S1** api.md §3.1「新しい例外型は増やさない」が §3.3 / §9 と矛盾（1 文修正）· **S2** `RenderResult.title` で `load_package` 二重呼びを消す · **S3** `internal-error` 安全網のテスト · **S5** `Settings` 値検査のテスト · **S6** 同時 4 件の NFR-A1 実測、`httpx2` 警告。Recycle 不要 |
