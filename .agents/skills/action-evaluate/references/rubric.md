# Action evaluate — rubric

各次元 **0.0–1.0**。アンカー:

## task_progress

| Score | 基準 |
|-------|------|
| 0.9–1.0 | brief 目的達成 · gate 前進 · ユーザー要求充足 |
| 0.6–0.8 | 部分達成 · ブロッカー明示 |
| 0.3–0.5 | 方向は正しいが未完成 |
| 0.0–0.2 | ゴール逸脱 · 未着手 |

## process_compliance

| Score | 基準 |
|-------|------|
| 0.9–1.0 | PM ループ順 · scope 遵守 · **探索型なら landscape-research（scan+drill）済** |
| 0.6–0.8 | 軽微な順序省略 |
| 0.3–0.5 | gate 無視 · 探索型で scan のみ（drill 無し） |
| 0.0–0.2 | Subagent/Hermes · index 無し memory · Loop1 で lifecycle 再分類 |

## nav_alignment（mini evaluate 必須）

| Score | 基準 |
|-------|------|
| 0.9–1.0 | 実行/brief が `nav.next_actions` · `session.intent` と一致 |
| 0.6–0.8 | 軽微なズレ · nav 更新予定あり |
| 0.3–0.5 | chat 要約と nav 矛盾 · Phase 0 未読疑い |
| 0.0–0.2 | nav 無視 · next_actions 空のまま作業 |

**mini mode**: `turn_reward = 0.5*process_compliance + 0.5*nav_alignment` · fail ≤ 0.5 → Loop2 次ターン

| Score | 基準 |
|-------|------|
| 0.9–1.0 | 引用 memory id が recall リストに存在 · docs と一致 |
| 0.6–0.8 | 一部 Assumption · 未記録 Fact なし |
| 0.3–0.5 | 記憶未参照で推測実行 |
| 0.0–0.2 | 矛盾する memory を Fact 化 |

## verifiable_pass

| Score | 基準 |
|-------|------|
| 1.0 | 全 verifiable checks pass |
| 0.5 | 一部 pass / 未実行 |
| 0.0 | fail または regressions |

## turn_reward（デフォルト加重）

```
turn_reward = 0.35*task_progress + 0.25*process_compliance
            + 0.25*memory_grounding + 0.15*verifiable_pass
```

memory-critique 後に `memory_grounding` を上書き可。
