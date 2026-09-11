# Context guard — checklist

## 1. Read nav.yaml

Path: `.agents/memory/state/nav.yaml`（missing → bootstrap from [`../../memory-reference/assets/state/nav-template.yaml`](../../memory-reference/assets/state/nav-template.yaml)）

Increment: `session.turn_estimate += 1`（memory-record で確定）

## 2. Score signals

Mark each signal yes/no. Count total.

## 3. Decide

| Outcome | Action |
|---------|--------|
| `reanchor_required` | Loop2 必須 · nav-brief · lifecycle-reference · **Edit/探索禁止** until nav pass |
| `pre_compact` | Loop1 可 · 終端 **L2 必須** · 応答末尾 **新チャット推奨** |
| Loop2 uncertain | **Run Loop2**（正確性） |
| else | Loop1 only |

## 4. Pass to memory-reference

Set Phase 0 flags in guard report:

```yaml
loop2_required: true | false
pressure_level: low | medium | high | pre_compact
reanchor_required: true | false
pre_compact_recommended: true | false
proactive_flush: L1 | L2
```

## 5. Pass to memory-record (end of turn)

Always update nav.yaml:

- `session.turn_estimate`
- `navigation.next_actions`（最大3）
- `pressure.*`
- `verification.last_verified_at`
- `updated`

On L2 / pre_compact: also `pressure.last_l2_flush_at`
