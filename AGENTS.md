# EnTeX — Agent Guide

> Kit: [.agents/README.md](.agents/README.md) · Tiers: [.agents/docs/CONTEXT_TIERS.md](.agents/docs/CONTEXT_TIERS.md)

## PM (IDE + external memory)

**No Subagents** · **No Hermes** · Memory: `.agents/memory/`

| Layer | Canonical |
|-------|-----------|
| L0 gate | `rules/secretary-gate` · `rules/no-subagents` |
| Every turn | `pm-turn-start` → `role-execute` → `pm-turn-end` · [PM_ROUTING.md](.agents/docs/PM_ROUTING.md) · `nav.yaml` |
| Loop2 | [PM_ROUTING.md](.agents/docs/PM_ROUTING.md) §Loop2 · `project-state.yaml` |

Roles: [CURSOR_ROLES.md](.agents/docs/CURSOR_ROLES.md) · Catalog: `skills/role-skill-catalog`

User chat: **Japanese** · Kit canon: **English** — [LANGUAGE_POLICY.md](.agents/docs/LANGUAGE_POLICY.md)

---

## Project

| Field | Value |
|-------|-------|
| Name | **EnTeX** |
| Description | Form input → fixed-format PDF via LaTeX, for people who do not write TeX. Charter: [docs/design/product/charter.md](docs/design/product/charter.md) |
| Stack | Python 3.12+ · FastAPI · pydantic · Jinja2 · Typer · LuaLaTeX+luatexja (container only) · React (later) |
| Dev env | WSL2 Ubuntu + Docker single image `entex-dev` · clone under WSL FS (`~/EnTeX`), not `/mnt/c` |
| Members | NPC (`NPCdotcom`) · Aster (`astel_isk`) |

## Stack docs

| Topic | Link |
|-------|------|
| Language / runtime | Python 3.13 in image (`python:3.13-slim`) · `pyproject.toml` · run TeX-dependent code via `make docker-*` |
| Framework | FastAPI (API, roadmap step 2) · Typer CLI (`src/entex/cli.py`, step 1) · Jinja2 → `.tex` · latexmk `-lualatex` |
| Style | Ruff (`line-length 100`, `E F I B UP`) · LF endings (`.gitattributes`) · `.editorconfig` |

## Design invariants (from charter)

- `renderer` must not know where the IR came from (`data-import` stays separable).
- Adding a doc-package must require **zero** changes under `src/entex/` — judged when the 2nd doc-package lands.
- Users never see TeX, including error logs.
- "テンプレート" = the `.tex.j2` file only; the whole bundle is a "パッケージ".

## Lifecycle

[PROJECT_LIFECYCLE.md](docs/PROJECT_LIFECYCLE.md) · `docs/project-state.yaml` · `.agents/memory/index.yaml`

## Shared paths

| Path | Purpose |
|------|---------|
| `docs/` | Requirements, design, ADR, glossary |
| `schemas/` | Shared schemas |
| `design/` | Design artifacts (non-doc) |
| `.agents/` | Shared agent kit (skills, rules, plans, memory scaffolding) |

## Principles

- Deterministic boundaries; share docs/schemas/design via git
- Agent kit assets are **tracked** (not gitignored) for collaborator sync
- Application secrets and generated runtimes stay local

---

# プロジェクト運用（日本語）

ここから下は EnTeX 固有の運用ルール。上のキット案内が English canon なのに対し、以下は charter・README と同じく日本語で書く（読む相手が我々2人であるため）。

## ドキュメント索引

作業前に該当するものを読むこと。

| 知りたいこと | 読むファイル |
|---|---|
| 何を作っているか・目的と非目的・成功の目安 | [docs/design/product/charter.md](docs/design/product/charter.md) |
| 着手順（CLI → API → 2つ目の文書種 → UI → CSV） | charter §11 |
| 用語（パッケージ / テンプレート / IR / 文書種） | charter §10 |
| 文書種パッケージの中身と置き方 | [packages/README.md](packages/README.md) |
| IR・API スキーマの置き場 | [schemas/README.md](schemas/README.md) |
| 開発環境の立ち上げ・make ターゲット | [README.md](README.md) §Development · `Makefile` |
| 今どのフェーズか・ゲートの状態 | [docs/project-state.yaml](docs/project-state.yaml) · [docs/PROJECT_LIFECYCLE.md](docs/PROJECT_LIFECYCLE.md) |
| 誰が何を担当するか | [docs/TEAM.md](docs/TEAM.md) |
| 設計判断の記録 | `docs/adr/` |

## Git 運用

- **main で作業しない**。変更は必ず作業ブランチを切り、PR 経由で main へマージする（2026/9/12 決定。dip_distributed_llm の運用に揃えたが、人数が2人なので `develop` は挟まない）
- ブランチ名: `issue番号/担当者/やること`（例: `7/aster/cli_render_json`）。担当者は `aster` / `npc` を使う
- コミットメッセージ: `接頭辞:やったこと`（**コロンの後に空白を入れない**）
  - 接頭辞: `feat`(新機能) / `ui`(UI変更) / `remove`(削除) / `fix`(修正) / `docs`(ドキュメントのみ) / `style`(挙動に影響しない整形) / `refact`(リファクタリング) / `perf`(パフォーマンス改善) / `test`(テスト) / `wip`(作業途中) / `chore`(ビルド・ツール・依存など雑多)
  - 例: `feat:JSONから.texを組み立てる`、`fix:日本語のエスケープ漏れを直す`
  - scaffold 期の履歴（`docs: ...` 形式）は書き換えない。今後のコミットから適用する
- PR タイトルも同じ接頭辞を付け、末尾に issue 番号を添える（例: `feat:CLIでJSONからPDFを出す(#7)`）
- 開発フロー: `main` を最新化 → 作業ブランチ作成 → 実装 → commit → `git push origin <ブランチ名>` → GitHub で PR → main へマージ
- 上の3つ（main で作業しない / ブランチ名 / コミットの接頭辞）は `.githooks/` の hook が機械検査する。**クローンしたら一度 `make hooks` を実行する**（`make setup` からも呼ばれる）
  - git には「ブランチ作成」の hook が無いため、ブランチ名が落ちるのは `checkout -b` の瞬間ではなく最初の push である
  - 規則の正はこの節であり、hook はその機械検査にすぎない。規則を変えたら `.githooks/` も同じ PR で直す
- 改行コードは LF 固定（`.gitattributes`）。ローカルが CRLF になっていて改行コードだけの差分が出たファイルは `git checkout --` で戻し、コミットに含めない

## 設計前提に反しそうな場合

上の「Design invariants」は charter から来た確定事項である。反する実装をしようとしていることに気づいたら、そのまま進めずに一度止まってユーザーに確認すること。特に次の2つは黙って破らない。

- 文書種を1つ足すのに `src/entex/` を変更している（charter §6 の合否判定そのもの）
- `renderer` が IR の出どころ（フォーム / CSV / DB）を知っている

## ファイルをコンテキストに読み込む際の注意

- `out/` 配下の生成物を全文読み込まない。latexmk のログは失敗箇所の周辺だけを見る（`scripts/tex-smoke.sh` は末尾40行だけ出す）
- PDF・フォント（`.ttf` / `.otf`）はバイナリ。読まない
- コンテナ内の TeX Live 本体（`/usr/share/texmf*`）を読まない。必要なのは `kpsewhich` で場所を確かめることだけ
- `.venv/` · `__pycache__/` · `node_modules/` は読まない
- `.agents/` 配下のテンプレート群は該当する1枚だけ開く。ディレクトリごと読まない

## コーディング規約

- Python 3.12+。型注釈を付け、モジュール冒頭で `from __future__ import annotations` を使う
- Ruff（`line-length 100`、`E F I B UP`）。整形は `make fmt`、検査は `make lint`
- **利用者の入力は必ずエスケープを通してから TeX へ渡す**。Jinja2 テンプレートに生の値を書き込まない
- **利用者向けのエラーに TeX のログを出さない**（charter §4）。latexmk の失敗は日本語の要約へ変換し、原文はサーバ側のログに残す
- IR は pydantic モデルで定義し、`schemas/` の内容と食い違った状態でコミットしない
- 体裁に関わる値（フォント・余白・罫線）は `src/entex/` ではなく doc-package 側に置く
- コメント・コミットメッセージは日本語で構わない。識別子とパスは英語

## テストを書く基準

以下に該当する変更は、実装と同じ PR でテストも書く。

- IR スキーマ（pydantic モデル・`schemas/`）の追加・変更
- TeX エスケープ処理と `.tex` の組み立て
- doc-package の読み込み・検証（想定どおりのディレクトリでないときに落ちること）
- 生成の失敗が利用者向けメッセージへ変換されること（TeX ログが漏れないこと）

以下は原則テスト不要。

- ドキュメントのみの変更
- 見た目の微調整（余白・罫線など、生成 PDF を目で見れば足りるもの）

## PR を出す前のローカル検査

CI とレビューを検査の代わりにしない。手元で次を通してから PR を出す。

```bash
make lint          # Ruff
make test          # pytest（TeX 依存テストは skip）
make docker-test   # pytest（TeX 込み）— renderer や Dockerfile を触ったとき
make tex-smoke     # 日本語組版が通るか — テンプレート・スタイルを触ったとき
```

## レビュー（CodeRabbit）

- 設定は [.coderabbit.yaml](.coderabbit.yaml)（日本語レビュー）
- スター数の少ないリポジトリは自動レビューが走らないことがある。**PR を出すたび・修正を push するたびに、PR コメントへ `@coderabbitai review` を明示投稿する**
- 無料枠で `Review rate limited` になることがある。レビューが来ない前提で進め、来たら拾う

## ハーネス（AI エージェント側の設定）

| パス | 用途 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | Claude Code の入口。中身はこの AGENTS.md へ転送している |
| `.claude/skills/docs-sync-check/` | `docs/`・`AGENTS.md` と実装のズレを点検するスキル |
| `.claude/settings.local.json` | ローカルの権限許可 |
| `.github/workflows/ci.yml` | lint / test（ホスト）と TeX スモーク（Docker） |
| `.github/pull_request_template.md` | PR の定型（関連 issue・ローカル検査・設計前提の確認） |
| `.githooks/` | Git 運用の機械検査（`commit-msg` 接頭辞 / `pre-commit` main 直コミット / `pre-push` main への push とブランチ名）。`make hooks` で有効化 |
