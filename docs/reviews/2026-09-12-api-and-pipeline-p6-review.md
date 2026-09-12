---
title: P6 レビュー — pipeline-and-cli（PR #10）+ api-render（PR #12）
kind: review
phase: P6
scope_level: H4
status: agreed
created: 2026-09-12
updated: 2026-09-12
reviewed_commit: 711c88e   # feature/npc（PR #12 の先端）。pipeline-and-cli は main@b561475（PR #10 マージ）に含まれる
related_plans:
  - .agents/plans/programs/pipeline-and-cli.md
  - .agents/plans/programs/api-render.md
related_design:
  - docs/design/programs/api.md
  - docs/design/programs/renderer.md
related_requirements: docs/design/programs/api.md   # §1 FR-A1〜A8 / NFR-A1〜A4（専用の 要件.md は作らない決定）
previous_review: docs/reviews/2026-09-12-renderer-cli-p6-review.md
verdict: pass
---

# P6 レビュー — pipeline-and-cli + api-render

対象は 2 つの plan の Do。ユーザー判断（2026-09-12「2で進みましょう」）により 1 回の Check にまとめる。

| plan | 差分 | 状態 |
|------|------|------|
| `pipeline-and-cli` | [PR #10](https://github.com/NPCdotcom/EnTeX/pull/10) のうち `d5675ab..3c0e0b9`（`7955490..b561475` の実装部分: 10 ファイル +435/−27） | main にマージ済み（`b561475`） |
| `api-render` | [PR #12](https://github.com/NPCdotcom/EnTeX/pull/12)（`3c0e0b9..711c88e`: 実装 15 ファイル +1712/−8、ほか plan / メモリ） | draft、CI green |

手順は skill `review-conduct`（V-model RTM）に従う。前回レビュー（[renderer / CLI](2026-09-12-renderer-cli-p6-review.md)）の W1 / W2 / S1 / S3 / S4 の解消確認も含む。

## 判定

**pass**（Critical なし・Warning 1 件・Suggestion 6 件）。
両 plan の AC はすべて自動テストで根拠がある。Warning は AC 違反ではなく、公開配置（認証を決める plan）より前に入れる小パッチとして残す。

| 項目 | 結果 |
|------|------|
| ローカル検査（本レビュー時、`feature/npc@711c88e`） | `ruff check` 通過 · `pytest` **217 passed / 0 skipped**（ホストに TeX Live あり） |
| CI（PR #12） | run 34669721284: lint/test 3.12 · 3.13 · tex smoke（Docker、pytest 込み）すべて pass |
| 設計前提（AGENTS.md Design invariants） | 4 項目とも違反なし（下記 ST） |
| 前回レビューの指摘 | W1 / W2 / S1 / S3 / S4 解消。S2 は plan Out of scope のまま（未着手） |

## RTM（要件 ↔ 設計 ↔ plan AC ↔ テスト）

検証層: UAT = api.md §1 の検証方法 · ST = api.md §2〜§3 / renderer.md · IT = plan scope / モジュール IF · UT = 単体テスト。

### api-render（api.md §1）

| 要件 | 検証層 | 設計リンク | plan AC | 実装 | テスト / 根拠 | 結果 |
|------|--------|------------|---------|------|---------------|------|
| FR-A1 `POST /v1/render` → `200` `application/pdf` | ST/UAT | api.md §3.2 | AC1 | `src/entex/api/routes.py:140-185` | `tests/test_api.py:120` `test_render_valid_examples_return_pdf`（valid 6 件、`@requires_tex`、`%PDF-` 先頭）· 手動 curl（plan Do 行: 61,367 B / 2.1 s） | pass |
| FR-A2 封筒 / 中身の検証エラー → `422` Problem Details、`issues[]` | UT/IT/UAT | §3.3 表 `envelope-mismatch` / `ir-invalid` | AC2 | `problems.py:223-228` | `test_api.py:170` invalid 6 件 · `:175` 封筒（`issues` 無し）· `:183` `03-…` は `issues` 2 件（`path` / `message`） | pass |
| FR-A3 JSON でない / オブジェクトでない本文 → `400` | UT/UAT | §3.3 `bad-request`、§3.4 `read_ir_body` | AC2 | `routes.py:87-97`、`problems.py:273-275`（`RequestValidationError` 上書き） | `test_api.py:201` 7 種の本文（壊れた JSON・配列・文字列・数値・null・空・非 UTF-8） | pass |
| FR-A4 組版失敗 → `500` `render-failed`、応答に TeX 語彙なし、原文はログ | UT/IT/UAT | §2 不変条件「利用者は TeX を見ない」 | AC3 | `problems.py:235-237`、`routes.py:169-173,200-210` | `test_api.py:218` 偽 latexmk → 本文 + **全ヘッダ**に `TEX_VOCABULARY` 無し、`caplog` に `LaTeX Error` と request_id · `:249` タイムアウトは `render-timeout` に分離（`tests/test_renderer.py:277`） | pass |
| FR-A5 パッケージ不備 → `500` `package-broken`、詳細はログのみ | UT/UAT | §3.3 | AC3 | `problems.py:229-231` | `test_api.py:234` 壊れた `schema.json` → `detail` に `schema.json` が無く、ログにはある | pass |
| FR-A6 `Content-Disposition` に `filename` + `filename*` | UT/UAT | §3.2、§6（RFC 6266 / 8187） | AC1 | `routes.py:193-197` | `test_api.py:125-128`（両方あり・ヘッダ全体が ASCII） | pass |
| FR-A7 `GET /v1/health` が toolchain の有無で 200 / 503 | UT/UAT | §3.2 | AC4 | `routes.py:224-250` | `test_api.py:265`（TeX あり、3 要素）· `:275`（PATH 空 → 503 `degraded`） | pass |
| FR-A8 CLI と API が同じ IR から同じ `.tex` | IT/UAT | §2 図（`pipeline.py` 1 本） | AC1 | `routes.py:162-168` → `pipeline.render_ir` | `test_api.py:143` `test_api_and_cli_write_the_same_tex`（偽 latexmk で API 側 `.tex` を捕まえ CLI `--tex-only` と byte 一致。ホストで実行可） | pass |
| NFR-A1 1 件 10 秒以内、タイムアウトは env で設定（既定 60） | ST | §3.4 / §3.5 | AC4 | `settings.py:19,52` | `test_api.py:133`（2 回目の往復を計測）· 実測 2.1 s（1 件）。**同時 4 件は未計測**（plan Assumption のまま） | pass（目安計測） |
| NFR-A2 同時実行上限 → `503` + `Retry-After` | UT/UAT | §3.4 `BoundedSemaphore` | AC4 | `routes.py:143-151`、`app.py:47` | `test_api.py:286`（セマフォを先に取って再現。plan に明記済みの逸脱、下記） | pass |
| NFR-A3 本文上限 → `413` | UT/UAT | §3.5 `ENTEX_MAX_BODY_BYTES` | AC4 | `routes.py:76-85` | `test_api.py:303`（上限 100 → 413、`detail` に上限値）· レビュー時追加確認: `Content-Length` 無しの chunked 送信でも 413（ただし下記 W1） | pass |
| NFR-A4 一時ディレクトリは応答後に消える、失敗分は設定で残せる | UT/UAT | §3.4 | AC4 | `routes.py:154-190`（`finally` で `rmtree`） | `test_api.py:311` 失敗後 · `:319` 422 後 · `:336` 成功後（TeX）· `:326` `keep_failed_jobs=True` で `latexmk.log` 入りの 1 件だけ残る | pass |
| （AC5）`/v1/doc-types*`、schemas 同期 | UT/IT | §3.2 任意 2 本、§3.7 | AC5 | `routes.py:261-300`、`app.py:88-114,123-128` | `test_api.py:364,376,386`（4 種の不正スラッグ → 404）· `:390` 未知パス · `:394,402` `problem.schema.json` / `openapi.json` 同期 · `:410` 6 ステータスが `application/problem+json`、`HTTPValidationError` 無し | pass |

### pipeline-and-cli

| AC | 起源 | 実装 | テスト / 根拠 | 結果 |
|----|------|------|---------------|------|
| AC1 `render_ir` / `prepare` / `RenderResult` が api.md §3.1 のシグネチャ、CLI は `pipeline` 経由のみ | api.md §3.1、前回 S4 | `src/entex/pipeline.py:41-48,67-126`、`cli.py:134` | `tests/test_pipeline.py:33,43,48` · `:68` `test_cli_goes_through_the_pipeline_only`（`cli.py` のソースに `load_and_validate` / `apply_derived` / `renderer.render` の import が無いことを検査） | pass |
| AC2（W1）規則外 `job_name` は `ValueError`、CLI は stem を正規化 | 前回 W1 | `pipeline.py:24,51-64,102-103`、`cli.py:120`、`renderer.py:183`（`./` 前置） | `test_pipeline.py:84`（`-bad` / `a b` / `x%y` → `ValueError`、`out_dir` を作らない）· `:109` 正規化表 8 件 · `:115` 正規表現が設計と一致 · `tests/test_cli.py:117` 4 件 `--tex-only` · `:190` 同 4 件で PDF（TeX）· `tests/test_renderer.py:266` `./` 前置 | pass（`pct-hash.tex`。plan 例示の `pct-hash-.tex` から末尾 `-` を落とした。Do 行に記録済み） |
| AC3（W2）`template.tex.j2` 欠落は `PackageError`、CLI exit 3 | 前回 W2 | `packages.py:93-95` | `tests/test_renderer.py:146` · `:157`（`build_tex` の安全網は残す）· `tests/test_cli.py:79`（exit 3、出力ディレクトリを作らない） | pass |
| AC4（S1 / S3）renderer.md IF 表が実装と一致、`TEXINPUTS` が既定パスを残す | 前回 S1 / S3 | `renderer.md` §公開 IF · `renderer.py:188-193` | IF 表の 9 行を `src/entex/` の実シグネチャと突き合わせ（`render(content, package, out_dir, *, job_name, timeout)`、`render_ir(...)`、`escape_content` — 一致）· `tests/test_renderer.py:233,255` | pass |
| AC5 lint / test 通過、CLI の利用者向け出力が不変、決定性 | — | — | 217 passed · 既存 `tests/test_cli.py` の期待値変更は W1 / W2 分のみ（`git diff 7955490..b561475 -- tests/test_cli.py` は追加 69 行、削除 0）· `test_pipeline.py:125` `render_ir(tex_only=True)` 経由の決定性 | pass |

### トレーサビリティ判定

- Forward: api.md の 12 要件（FR-A1〜A8、NFR-A1〜A4）と pipeline-and-cli の 5 AC すべてに 1 つ以上の自動テストがある。TeX 依存は FR-A1 / FR-A7(200) / NFR-A1 / NFR-A4(成功) の 4 つで、いずれも CI の Docker ジョブで実行されている。
- Backward: `src/` の変更はすべて要件・設計・plan Open の決定に辿れる。plan scope の外に見える `errors.py` / `renderer.py` の変更（`RenderTimeoutError`）は plan `api-render` の Open「推奨: この plan で分ける」の解消であり、api.md §3.3 表 / §9 にも記録済み。
- Orphan 要件: なし。
- Orphan テスト: `test_api.py:342,351`（`X-Request-ID` の UUID 限定）、`:390`（未知パス 404）、`:420`（語彙表の自衛）は AC に無いが、それぞれ反射攻撃の防止・Problem Details 統一・AC3 の空振り防止を守るもの。維持。

### 四層カバレッジ（G10）

| 層 | 確認 | 状態 |
|----|------|------|
| UT | `tests/test_pipeline.py`（28、parametrize 展開後）· `tests/test_api.py`（48、同）· `tests/test_renderer.py` に W1 / W2 / S3 / timeout の 6 件追加。`Settings` の値検査（`settings.py:34-42`）は直接テストが無い（下記 S5） | ✓ |
| IT | CLI → `pipeline` → renderer（`test_cli.py`）、API → `pipeline` → renderer（`test_api.py`）、両者の `.tex` 一致（FR-A8）。`schemas/api/` と pydantic / FastAPI の同期テスト | ✓ |
| ST | api.md §2 の責務表・§3.2 ルート・§3.3 表（13 種）・§3.4 実行モデル（同期 `def` + セマフォ + `mkdtemp` + `finally`）・§3.5 環境変数 7 個（README / api.md / `settings.py` で名前が一致することを `rg` で確認）に一致。差分は「本文読み取りだけ `async def` 依存」で §3.4 に追記済み | ✓ |
| UAT | api.md §1 の検証方法をそのままテスト化。手動: ホスト uvicorn + curl（plan Do 行）。`docker run … uvicorn` での起動は本環境に Docker が無く未実施（CI の Docker ジョブが pytest 経由で `TestClient` を通す。コンテナ起動そのものは PR #12 マージ後にユーザー環境で `make docker-serve` を一度叩くのが望ましい） | ✓（コンテナ起動の目視は保留） |

### 設計前提の確認（ST）

| 前提 | 確認箇所 | 結果 |
|------|----------|------|
| `renderer` は IR の出どころを知らない | `pipeline.render_ir(raw: Any, …)` は dict のみ。ファイル読みは `cli.py:124`、HTTP 読みは `routes.py:69-97` だけ。`renderer.py` / `ir/` は API 導入で変更なし（timeout 分類のみ） | ✓ |
| 文書種追加で `src/entex/` を変えない | `rg circle-monthly-report src/` → 0 件。ルートに文書種固有のパスなし（`/v1/render` は封筒の `doc_type`、`/v1/doc-types` は `packages/` を列挙） | ✓（判定自体は着手順 3 で行う。`GET /v1/doc-types` がその判定材料） |
| 利用者は TeX を見ない | `detail` に入るのは `user_message` と `problems.py` の定型文のみ（`problems.py:1-5` に明記）。`RenderError.detail` / `log_path` / `PackageError.user_message` は `logger.error` のみ（`problems.py:230,233,236`、`routes.py:200-210`）。想定外例外も `internal-error` 定型文（`problems.py:291-295`） | ✓ |
| 体裁値は doc-package 側 | API は PDF の bytes を素通し（`routes.py:176-185`）。`src/entex/api/` にフォント・余白の値なし | ✓ |

## 指摘

### Critical

なし。

### Warning

| # | 内容 | 場所 | 起源工程 | 提案 |
|---|------|------|----------|------|
| W1 | **本文上限（413）の判定が「全部読んでから」になる。** `Content-Length` があれば先に弾くが、無い場合（chunked）は `await request.body()` で全文をメモリに載せてから長さを見る。uvicorn 側に本文サイズの上限オプションは無い（`--limit-concurrency` / `--limit-max-requests` / `--h11-max-incomplete-event-size` のみ。レビュー時に `uvicorn --help` で確認）。NFR-A3 の応答としては正しい（chunked でも 413 を返すことをレビュー時に `TestClient` で確認）が、公開配置では 1 GB の chunked 本文でメモリを食われる | `src/entex/api/routes.py:80-85` | P5（実装） | `request.stream()` で逐次読み、累計が `max_body_bytes` を超えた時点で `ProblemError(CONTENT_TOO_LARGE)` を投げて打ち切る。パッチ規模: 1 ファイル 10 行以内 + テスト 1 件（chunked で上限超え）。認証 plan（公開配置の前提）と同じタイミングでよい |

### Suggestion

| # | 内容 | 場所 | 提案 |
|---|------|------|------|
| S1 | api.md §3.1 に「新しい例外型は増やさない」と残っているが、同じ文書の §3.3 / §9 で `RenderTimeoutError` を足すと決めている。文書内で矛盾 | `docs/design/programs/api.md:104` | §3.1 の当該文を「`RenderTimeoutError`（`RenderError` の派生）以外は増やさない」に直す。`status` は変えない |
| S2 | 成功時に `load_package()` をもう一度呼んで `title` を取っている（`render_ir` 内で既に読んだパッケージを `RenderResult` が持っていない）。`schema.json` の 2 回読み + 検証 | `src/entex/api/routes.py:177`、`src/entex/pipeline.py:41-48` | `RenderResult` に `title: str`（または `package: DocPackage`）を足す。`pipeline` の公開 IF 変更なので api.md §3.1 も 1 行直す。急がない |
| S3 | 想定外例外の安全網（`internal-error`）にテストが無い。`TestClient(raise_server_exceptions=False)` で `render_ir` を `RuntimeError` に差し替えれば 5 行で書ける | `src/entex/api/problems.py:291-295` | テスト 1 件を足し、応答にトレースバックが無いことを確認する |
| S4 | `is_valid_slug()` が `SLUG_RE.match` + `$` のため末尾改行を通す（`"circle-monthly-report\n"` が合格 → その後 `PackageNotFoundError` になるだけで害は無い）。前回 S2（`pattern` の部分一致）と同じ「`fullmatch` に寄せる」判断 | `src/entex/packages.py:56`、`src/entex/ir/schema.py:35` | 前回 S2 と一緒に `fullmatch` へ。語彙文書の 1 行決定（`doc-record`）と同じ PR で |
| S5 | `Settings.__post_init__` の値検査と `from_env` の変換エラー（`ENTEX_RENDER_TIMEOUT=abc` など）に直接テストが無い。起動時に `ValueError` で落ちる挙動自体は妥当 | `src/entex/api/settings.py:34-42,60-84` | parametrize で 4〜5 件。起動失敗のメッセージが変数名を含むことも確認 |
| S6 | NFR-A1 の Assumption「CPU 数の同時 latexmk で 10 秒を守れる」は 1 件（2.1 s）しか測っていない。Starlette `TestClient` の `httpx`→`httpx2` 非推奨警告も残っている | plan `api-render` Assumptions / Open | Docker で `ENTEX_MAX_CONCURRENT_RENDERS=4` にし同時 4 件を一度計測して plan の Act 行に残す。`httpx2` は CI で警告がエラー化されたときに追う |

## Spec gap / Act への提案

- **W1**: 認証 plan（公開配置の前段）と同じ PR で入れるのが自然。`patch-reference` の小パッチ範囲。
- **S1**: api.md §3.1 の 1 文修正（設計文書の追従。`status` は変えない）。
- **S2 / S3 / S5**: 着手順 3（2 文書種目）か着手順 4（UI）の plan の「ついで」で拾う。単独 PR にするほどではない。
- **S4**: 前回 S2 とまとめて `doc-record`（語彙文書 1 行）+ `fullmatch` 化。
- Recycle 不要。P3 / P4 への巻き戻しは要らない。
- Outcome check（任意）: 「利用者が口頭説明なしで PDF を出せる」（charter §6）は実物 Word 様式の入手後に UAT として実施。API 化で測れるようになった leading indicator は「`/v1/doc-types` に新パッケージが `src/entex/` 無変更で現れるか」で、これは着手順 3 で判定する。

## 次のアクション

1. plan 2 本の PDCA log に Check 行を追加（本レビューへのポインタ）。`.agents/plans/README.md` の Status を「Check pass」に。
2. `docs/project-state.yaml` を P6 に進め、`gate_status.proposal` を「PR #12 を main へ（ユーザー）→ 着手順 3（2 文書種目）の P3 設計へ」にする。W1 / S1〜S6 はブロッカーではないので `open_blockers` には載せない。
3. PR #12 を ready for review にする（CI green・Check pass）。マージはユーザー。
4. 着手順 3 の P3 設計に、S2（`RenderResult.title`）と「`/v1/doc-types` を判定材料にする」ことを織り込む。
