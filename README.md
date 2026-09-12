# EnTeX

TeX を知らない人が、決められた項目を埋めて本文を Markdown で書くか、フォームに入力するだけで、決められた書式どおりの PDF を崩さずに出力できる Web アプリケーション。  
概要の正本: [docs/design/product/charter.md](docs/design/product/charter.md)

## Members

| Nickname | GitHub ID | Role |
|----------|-----------|------|
| NPC | [NPCdotcom](https://github.com/NPCdotcom) | Owner / collaborator |
| Aster | [Astel-isk](https://github.com/Astel-isk) | Collaborator |

## Repository

- HTTPS: https://github.com/NPCdotcom/EnTeX.git
- SSH: `git@github.com:NPCdotcom/EnTeX.git`
- Default branch: `main`

## Stack

| 層 | 選定（charter §7） |
|----|--------------------|
| バックエンド | Python 3.12+ · FastAPI · pydantic · Jinja2 · Typer(CLI) |
| 組版 | LuaLaTeX + luatexja（latexmk 経由）— **コンテナ内のみ** |
| フロント | React（着手順 4 で追加。まだ無い） |
| 開発環境 | WSL2 Ubuntu + Docker（単一イメージ `entex-dev`） |

## Development

### 1. WSL 側にクローンする（重要）

TeX は中間ファイルを大量に書くため、`/mnt/c` 配下（Windows ディレクトリのバインドマウント）だとコンパイルが大幅に遅くなります。**開発コードは WSL のファイルシステムに置く**（charter §7）。

```bash
wsl -d Ubuntu
git clone git@github.com:NPCdotcom/EnTeX.git ~/EnTeX
cd ~/EnTeX
```

Windows 側のクローン（Cursor で開いているもの）はドキュメント編集用に残して構いません。両方で `git pull` してください。

### 2. コンテナ（Python + TeX）

```bash
make docker-build    # 初回のみ。TeX Live を apt で入れるので数分かかる
make docker-doctor   # lualatex / latexmk / luatexja が見えるか
make tex-smoke       # tests/fixtures/smoke.tex → out/smoke/smoke.pdf（日本語組版の確認）
make docker-test     # pytest（TeX を使うテスト込み）
make docker-serve    # API を http://localhost:8000 で起こす（下の「API」節）
make docker-shell    # 中に入って作業
```

### 3. ホスト側だけ（TeX 不要の lint / 単体テスト）

```bash
make setup           # .venv 作成 + `pip install -e ".[dev]"`
make lint
make test            # TeX 依存テストは自動 skip
```

### CLI

```bash
entex version
entex doctor         # コンテナ内で実行
entex render packages/circle-monthly-report/examples/valid/01-typical.json   # コンテナ内で実行
# → out/render/01-typical/01-typical.pdf（.tex と latexmk.log も同じ場所に残る）
entex render <json> --out DIR            # 出力先を指定
entex render <json> --tex-only           # latexmk を呼ばず .tex だけ書く（TeX の無いホストで確認するとき）
```

`render` の終了コード: `0` 成功 / `1` 入力の誤り（封筒・中身。日本語でまとめて標準エラーに出る）/ `2` 組版の失敗（利用者向けには汎用文だけ。TeX のログは `out/.../latexmk.log`）/ `3` doc-package の不備（`schema.json` / `template.tex.j2` の欠落など）。

出力ディレクトリは JSON のファイル名のまま（`out/render/<ファイル名>/`）だが、`.tex` / `.pdf` の名前は latexmk に安全な文字（英数字・`-`・`_`、先頭は英数字、64 文字まで）へ寄せる。例: `報告 8月.json` → `out/render/報告 8月/8.pdf`、`報告書.json` → `out/render/報告書/document.pdf`。

処理の流れは [docs/design/programs/renderer.md](docs/design/programs/renderer.md): `cli.py`（JSON を読む）→ `pipeline.py`（共通入口。CLI も API もここを通る）→ `ir/loader.py`（封筒・型検証）→ `ir/derive.py`（導出値）→ `renderer.py`（`tex/escape.py` でエスケープ → `template.tex.j2` → latexmk）。

### API（着手順 2）

```bash
make docker-serve    # http://localhost:8000（コンテナの CMD も同じ uvicorn）
curl -sS -X POST http://localhost:8000/v1/render \
     -H 'Content-Type: application/json' \
     --data-binary @packages/circle-monthly-report/examples/valid/01-typical.json \
     -o report.pdf -D -          # ヘッダを表示しつつ PDF を保存
curl -sS http://localhost:8000/v1/health       # {"status":"ok"|"degraded","version":…,"toolchain":{…}}
curl -sS http://localhost:8000/v1/doc-types    # [{"doc_type":"circle-monthly-report","schema_version":1,"title":"…"}]
```

| メソッド / パス | 成功 | 失敗 |
|---|---|---|
| `POST /v1/render`（IR の JSON） | `200` `application/pdf`。`Content-Disposition` に ASCII の `filename` と UTF-8 の `filename*` | `400` 本文が JSON でない · `413` 本文過大 · `415` `Content-Type` 不一致 · `422` 封筒 / 中身の誤り · `500` 組版失敗 / 時間切れ / パッケージ不備 · `503` 混雑（`Retry-After`） |
| `GET /v1/health` | `200 {"status":"ok"}` | `503 {"status":"degraded"}`（TeX 不在） |
| `GET /v1/doc-types` · `GET /v1/doc-types/{doc_type}` | 一覧 / `schema.json` の内容 | `404` |

失敗はすべて [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html)（`application/problem+json`）。`type` の末尾（`ir-invalid` / `envelope-mismatch` / `render-failed` / …）で機械判別し、`detail` は日本語の完成文、`ir-invalid` だけ `issues[]`（`path` / `message`）を持つ。TeX のログは応答に出ず、サーバ側ログに `X-Request-ID`（応答ヘッダにも入る。`instance` は `urn:uuid:<同じ ID>`）付きで残る。OpenAPI は `/openapi.json`（生成物は `schemas/api/openapi.json`、`make schemas` で再生成）。

環境変数（既定値）: `ENTEX_PACKAGES_DIR`（`./packages`）· `ENTEX_WORK_DIR`（システム tmp）· `ENTEX_RENDER_TIMEOUT`（`60` 秒）· `ENTEX_MAX_CONCURRENT_RENDERS`（CPU 数）· `ENTEX_QUEUE_WAIT_SECONDS`（`5`）· `ENTEX_MAX_BODY_BYTES`（`1048576`）· `ENTEX_KEEP_FAILED_JOBS`（`0`。`1` で失敗ジョブの一時ディレクトリを残す）。設計は [docs/design/programs/api.md](docs/design/programs/api.md)。認証はまだ無い（公開配置の前に別 plan）。

## Layout

| Path | Shared? | Notes |
|------|:-------:|-------|
| `src/entex/` | yes | アプリ本体（renderer / job-runner / API / CLI） |
| `packages/` | yes | 文書種パッケージ（doc-package）— 本体を変えずに増やす |
| `tests/` | yes | pytest。`fixtures/smoke.tex` は組版スモーク |
| `scripts/` | yes | 開発補助シェル |
| `Dockerfile` / `compose.yaml` / `Makefile` | yes | 開発環境定義 |
| `docs/` | yes | 概要・要求・設計・ADR・用語 |
| `schemas/` | yes | 共有スキーマ（IR の封筒・API の OpenAPI / Problem Details）。`make schemas` で再生成 |
| `design/` | yes | デザイン成果物（図・モック） |
| `.agents/` | yes | AI キット（skills / rules / plans / memory 骨格） |
| `AGENTS.md` · `CLAUDE.md` | yes | AI エージェント向けの前提。`CLAUDE.md` は `AGENTS.md` へ転送するだけ |
| `.claude/` | yes | Claude Code 用のスキル・権限（`docs-sync-check` など） |
| `.github/` | yes | CI（lint/test と TeX スモーク）・PR テンプレート |
| `out/` · `.venv/` · `.env` · `.cursor` junctions | no | 生成物・秘密情報（`.gitignore`） |

`.gitignore` に **独自 AI アセットは載せません**。共同者がドキュメント・スキーマ・デザイン・エージェント資産を同じリポジトリで共有できるようにしています。

## First-time setup (collaborators)

```bash
git clone git@github.com:NPCdotcom/EnTeX.git
cd EnTeX

# Cursor 用 junction（Windows PowerShell）
.\.agents\scripts\link-cursor.ps1

# または WSL / Unix
./.agents/scripts/link-cursor.sh

# 任意: エージェント実行用 venv
# Windows: .\.agents\env\bin\setup.ps1
# Unix:    ./.agents/env/bin/setup.sh
```

## Contributing

運用ルールの正本は [AGENTS.md](AGENTS.md)（「プロジェクト運用」節）。要点だけ:

- **`main` で直接作業しない。** 作業ブランチ → PR → `main`
- ブランチ名: `issue番号/担当者/やること`（例: `7/aster/cli_render_json`）
- コミット: `接頭辞:やったこと`（コロンの後に空白なし。`feat` / `fix` / `docs` / `refact` / `chore` など）
- PR を出す前に `make lint` と `make test` を通す（TeX を触ったときは `make docker-test` と `make tex-smoke` も）
- レビューはもう一方に依頼する（担当領域は [docs/TEAM.md](docs/TEAM.md)）。自動レビューは入れていない
- 上の3点は `.githooks/` の hook が検査する。**クローン後に一度 `make hooks`**（`make setup` からも呼ばれる）

## Docs entry

- [docs/README.md](docs/README.md)
- [docs/FIRST_PROJECT_START.md](docs/FIRST_PROJECT_START.md)
- [docs/PROJECT_LIFECYCLE.md](docs/PROJECT_LIFECYCLE.md)
- [docs/TEAM.md](docs/TEAM.md)
