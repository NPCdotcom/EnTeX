# Memory refine — operations

| op | index 変更 | ファイル |
|----|-------------|----------|
| **archive_thread** | granularity→archive, recall→on_demand | episode 保持 |
| **supersedes** | 旧 id に supersedes、新 id を linked | alignment 等 |
| **reject_lesson** | lesson 候補を index から除外 | trace 無し禁止 |
| **merge_thread** | 同一 plan slug の thread 統合 | summary 更新 |
| **shard_index** | `index/shards/` へ分割提案 | 50+ entries |
| **append_reward** | `rewards/rollup.yaml` 更新 | 累積 turn_reward |

## Episodic vs schema（CLS 型）

- **traces/** · **episodes/** = episodic（上書き禁止、append-only）
- **knowledge/lessons/** = schema（昇格は G1–G5 + trace 必須）
- refine は **episodic を圧縮しない** — archive index のみ

## Do not

- episode 本文の削除・要約上書き
- critique 無しで lesson 作成
- global に project thread を移動
