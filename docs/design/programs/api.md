---
title: api — IR を POST すると PDF が返る（着手順 2）
kind: design
phase: P3
scope_level: program
status: agreed   # 2026-09-12 ユーザー確認「api.md を agreed にしてよいです」
created: 2026-09-12
updated: 2026-09-12
parent_element: docs/design/elements/ir-type-vocabulary.md
parent_system: ""
related_design: docs/design/programs/renderer.md
related_requirements: docs/design/product/charter.md   # §11 着手順 2。専用の 要件.md は Open（本文 §1）
related_review: docs/reviews/2026-09-12-renderer-cli-p6-review.md
---

# api（H4）

親: [charter.md](../product/charter.md) §5 / §11 · [renderer.md](./renderer.md) · [P6 レビュー](../../reviews/2026-09-12-renderer-cli-p6-review.md)

## 目的（どの H1/H2 のためか）

charter §11 着手順 2「API化する。中間表現を POST すると PDF が返る」を実現する。着手順 1（CLI）で固めた検証・導出・エスケープ・組版の流れを **HTTP 越しに同じ結果で** 呼べるようにし、着手順 4 の `form-ui` が乗る土台と、着手順 3（2 文書種目）の判定材料（`src/entex/` を触らずに文書種を増やせるか）を用意する。

同時に、P6 レビュー S4 で指摘した「`load_and_validate → apply_derived → render` の並びを CLI が直接書いている」問題を解消する。API がこの 3 段をもう一度書くのではなく、**共通のパイプライン関数** を 1 つ置き、CLI と API がそれを呼ぶ形にする。

範囲外: 認証・権限、生成履歴・ジョブ化（`job-runner`、着手順 4）、CSV（着手順 5）、2 文書種目の追加そのもの、React UI。

## 1. 要件（この設計が満たすもの）

着手順 2 には専用の `docs/requirements/<slug>/要件.md` が無い。charter §4 / §5 / §6 / §11 と renderer の要件.md（FR1–FR8・NFR1–2 はそのまま API 経由でも成立させる）から、API 固有の要件を以下に起こす。P2 文書として独立させるかは Open（§8）。

| ID | 要件 | 検証方法 |
|----|------|----------|
| FR-A1 | `POST /v1/render` に IR（封筒込み JSON）を送ると、`200` と `application/pdf` の本文で PDF が返る | `examples/valid/` 6 件を POST し、本文が `%PDF-` で始まり、`Content-Type: application/pdf` であること（TeX 環境） |
| FR-A2 | 封筒不一致・中身の検証エラーは `422` と RFC 9457 Problem Details（`application/problem+json`）で返り、`detail` は日本語、`issues` に件ごとの `path` / `message` が入る（FR1–FR3 と同じ内容） | `examples/invalid/` 6 件を POST。`06-envelope-mismatch` は `issues` 無しの封筒エラー 1 件、`03-…` は `issues` 2 件 |
| FR-A3 | JSON として読めない本文・オブジェクトでない本文は `400` の Problem Details で返る | 壊れた JSON / 配列 / 文字列を POST |
| FR-A4 | 組版失敗（`RenderError`）は `500` の Problem Details で、`detail` は `RenderError.GENERIC_MESSAGE`。**応答本文・ヘッダのどこにも TeX の語彙が出ない**。原文（latexmk のログ）はサーバ側ログにだけ残る | 偽 `latexmk` を PATH に置いて POST し、応答全文に `tests/test_renderer.py::TEX_VOCABULARY` が無いこと。サーバ側ログに `LaTeX Error` があること |
| FR-A5 | パッケージ不備（`PackageError` / `DerivationError`）は `500` の Problem Details。`detail` は汎用文で、パッケージ作者向けの詳細はサーバ側ログにだけ出す | 壊れた `schema.json` の `packages_dir` を設定して POST |
| FR-A6 | 応答ヘッダ `Content-Disposition` に保存名を付ける。ASCII の `filename` と UTF-8 の `filename*`（RFC 6266 / 8187）の両方を出す | 応答ヘッダの検査 |
| FR-A7 | `GET /v1/health` がツールチェーン（`lualatex` / `latexmk` / `luatexja.sty`）の有無を返す（`entex doctor` の HTTP 版）。配置先（Fly.io / Cloud Run）の readiness に使う | TeX あり: `200 {"status":"ok"}`、無し: `503` |
| FR-A8 | CLI `entex render` と API `POST /v1/render` は同じ IR から同じ `.tex` を作る（パイプラインが 1 本であることの検証） | 同じ IR で CLI `--tex-only` の `.tex` と API 側の `.tex` を比較 |
| NFR-A1 | 生成 1 件は 10 秒以内（charter §6）。API 側の latexmk タイムアウトは環境変数で設定でき、既定 60 秒 | `01-typical` の往復時間を計測（目安） |
| NFR-A2 | 同時実行数に上限を持ち、上限超えは `503` + `Retry-After` で返す（latexmk で CPU を食い潰さない） | 上限 1 に設定し 2 件同時に POST |
| NFR-A3 | 本文サイズに上限を持ち、超過は `413` | 上限を小さく設定して POST |
| NFR-A4 | 一時ディレクトリは応答後に消える（成功時）。失敗時は設定で残せる（既定は消す。ログにのみ原文を残す） | テスト後に work dir が空 |

## 2. 責務・境界

```
[ CLI: cli.py ]                     [ API: api/ ]
  JSON ファイルを読む                 HTTP 本文を JSON として読む・Problem Details を返す
      │ raw dict                          │ raw dict
      ▼                                   ▼
[ pipeline.py ]  render_ir(raw, packages_dir, out_dir, *, job_name, tex_only) -> RenderResult
      │  load_and_validate → apply_derived → renderer.render（または build_tex）
      │  ジョブ名の正規化・出力ディレクトリの作成はここが持つ（P6 レビュー W1 の解消）
      ▼
[ ir/ · tex/ · renderer.py ]  変更なし。IR の出どころ（ファイル / HTTP）を知らない
```

| モジュール | 知っていること | 知らないこと |
|---|---|---|
| `entex.api` | HTTP（ルート・ステータス・ヘッダ・Problem Details）、設定（環境変数）、一時ディレクトリの寿命 | IR の型、TeX、doc-package の中身 |
| `entex.pipeline` | 3 段の並び、`EnTeXError` の種類、ジョブ名の規則 | 呼び出し元が CLI か HTTP か |
| `entex.cli` | ファイル I/O、終了コード | 3 段の中身（`pipeline` に委ねる） |
| `entex.ir` / `entex.tex` / `entex.renderer` | 変更なし（renderer.md） | 変更なし |

守る不変条件（AGENTS.md Design invariants）:

- `renderer` は IR の出どころを知らない — `pipeline` が dict だけを受け取り、API はファイルもパスも渡さない
- 文書種追加で `src/entex/` を変えない — API のルートに文書種固有のパスを作らない（`/v1/render` は封筒の `doc_type` で振り分ける）
- 利用者は TeX を見ない — Problem Details の `detail` は `EnTeXError.user_message` のみ。`RenderError.detail` / `log_path` はサーバ側ログ
- 体裁値は doc-package 側 — API は PDF のバイト列を素通しする

## 3. 公開インターフェース / API

### 3.1 Python — `entex.pipeline`（CLI と API の共通入口）

```python
@dataclass(frozen=True, slots=True)
class RenderResult:
    doc_type: str
    schema_version: int
    job_name: str
    out_dir: Path
    tex_path: Path
    pdf_path: Path | None      # tex_only のとき None

def prepare(raw: Any, packages_dir: Path) -> PreparedIR
    # load_and_validate + apply_derived。PreparedIR = ValidatedIR + content（導出値込み）

def render_ir(
    raw: Any,
    packages_dir: Path,
    out_dir: Path,
    *,
    job_name: str = "document",
    tex_only: bool = False,
    timeout: float | None = None,
) -> RenderResult
```

- `job_name` は `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$` に **限定** し、外れたら `ValueError`（呼び出し側のプログラムミス）。CLI は JSON のファイル名の stem をこの規則に **正規化**（合わなければ `document`）して渡す。latexmk への引数は `./<job>.tex` と前置する。→ P6 レビュー W1 の解消をここに置く
- 例外は既存の `EnTeXError` 階層をそのまま上げる（新しい例外型は増やさない）。`template.tex.j2` の欠落は `load_package()` で `PackageError` にする → W2 の解消
- `prepare()` を分けるのは、着手順 4 の UI が「検証だけ」（プレビュー前のエラー表示）を呼べるようにするため。今回は `render_ir()` の内部で使うだけでよい

### 3.2 HTTP

| メソッド / パス | 入力 | 成功 | 失敗（すべて `application/problem+json`） |
|---|---|---|---|
| `POST /v1/render` | `application/json`、IR の封筒（`schemas/ir/envelope.schema.json`） | `200` `application/pdf`、`Content-Disposition: attachment; filename="<doc_type>.pdf"; filename*=UTF-8''<title>.pdf` | `400` 本文不正 · `413` 本文過大 · `415` `Content-Type` 不一致 · `422` 封筒 / 中身 · `500` 組版失敗 / パッケージ不備 · `503` 同時実行上限（`Retry-After`） |
| `GET /v1/health` | — | `200 {"status": "ok", "toolchain": {...}}` | `503 {"status": "degraded", ...}`（TeX 不在） |
| `GET /v1/doc-types`（任意） | — | `200 [{"doc_type", "schema_version", "title"}]` | — |
| `GET /v1/doc-types/{doc_type}`（任意） | パススラッグ | `200` `schema.json` の内容 | `404` |

`/v1/doc-types*` は着手順 4（`form-ui` がスキーマからフォームを作る）で必要になる読み取り専用の 2 本。実装は小さいが着手順 2 の定義には無いので、P4 で「同じ plan に含める / 別 plan / 見送り」を決める（§7 推奨は「含める」）。

`format=tex` のような `.tex` を返す口は **v1 では作らない**。charter §5 は出力に `.tex` を含めるが、それはテンプレート作者向けで認証と一緒に考える（Open）。

### 3.3 エラー応答 — RFC 9457 Problem Details

FastAPI 既定の `{"detail": ...}` ではなく、[RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) の形に統一する。FastAPI 自身が出す `RequestValidationError`（本文が JSON でない等）も同じ形に上書きする。

```json
{
  "type": "https://entex.example/problems/ir-invalid",
  "title": "入力に問題があります",
  "status": 422,
  "detail": "入力に2件の問題があります。\n- 会計明細 1行目の区分は 収入 / 支出 のいずれかを選んでください\n- …",
  "instance": "urn:uuid:<request id>",
  "issues": [
    {"path": "finance[0].category", "message": "会計明細 1行目の区分は 収入 / 支出 のいずれかを選んでください"}
  ]
}
```

| 例外（`entex.errors`） | status | `type` の末尾 | `detail` | 拡張 |
|---|---|---|---|---|
| 本文が JSON でない / オブジェクトでない（FastAPI 層） | 400 | `bad-request` | 「入力を JSON として読めません。」 | — |
| `EnvelopeError` | 422 | `envelope-mismatch` | `user_message` | — |
| `IRValidationError` | 422 | `ir-invalid` | `user_message` | `issues[]`（`FieldIssue` をそのまま） |
| `PackageError` / `DerivationError` | 500 | `package-broken` | 汎用文「文書種の定義に問題があります。管理者へお問い合わせください。」 | — （`user_message` はサーバ側ログ） |
| `RenderError` | 500 | `render-failed` | `RenderError.GENERIC_MESSAGE` | — （`detail` / `log_path` の中身はサーバ側ログ） |
| `RenderTimeoutError`（P5 で追加。`RenderError` の派生） | 500 | `render-timeout` | `RenderTimeoutError.GENERIC_MESSAGE`（やり直しを促す文） | — |
| 同時実行上限 | 503 | `busy` | 「混み合っています。しばらくしてからやり直してください。」 | ヘッダ `Retry-After` |
| 本文過大 | 413 | `content-too-large` | 上限値を含む日本語文 | — |
| `Content-Type` が JSON でない | 415 | `unsupported-media-type` | 「本文は application/json で送ってください。」 | — |
| 未知のパス / 未知の `doc_type`（`/v1/doc-types/{doc_type}`） | 404 | `not-found` | 定型文 | — |
| 想定外の例外（安全網） | 500 | `internal-error` | 定型文（トレースバックは出さない） | — |

P5 実装メモ（2026-09-12）: `type` の一覧と `title` は `src/entex/api/problems.py` の `ALL_TYPES` が正本。`X-Request-ID` は **UUID として解釈できるときだけ** 採用し、それ以外は生成する（任意文字列をログや応答に反射しない。§9 Open の解消）。応答ヘッダにも同じ `X-Request-ID` を返す。

`type` の URI は当面ドキュメントに解決しないダミー（`https://entex.example/problems/<slug>`）。実 URL に変えるのは配置先が決まってから。`title` は `type` ごとに固定、`detail` だけが出来事ごとに変わる（RFC 9457 §3.1.3 / §3.1.4）。`instance` はリクエスト ID（`X-Request-ID` を受け取ればそれ、無ければ生成）で、サーバ側ログの行と突き合わせる鍵にする。

400 と 422 の使い分けは RFC 9110 §15.5.1 / §15.5.21 に従う: 構文が壊れていれば 400、構文は正しいが中身が処理できなければ 422。封筒不一致は「JSON としては正しい」ので 422（`doc_type` 不明を 404 にする案は退けた。`/v1/render` というリソースは存在するため）。

### 3.4 実行モデル

- エンドポイントは **同期 `def`** で書く。FastAPI（Starlette）は `def` のハンドラをスレッドプール（AnyIO、既定 40 トークン）で実行するので、`subprocess.run` の latexmk がイベントループを塞がない。`renderer.render()` を async 化しない。本文の読み取り（415 / 413 / 400）だけは `async def` の依存 `read_ir_body` に切り出す（`await request.body()` が要るため。P5 実装メモ）
- 同時実行は `threading.BoundedSemaphore(ENTEX_MAX_CONCURRENT_RENDERS)`（既定: CPU 数）で絞る。取得を `ENTEX_QUEUE_WAIT_SECONDS`（既定 5 秒）待って取れなければ `503`
- 1 リクエスト = 1 一時ディレクトリ（`tempfile.mkdtemp(dir=ENTEX_WORK_DIR)`）。PDF を **bytes に読んでから** `Response(content=..., media_type="application/pdf")` で返し、`finally` で消す（`FileResponse` + `BackgroundTask` は応答送出後まで削除を遅らせる必要が出るので採らない。PDF は数十〜数百 KB の想定）
- 失敗時は `latexmk.log` / `render-error.log` の中身を `logging`（`request_id` 付き）に流してから消す。`ENTEX_KEEP_FAILED_JOBS=1` のときだけディレクトリを残す
- latexmk のタイムアウトは `ENTEX_RENDER_TIMEOUT`（既定 60 秒。renderer の既定 180 秒より短くする）

### 3.5 設定（環境変数）

| 変数 | 既定 | 用途 |
|---|---|---|
| `ENTEX_PACKAGES_DIR` | `packages.default_packages_dir()` | doc-package の置き場（既存） |
| `ENTEX_WORK_DIR` | システムの tmp | 一時ディレクトリの親 |
| `ENTEX_RENDER_TIMEOUT` | `60` | latexmk のタイムアウト秒 |
| `ENTEX_MAX_CONCURRENT_RENDERS` | CPU 数 | 同時 latexmk 数 |
| `ENTEX_QUEUE_WAIT_SECONDS` | `5` | セマフォ待ち上限 |
| `ENTEX_MAX_BODY_BYTES` | `1048576`（1 MiB） | 本文上限（`max_items` 20 行の IR は数 KB） |
| `ENTEX_KEEP_FAILED_JOBS` | `0` | 失敗ジョブのディレクトリを残す |

新しい依存（`pydantic-settings`）は入れず、`os.environ` を読む小さな `Settings` データクラスで足りる。

### 3.6 起動

- 本番相当: `uvicorn entex.api.app:app --host 0.0.0.0 --port 8000`（Dockerfile の `CMD` をこれに変える。`EXPOSE 8000` は既にある）
- 開発: `make docker-serve`（`compose.yaml` の `ports: 8000:8000` を使う）
- `entex serve` コマンドは **作らない**（uvicorn の薄い包みになるだけ。必要になれば足す）

### 3.7 モジュール配置

```
src/entex/
  pipeline.py          # render_ir / prepare / RenderResult / job_name 規則
  api/
    __init__.py
    app.py             # create_app() / app = create_app()、lifespan で Settings と toolchain 確認
    routes.py          # /v1/render /v1/health（/v1/doc-types*）
    problems.py        # EnTeXError → Problem Details、FastAPI 例外ハンドラ
    settings.py        # 環境変数
schemas/api/
  problem.schema.json  # Problem Details（拡張 issues 込み）の JSON Schema。pydantic モデルから生成
  openapi.json         # `python -m entex.api.app` で生成（schemas/README.md の「予定」を埋める）
```

## 4. 依存（H3 フレームワーク）

charter §7 で FastAPI は確定済み。新規選定なし。

| 用途 | 選定 | 備考 |
|---|---|---|
| HTTP | FastAPI + uvicorn | `pyproject.toml` に既にある（`fastapi>=0.115`、`uvicorn[standard]>=0.30`）。**注意**: 現行の FastAPI は `pydantic>=2.9` を要求する（FastAPI PR #15139、2026-03）。`pyproject.toml` の `pydantic>=2.7` は下限を揃える |
| テスト | `httpx`（`TestClient`） | dev 依存に既にある |
| エラー形式 | RFC 9457 | 自前で 30 行程度。ライブラリは入れない |
| 設定 | `os.environ` | `pydantic-settings` は入れない |

## 5. エージェント提案

| # | 論点 | 案 | 推奨 |
|---|---|---|---|
| 1 | 3 段の並びの置き場 | (a) API が CLI と同じ並びをもう一度書く · (b) `entex.pipeline.render_ir()` を作り CLI も API もそれを呼ぶ | **(b)** — 並びが 2 か所にあると FR-A8（同じ `.tex`）が壊れる余地が残る。P6 レビュー S4 |
| 2 | エラー応答の形 | (a) FastAPI 既定 `{"detail": ...}` · (b) RFC 9457 Problem Details | **(b)** — `type` で機械判別、`detail` で日本語、`issues` で件ごと。UI（着手順 4）がフィールドにエラーを貼るのに `path` が要る |
| 3 | latexmk の実行 | (a) `def` ハンドラ + セマフォ · (b) `asyncio.create_subprocess_exec` で renderer を async 化 · (c) ジョブキュー（202 Accepted + ポーリング） | **(a)** — renderer を触らずに済む。(c) は `job-runner`（着手順 4）の話で、今は 1 リクエスト = 1 生成の同期応答で足りる |
| 4 | PDF の返し方 | (a) bytes を `Response` · (b) `FileResponse` + `BackgroundTask` で削除 | **(a)** — 一時ディレクトリの寿命を `finally` で閉じられる。PDF は小さい |
| 5 | `/v1/doc-types*` | (a) 今回含める · (b) 着手順 4 まで見送る | **(a)** — 読み取り専用で 30 行程度、着手順 3 の判定（新パッケージが API に自動で現れるか）にも使える |
| 6 | W1 / W2 の直し方 | (a) 先に小パッチ PR · (b) `pipeline` 導入の plan に含める | **(b)** — ジョブ名の所有者が `pipeline` に移るので、そこで規則を決めるのが自然。W2 も `load_package()` の 3 行 |

### P4 plan の分割案

| Plan（仮称） | scope_level | 含む | 完了判定 |
|---|---|---|---|
| `pipeline-and-cli` | H4 program | `entex.pipeline`、CLI をそれに乗せ替え、W1（ジョブ名）・W2（テンプレ欠落 → `PackageError`）、renderer.md IF 表の追従（S1） | 既存テスト 126 件が通り、CLI の出力が変わらない（ジョブ名の正規化を除く）。`make test` で判定可（TeX 非依存） |
| `api-render` | H4 program | `entex.api`（`/v1/render` `/v1/health` `/v1/doc-types*`）、Problem Details、Settings、`schemas/api/`、Dockerfile `CMD`、`make docker-serve`、テスト（FR-A1〜A8・NFR-A1〜A4） | `make docker-test` 相当で FR-A1 が通る。ホストでは偽 latexmk で FR-A4 |

先に `pipeline-and-cli` を入れると、`api-render` は HTTP の皮だけになる。

## 6. Terminology alignment（外部調査、2026-09-12）

| 用語 | 本プロジェクトでの定義 | 外部の一般定義（要約） | ソース |
|---|---|---|---|
| Problem Details | API のエラー応答の JSON 形。`type` / `title` / `status` / `detail` / `instance` + 拡張 `issues` | HTTP API のエラーを `application/problem+json` で表す標準。`type` は URI、`title` は型ごとに固定、`detail` は出来事ごと | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) §3 |
| 400 / 422 | 400 = 本文が JSON でない、422 = JSON だが封筒・中身が処理できない | 400 Bad Request = 構文不正、422 Unprocessable Content = 構文は正しいが処理できない（RFC 9110 で正式化） | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) §15.5.1 / §15.5.21 |
| `Content-Disposition` の `filename*` | 日本語の保存名を `filename*=UTF-8''…` で、ASCII の `filename` を先に併記 | 非 ASCII は `filename*`（RFC 8187 の符号化）で送り、`filename` は互換用の ASCII フォールバック。`filename` を先に置く | [RFC 6266](https://www.rfc-editor.org/rfc/rfc6266.html) §4.3 / Appendix D · [RFC 8187](https://datatracker.ietf.org/doc/html/rfc8187) |
| `def` ハンドラ（sync endpoint） | latexmk を呼ぶルートは `def` で書き、スレッドプールに任せる | FastAPI は `def` のパス関数を外部スレッドプールで実行して await する。ブロッキング I/O を含むなら `def` | [FastAPI docs — async](https://fastapi.tiangolo.com/async/) · [Starlette — Thread Pool](https://starlette.dev/threadpool/)（既定 40 トークン） |
| `Response(content=bytes, media_type="application/pdf")` | PDF はメモリに読んで `Response` で返す | メモリ上のデータは `StreamingResponse` ではなく `Response`。`FileResponse` はディスク上のファイルをストリーム | [FastAPI docs — Custom Response](https://fastapi.tiangolo.com/advanced/custom-response/) |
| lifespan | 起動時に Settings とツールチェーンを確認する場所 | `@asynccontextmanager` の `lifespan` を `FastAPI(lifespan=...)` に渡す（`on_event` は非推奨） | FastAPI 0.141 系（2026-07）のドキュメント |

ズレ・リスク: 「バリデーションエラー = 422」は FastAPI の慣習でもあるが、FastAPI 既定の 422 本文は `{"detail": [...]}` で Problem Details ではない。既定ハンドラを上書きしないと 2 種類の形が混ざる。

## 7. Facts

- charter §11 着手順 2 は「中間表現を POST すると PDF が返る」。認証は charter §11 Open のまま
- `pyproject.toml` に `fastapi` / `uvicorn` / `httpx`（dev）は既にある。`Dockerfile` は `EXPOSE 8000`、`compose.yaml` は `8000:8000` を持つ
- `entex.errors` の 5 例外はすべて `user_message` を持ち、renderer.md は「CLI 層・将来の API 層の両方が同じ形でハンドリングできる」ことを前提に設計済み
- P6 レビュー（2026-09-12）: W1（ジョブ名素通し）・W2（テンプレ欠落が exit 2）・S4（3 段の並びが CLI にある）
- 現行 FastAPI（0.141 系）は pydantic ≥ 2.9 を要求する

## 8. Assumptions

- 当面の利用者は我々 2 人と、着手順 4 で作る UI。公開配置は認証を決めてから（Open）
- PDF は 1〜2 ページ・数百 KB 以下。bytes でメモリに載せて問題ない
- 1 コンテナで uvicorn 1 プロセス。CPU 数分の latexmk 同時実行で NFR-A1 を守れる（実測は plan で）
- `.tex` を API から返す需要は今は無い（テンプレート作者は CLI `--tex-only` を使う）

## 9. Open questions

- API 固有の要件（§1）を `docs/requirements/api/要件.md` として P2 文書に独立させるか、この設計の §1 のままでよいか。**推奨**: このままで進め、着手順 4（UI）で要件が膨らんだら独立させる
- 認証: 公開配置の前に、最低限の共有トークン（`Authorization: Bearer`）を `api-render` に含めるか、別 plan にするか
- `type` URI の実ドメイン（配置先決定後）
- ~~`RenderError` を「タイムアウト」と「組版失敗」で `type` を分けるか（現状の `RenderError` は区別を持たない。分けるなら `errors.py` に `RenderTimeoutError` を足す小さな変更）~~ → **分けた（P5, 2026-09-12）**: `errors.RenderTimeoutError(RenderError)`、`type` は `render-timeout`。CLI は `RenderError` として捕まえるので exit 2 のまま（文言だけ変わる）
- ~~`GET /v1/doc-types/{doc_type}` が返す `schema.json` に `expr` や `derived` をそのまま含めてよいか~~ → **含める（P5）**: ファイルの内容をそのまま返す（`load_package` で検証してから）。UI は `derived` を「入力欄にしない」判断に使う
- 一覧 `GET /v1/doc-types` は **読み込めるパッケージだけ** を返し、壊れたものは警告ログに出して外す（P5 の判断。作者が気づけるよう `/v1/doc-types/{doc_type}` の方は `500 package-broken` を返す）

## ユーザー思考

> 2026-09-12: 「1. api.md を agreed にしてよいです。2. Go（P4 の 2 分割）3. 承知（ブランチ名 feature/npc の規約不一致）4. 承認（pydantic 下限を >=2.9 に）」
> 2026-09-12: 「pipeline-and-cli の P5 実装に進めてください。」→ Do 完了後の選択肢（1: 先に P6 Check / 2: api-render の P5 へ進み Check をまとめる）に「2で進みましょう。」

## 次

- [x] P3 ゲート → `status: agreed`（2026-09-12）→ [`.agents/plans/programs/pipeline-and-cli.md`](../../../.agents/plans/programs/pipeline-and-cli.md)・[`.agents/plans/programs/api-render.md`](../../../.agents/plans/programs/api-render.md)
- [x] `docs/project-state.yaml` の `scope_focus.path` をこの文書へ
- [x] §9 Open のうち plan 側で決めるもの: 認証トークン（`api-render` の Out of scope に置き、別 plan）、`RenderTimeoutError`（`api-render` で分けた）
- [ ] P6 Check（`pipeline-and-cli` と `api-render` をまとめて。ユーザー判断 2026-09-12「2 で進みましょう」）
