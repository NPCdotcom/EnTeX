---
name: docs-sync-check
description: Check whether EnTeX docs (charter, AGENTS.md, README, packages/schemas READMEs) still match the actual repo implementation — stack versions, doc-package layout, IR schemas, design invariants, cross-doc links. Use when asked to verify docs are up to date, check docs against implementation, or before a docs-related commit/PR in this repo.
---

# docs-sync-check

このリポジトリ(EnTeX)の `docs/`・`AGENTS.md`・`README.md` が実装と食い違っていないかを確認するチェックリスト。charter は「何を作るか」の正本であり、実装とのズレは他のどんな不整合よりも実害が大きい(設計の合否判定そのものが charter に書かれているため)。

## 実行手順

以下を順番にチェックし、最後にズレをまとめて報告する。**勝手に修正しない** — 見つかった不一致は報告し、直すかどうか・どちらを正とするかはユーザーに確認する。既定の考え方は「charter は人が決めたことなので charter が正、ただし事実関係(バージョン・パス・コマンド)は実装が正」。

### 1. 設計不変条件の逸脱(最優先)

charter §4・§6 の4点が守られているかをコードで確かめる。

```bash
ls packages/
grep -rn "packages/" src/entex/ || true
grep -rniE "latexmk|lualatex|\.log" src/entex/ || true
```

- **文書種を足すのに `src/entex/` を変えていないか**: `git log --oneline -- packages/ src/entex/` を見て、doc-package の追加コミットが `src/entex/` を巻き込んでいないか。文書種が2つになった時点がこの判定のタイミング(charter §6)
- **`renderer` が IR の出どころを知らないか**: renderer 側のコードに form / CSV / DB / HTTP リクエストへの依存が入っていないか
- **利用者に TeX を見せていないか**: latexmk のログ・`.tex` の内容が、CLI の標準出力や API のレスポンスへそのまま流れる経路がないか
- **用語**: 「テンプレート」が `.tex.j2` 以外(パッケージ全体・スキーマ)を指して使われていないか(charter §10)

### 2. スタック・バージョンの一致

```bash
grep -nE "requires-python|python_requires|^version" pyproject.toml
grep -nE "^FROM|texlive|latexmk" Dockerfile
```

`pyproject.toml`(`requires-python`・依存)と `Dockerfile`(ベースイメージの Python・TeX パッケージ)を、`README.md` §Stack・`AGENTS.md`「Project / Stack docs」・charter §7 の記述と突き合わせる。バージョンの数字の食い違い(例: README が 3.12、イメージが 3.13)は報告する。

### 3. doc-package のレイアウト

`packages/README.md` が示す構成(`schema.json` / `template.tex.j2` / `style/` / `README.md`)と、実際の `packages/<slug>/` の中身を比較する。まだ文書種が1つも無い段階なら「未作成(着手順1の前)」として現在地を報告し、実装漏れとして扱わない。

### 4. IR スキーマと pydantic モデル

`schemas/` 配下のスキーマと `src/entex/` の pydantic モデルを突き合わせる。フィールド名・必須/任意・型が一致しているか、片方にしかないフィールドがないか。`schemas/README.md` の「予定」に書かれた構成(`ir/`・`api/`)と実際のディレクトリのズレも見る。

### 5. コマンドの実在

README・AGENTS.md・CLAUDE.md に書かれたコマンドが実在するか。

```bash
grep -nE '^[a-zA-Z_-]+:' Makefile
grep -rn "@app.command" src/entex/cli.py
```

- `make` ターゲット(`setup` / `lint` / `test` / `docker-*` / `tex-smoke`)がドキュメントの記述と一致しているか
- `entex <subcommand>` として案内されているものが CLI に実在するか(未実装のものは「着手順◯で入る」と明記されているか)

### 6. ドキュメント間の相互参照

```bash
grep -noE '\[[^]]*\]\([^)]+\)' AGENTS.md CLAUDE.md README.md docs/*.md docs/**/*.md | head -100
```

- リンク先のファイルが実在するか(`docs/README.md` の目次・`AGENTS.md` のドキュメント索引を特に見る)
- `docs/` に存在するのに索引へ載っていないファイルがないか
- charter の節番号への参照(§4・§6・§7・§10・§11)が、charter の実際の節とずれていないか

### 7. フェーズ表示の一致

`docs/project-state.yaml`(`current_phase` / `gate_status`)と `.agents/memory/state/nav.yaml`(`alignment` ブロック)が同じフェーズを指しているか。ズレていたら、どちらが新しいかを日付で示して報告する。

## 報告フォーマット

チェック項目ごとに一致/不一致を短くまとめ、不一致のみ詳細(該当ファイル・行、doc 側の記述、実装側の状態)を添える。全部一致していれば「一致」とだけ簡潔に報告し、余計な前置きをしない。
