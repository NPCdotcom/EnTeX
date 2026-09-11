# Role execute — Cursor 内 skill 列実行

**Role**: PM のみ · brief の割当表 1 行ずつ。

正本: `docs/PM_ROUTING.md`

## Per row

1. Read 行の **スキル（順）** — 左から順に Cursor 内で実行
2. **Cursor 補助** — PM が WebSearch / browser / Shell 等を適用
3. 各 skill 完了後、Facts を **memory-flush** 用にメモ（ターン終端で file 化）
4. **action-evaluate** 用に trajectory（skills, tools, files）を structured に残す
5. gate=block → ユーザー確認まで conduct/record しない

## 禁止

- `Subagent`
- WSL `hermes` / Hermes MCP
- brief 無しの `*-conduct` 自己実行
- キット作業の ad-hoc スクリプト（→ `env/bin/agents-run.py` · `_SCRIPT_POLICY.md`）

## Output

各 skill の structured result + files touched + blockers

## Checklist

- [ ] context-guard + memory-reference(nav) 済み
- [ ] brief 行を実行順に処理
- [ ] P0–P4 → WebSearch + terminology-research
- [ ] ターン終端 → action-evaluate (full/mini/skip) → memory-critique (full/skip) → memory-flush → memory-record（**nav.yaml**）
