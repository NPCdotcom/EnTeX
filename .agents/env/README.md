# Agent 実行環境（`.agents/env/`）

**用途**: エージェント作業専用ツールチェーン。**プロジェクトの `.venv` / `node_modules` とは別**。

| 層 | パス | 役割 |
|----|------|------|
| Python | `env/python/` | スキル補助スクリプト（監査・YAML 等） |
| 共有ロジック | `env/python/lib/` | `kit_paths` 等 — スキル script から import |
| Node | `env/node/` | 将来の CLI ラップ（段階導入） |
| 起動 | `env/bin/agents-run.py` | スキル `scripts/` の推奨入口 |
| Hooks | `hooks/` | Cursor hook — **stdlib のみ**（env 非依存） |

## 初回セットアップ

```powershell
# キットルート（%USERPROFILE%\.agents または project\.agents）で
.\env\bin\setup.ps1
```

```bash
./env/bin/setup.sh
```

作成物（git 除外）:

- `env/python/.venv/`
- `env/node/node_modules/`（`package.json` に依存がある場合）

## スクリプト実行（エージェント向け）

```powershell
python env/bin/agents-run.py maintain-scripts inventory skills
python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills
```

```bash
python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills
```

形式: `agents-run <skill名> <script-stem> [引数…]`  
解決: `skills/<skill>/scripts/<stem>.{py,ps1,sh}`

## ガバナンス

正本: [`skills/_SCRIPT_POLICY.md`](../skills/_SCRIPT_POLICY.md)

- **禁止**: ターン中の ad-hoc `python -c` / 未登録スクリプト新規作成
- **許可**: `SKILL.md` に列挙された `scripts/` + `agents-run` 経由
- **新規スクリプト**: `kit_maintainer` + `maintain-record` · 追加後 `maintain-scripts inventory`

## Python / Node の使い分け

| 用途 | ランタイム |
|------|-----------|
| 監査・ファイル走査・YAML patch | Python 3.12（`env/python/.venv`） |
| Cursor hooks | システム Python 3 · stdlib のみ |
| Markdown AST · npm CLI ラップ | Node 20+（必要時のみ `env/node`） |
| アプリのテスト・ビルド | **プロジェクト環境**（ここではない） |

## バージョン

- Python: **3.12**（`env/python/.python-version`）
- Node: **20 LTS**（`env/node/package.json` `engines`）
