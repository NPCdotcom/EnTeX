# Memory record — audit view（核 3 · AI-DLC audit.md 相当）

**正本ファイル**: `.agents/memory/audit/audit-log.md`（**append-only**）

## When to append

| トリガ | event_type | 必須 refs |
|--------|------------|-----------|
| `lifecycle_plan` ユーザー Go | `lifecycle_plan` | project-state · adaptive output |
| `gate_status` 更新 | `gate` | project-state · last_decision |
| `current_phase` 変更 | `phase_change` | project-state · 理由 1 行 |
| verification-questions Approval | `question_approval` | 質問ファイル path |
| P6 stage / unit 完了 | `stage_complete` | plan path · unit_scope |
| L2 flush（任意） | `turn_summary` | trace id |

**毎ターン必須ではない** — gate · phase · lifecycle · 質問承認は **必ず**記録。

## Workflow

1. イベント発生を検知（`*-record` · project-state 更新 · gate 提案確定）
2. [`assets/audit/audit-entry-template.md`](../assets/audit/audit-entry-template.md) で 1 セクション起草
3. `audit-log.md` **末尾に追記**（既存エントリの改変禁止）
4. project `index.yaml` に `tier: audit` エントリ（初回のみ · `recall: on_demand`）
5. `lifecycle_plan.executed_phases` / `skipped_phases` と **整合**させる

## Bootstrap

`audit-log.md` が無い場合:

```text
cp .agents/memory/audit/audit-log.md.example .agents/memory/audit/audit-log.md
```

## ビュー生成（読み取り）

監査レビュー時:

1. `audit-log.md` を時系列で Read
2. `docs/project-state.yaml` の `gate_status` · `lifecycle_plan` と突合
3. 必要なら trace / plan PDCA を refs から辿る

**再生成ビューは作らない** — 単一 append-only ログが正本（confabulation 防止 · s-04）。

## Do not

- audit-log の過去エントリを編集・削除
- チャットのみで監査証跡を完結
- trace 無しで lesson 昇格（既存ルール維持）

## AI-DLC 対応

| AI-DLC | キット |
|--------|--------|
| `audit.md` | `audit/audit-log.md` |
| ISO8601 | エントリ先頭タイムスタンプ |
| stage 完了承認 | `gate` + `stage_complete` |
| raw input 改変禁止 | summary は事実のみ · 推測は Assumptions と分離 |
