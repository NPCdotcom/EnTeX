# Skill 補助スクリプト — 実行ポリシー

正本: [`env/README.md`](../env/README.md) · 起動: `env/bin/agents-run.py`

## 目的

エージェントがターン中に **未レビューの Python/Shell をその場生成**するのを防ぎ、スキルに紐づく **確定スクリプト**だけでキット作業を進める。

## 実行経路（優先順）

| 順 | 経路 | 用途 |
|----|------|------|
| 1 | `python env/bin/agents-run.py <skill> <stem> [args]` | スキル `scripts/`（**推奨**） |
| 2 | `hooks/*.py` | Cursor preCompact/stop — **stdlib のみ** |
| 3 | プロジェクトの pytest/npm 等 | **builder** がアプリ検証するときのみ |

## 禁止（PM · role-execute · 全 role）

- ターン中の `python -c` / 一時 `.py` 新規作成・実行
- `skills/` 未登録のスクリプト実行
- キット作業をプロジェクト `.venv` に依存させる（逆も同様）
- スクリプトから秘密情報・`.env` の読取

## 新規スクリプト追加

1. `skills/<skill>/scripts/<name>.py`（薄いラッパー）
2. 重い依存は `env/python/requirements.txt` へ（`kit_maintainer`）
3. `SKILL.md` に stem 名と引数を 1 行記載
4. `python env/bin/agents-run.py <skill> <name> --help` で smoke

新規スクリプト追加後: **`maintain-scripts inventory`** + **`review`**

## スクリプト作者規約

| 項目 | 要件 |
|------|------|
| 引数 | `argparse` · `--dry-run` 推奨 |
| 書込 | `references/` に許可パスを明記 |
| 終了コード | 0=OK · 非0=失敗（監査は issue 数を返す） |
| Windows | `.py` 正本 · `.sh` は Unix オプション |

## Node

`env/node/package.json` に依存を追加したときだけ `npm` スクリプトを skill から呼ぶ。初期キットは **Python 主軸**。
