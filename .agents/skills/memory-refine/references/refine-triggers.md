# Memory refine — triggers

**Run when any**:

- memory-critique `refine_needed: yes`
- action-evaluate `turn_reward < 0.6`
- memory-reason proposed **L2**
- `confabulation_risk: high`（lesson 却下優先）
- project index entries > 50（shard 提案）
- active threads > 3

**Skip when**:

- L0 flush
- 挨拶のみ · 実質変更なし
