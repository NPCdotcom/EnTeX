# RICE prioritization block（plan 候補 · 任意）

P4 前に **複数 H4/H5 unit 候補**があるときのみ使用。discovery（OST · 要求）の **後**（p-05）。

```markdown
## RICE 優先順位（候補 unit）

| Unit / 候補 | Reach（期間内ユーザー数） | Impact（0.25–3） | Confidence（%） | Effort（人日） | Score |
|-------------|---------------------------|------------------|-----------------|---------------|-------|
| unit-a | | | | | (R×I×C)/E |
| unit-b | | | | | |

**採用 unit**: （上表 1 位 or ユーザー Go）
```

**ICE 代替**: データ不足 · 2–3 候補のみ → Impact·Confidence·Ease を 1–10 で採点（t-05）。

正本: `adaptive-lifecycle-plan` · 学習 `t-05-prioritization-mvp.md`
