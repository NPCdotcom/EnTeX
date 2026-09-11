# Plan record — prerequisites and blockers

## Prerequisites（すべて必須）

| Check | Source |
|-------|--------|
| Gate pass | `lifecycle-reference` — gate: pass |
| PM ユーザー確認 | `programs/` / `algorithms/` 作成前 |
| Terminology | P4 — `terminology-research` alignment 表（criteria・DoD 用語） |
| Upper H | design paths in Scope hierarchy — missing → **block** |
| Phase | `current_phase` < P3 → **block** large plan-record |

## Hard blocks

- Upper H missing in design paths
- `current_phase` < P3（`project-state.yaml`）
- Terminology alignment 未実施（P4）
- `lifecycle-reference` gate: block

## Out of scope for plan-record

| Path | Use instead |
|------|-------------|
| `docs/design/*.deliberation.md` | design-deliberate / design-record |
| `docs/requirements/` | design-record |
| Application source | implement-conduct |

## Hand off

When plan agreed and P5 ready → **builder** via `implement-reference`.
