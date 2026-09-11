# Design reference — read order

0. **P0–P3**: PM が `terminology-research`（WebSearch + browser）を **先に** 実行済みか確認。未実施 → block。

## Paths

1. [docs/PROJECT_LIFECYCLE.md](../../../docs/PROJECT_LIFECYCLE.md) — H0–H5
2. `docs/requirements/` — per-slug `要求.md` / `要件.md` status
3. [docs/design/README.md](../../../../docs/design/README.md) — product/, elements/, systems/, frameworks/, programs/
4. IaC / クラウド: [docs/design/_template/infrastructure/](../../../../docs/design/_template/infrastructure/README.md) → 利用先 `docs/design/systems/<slug>/`（G9 · o-06）
5. Search; prefer `status: agreed` on current `scope_level`
6. Cite path + section; Facts / Assumptions / Open

## Order

`docs/glossary/` → `docs/requirements/` → `docs/design/`（H0→H5）→ `docs/adr/`

For plans: **plan-reference**. For gates: **lifecycle-reference**.

Do not modify files.
