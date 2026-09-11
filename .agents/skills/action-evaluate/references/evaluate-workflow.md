# Action evaluate — workflow

**Input**: turn-brief · nav.yaml · role-execute 結果 · `docs/project-state.yaml`（Loop2）· active thread

**Output**: turn eval YAML + trace draft → **memory-record**

**Mode**: full | mini（Loop1 read-only · Role 0）| skip（軽量）

## Steps

1. **Mode select** — lightweight → skip · Role 0 + 質問のみ → **mini** · else **full**
2. **Goal snapshot** — turn-brief 目的 · nav.next_actions · alignment（P/H/gate）
3. **Trajectory** — skill 列 · tools · files（role-execute log）
4. **Divergence** — brief vs 実際
5. **Score** — full: 4 次元 + turn_reward · mini: **process_compliance** + **nav_alignment** only
6. **Verifiable** — full mode · lint/test（あれば）
7. **Critique** — 1–3 文（full のみ · Reflexion）

## Mini mode

`turn_reward = 0.5*process_compliance + 0.5*nav_alignment` · fail ≤ 0.5 → Loop2 次ターン推奨

## Triggers for downstream

| 条件 | 次 |
|------|-----|
| `turn_reward < 0.6` | memory-critique（full）· L2 提案 |
| `nav_alignment < 0.5` | reanchor · Loop2 |
| `process_compliance < 0.5` | gate 違反 · 運用証跡 |
| context-guard pre_compact | L2 必須 |

## Do not

- mini/skip 後に memory-critique full を必須化
- nav 無視で P/H を chat から再採点
