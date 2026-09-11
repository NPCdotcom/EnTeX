# Plan readiness checklist

0. **P4**: `terminology-research` 済み（criteria・DoD・スコープ語）。未実施 → block。
1. `lifecycle-reference` — phase P?, scope H?, upstream gates
2. [.agents/plans/README.md](../../../plans/README.md) — path under `programs/` or `algorithms/` for Do
3. Open target plan; verify frontmatter:
   - `scope_level` is `program` or `algorithm` for **implement-conduct**
   - `pdca_eligible: true`
   - `status: agreed` for large Do（draft → block unless user allowed S0）
   - `parent_hierarchy` / Scope hierarchy table — upper H linked
4. Acceptance criteria count ≤5 for S1（else recommend split）
5. Follow `related_design`, `related_requirements`

Do not modify plans.
