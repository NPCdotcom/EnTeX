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

- [ ] AC1 (FR-A1 / FR-A6 / FR-A8): `examples/valid/` 6 件を `POST /v1/render` すると `200`、`Content-Type: application/pdf`、本文が `%PDF-` で始まり、`Content-Disposition` に `filename="circle-monthly-report.pdf"` と `filename*=UTF-8''…` の両方がある（TeX 環境）。同じ IR で CLI `--tex-only` が出す `.tex` と API 側が書いた `.tex` が一致する（偽 latexmk で `.tex` を捕まえて比較。ホストで実行可）
- [ ] AC2 (FR-A2 / FR-A3): `examples/invalid/` 6 件は `422` + `application/problem+json`。`06-envelope-mismatch` は `type` 末尾 `envelope-mismatch` で `issues` 無し、`03-…` は `ir-invalid` で `issues` 2 件（`path` / `message`）。壊れた JSON・配列・文字列の本文は `400` + Problem Details。どの失敗応答にも FastAPI 既定の `{"detail": [...]}` の形が出ない
- [ ] AC3 (FR-A4 / FR-A5): 偽 latexmk で失敗させると `500` + `render-failed`、`detail` は `RenderError.GENERIC_MESSAGE`、**応答のヘッダと本文全体**に `tests/test_renderer.py::TEX_VOCABULARY` が無い。サーバ側ログ（`caplog`）に `LaTeX Error` がある。壊れた `schema.json` の `packages_dir` では `500` + `package-broken` で `detail` は汎用文（`user_message` はログのみ）
- [ ] AC4 (FR-A7 / NFR-A2 / NFR-A3 / NFR-A4): `GET /v1/health` が TeX ありで `200 {"status":"ok"}`、なしで `503`。`ENTEX_MAX_CONCURRENT_RENDERS=1`・`ENTEX_QUEUE_WAIT_SECONDS=0` で 2 件同時に投げると 1 件が `503` + `Retry-After`。`ENTEX_MAX_BODY_BYTES=100` で `413`。成功・失敗いずれも応答後に `ENTEX_WORK_DIR` 配下にディレクトリが残らない（`ENTEX_KEEP_FAILED_JOBS=1` のときだけ失敗分が残る）
- [ ] AC5: `GET /v1/doc-types` が `[{"doc_type":"circle-monthly-report","schema_version":1,"title":…}]`、`GET /v1/doc-types/circle-monthly-report` が `schema.json` と同じ内容、未知スラッグは `404` Problem Details。`schemas/api/problem.schema.json` / `openapi.json` が生成物と一致（同期テスト）。`make lint` / `make test` 通過、CI の tex ジョブ（Docker、pytest 込み）通過。`docker run … uvicorn` で起動し `curl` で `01-typical.json` から PDF が落ちる（手動、PR 本文に記録）

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

- `RenderError` をタイムアウトと組版失敗で `type` を分けるか（`errors.py` に `RenderTimeoutError` を足す小変更）。**推奨**: この plan で分ける。UI が「時間内に終わらなかった」を別文言にできる
- `X-Request-ID` を受け取る場合の形式検証（任意文字列をそのままログに出さない）

## Agent recommendations（計画時）

| 案 | 概要 | 推奨度 |
|----|------|--------|
| 1 | `/v1/render` だけを先に出し、`/v1/health` `/v1/doc-types*` は次の plan | △ — health が無いと配置先の readiness が組めない。doc-types は 30 行程度 |
| 2 | api.md §3.2 の 4 ルートをこの plan で出す | ✓ — 着手順 3（2 文書種目）で「新パッケージが API に自動で現れるか」を doc-types で判定できる |

**推奨**: 案2。

## User thinking（推敲）

> 2026-09-12: 「1. api.md を agreed にしてよいです。2. Go 4. 承認（pydantic>=2.9）」

## Progress assessments

| Date | Verdict | Summary |
|------|---------|---------|
| 2026-09-12 | on_track | plan 記録直後。`pipeline-and-cli` 完了後に着手 |

## PDCA log

| Date | Phase | Note |
|------|-------|------|
| 2026-09-12 | Plan | api.md §5 の分割案どおり起票。認証は Out of scope に置いて別 plan |
