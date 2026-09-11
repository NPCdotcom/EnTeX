# Plan evaluate — audit workflow

**Role**: `evaluator` · **P6 Act** · One plan file.

After `evaluate-reference`:

1. Audit each acceptance criterion（met / partial / blocked + evidence）
2. PDCA log vs actual work
3. Scope drift vs `scope_level` and H hierarchy（[PROJECT_LIFECYCLE.md](../../../docs/PROJECT_LIFECYCLE.md)）
4. Criteria partially met or count >5 → recommend **plan split**（new file under `programs/` or `algorithms/`）
5. Verdict: `on_track` | `at_risk` | `blocked`
6. If blocked → PM user confirm or phase rollback P3/P2

Recommend next role（e.g. plan_slicer, spec_designer）— not Subagent.

Optional: **evaluate-record**
