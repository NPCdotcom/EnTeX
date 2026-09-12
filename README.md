# EnTeX

TeX を知らない人が、フォームに入力するだけで、決められた書式どおりの PDF を崩さずに出力できる Web アプリケーション。  
概要の正本: [docs/design/product/charter.md](docs/design/product/charter.md)

## Members

| Nickname | GitHub ID | Role |
|----------|-----------|------|
| NPC | [NPCdotcom](https://github.com/NPCdotcom) | Owner / collaborator |
| Aster | [astel_isk](https://github.com/astel_isk) | Collaborator |

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

`render` の終了コード: `0` 成功 / `1` 入力の誤り（封筒・中身。日本語でまとめて標準エラーに出る）/ `2` 組版の失敗（利用者向けには汎用文だけ。TeX のログは `out/.../latexmk.log`）/ `3` doc-package の不備。

処理の流れは [docs/design/programs/renderer.md](docs/design/programs/renderer.md): `cli.py`（JSON を読む）→ `ir/loader.py`（封筒・型検証）→ `ir/derive.py`（導出値）→ `tex/escape.py`（エスケープ）→ `renderer.py`（`template.tex.j2` → latexmk）。

## Layout

| Path | Shared? | Notes |
|------|:-------:|-------|
| `src/entex/` | yes | アプリ本体（renderer / job-runner / API / CLI） |
| `packages/` | yes | 文書種パッケージ（doc-package）— 本体を変えずに増やす |
| `tests/` | yes | pytest。`fixtures/smoke.tex` は組版スモーク |
| `scripts/` | yes | 開発補助シェル |
| `Dockerfile` / `compose.yaml` / `Makefile` | yes | 開発環境定義 |
| `docs/` | yes | 概要・要求・設計・ADR・用語 |
| `schemas/` | yes | 共有スキーマ（IR 等） |
| `design/` | yes | デザイン成果物（図・モック） |
| `.agents/` | yes | AI キット（skills / rules / plans / memory 骨格） |
| `AGENTS.md` · `CLAUDE.md` | yes | AI エージェント向けの前提。`CLAUDE.md` は `AGENTS.md` へ転送するだけ |
| `.claude/` | yes | Claude Code 用のスキル・権限（`docs-sync-check` など） |
| `.github/` | yes | CI（lint/test と TeX スモーク）・PR テンプレート |
| `.coderabbit.yaml` | yes | CodeRabbit レビュー設定（日本語） |
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
- レビューが要るときは PR に `@coderabbitai review` をコメントする
- 上の3点は `.githooks/` の hook が検査する。**クローン後に一度 `make hooks`**（`make setup` からも呼ばれる）

## Docs entry

- [docs/README.md](docs/README.md)
- [docs/FIRST_PROJECT_START.md](docs/FIRST_PROJECT_START.md)
- [docs/PROJECT_LIFECYCLE.md](docs/PROJECT_LIFECYCLE.md)
- [docs/TEAM.md](docs/TEAM.md)
