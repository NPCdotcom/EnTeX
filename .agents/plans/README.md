# Plans Index

**実装計画（P4+）** の正本。思案・仕様: `docs/design/`。要求・要件: `docs/requirements/`。

ライフサイクル: [docs/PROJECT_LIFECYCLE.md](../docs/PROJECT_LIFECYCLE.md)

## フォルダ（スコープ階層）

| フォルダ | scope_level | PDCA Do |
|----------|-------------|---------|
| `product/` | H0 | 通常しない（`pdca_eligible: false`） |
| `elements/` | H1 | 通常しない |
| `systems/` | H2 | 通常しない |
| `elements/` | H1 | 通常しない |
| `systems/` | H2 | 通常しない |
| `frameworks/` | H3 | S0 スパイクのみ |
| `programs/` | H4 | **主戦場** |
| `algorithms/` | H5 | **主戦場** |

**原則**: 1 plan = 1 PDCA サイクル（S0 or S1）。program / algorithm が主；それ以外はユーザー確認 + `pdca_eligible: false`。

## Actions

| Action | Skill / Agent |
|--------|----------------|
| Readiness | `plan-reference`, `lifecycle-reference` |
| Record | `plan-record` |
| Mid-plan evaluation | `plan-evaluate`, **`evaluator`** |
| Bundled | **`plan_slicer`** |

Template: [_template.md](_template.md)  
Example（中立・削除可）: [_example/](_example/)

## Plans

| Plan | scope_level | Status | Summary |
|------|-------------|--------|---------|
| [algorithms/ir-validate-and-derive](algorithms/ir-validate-and-derive.md) | H5 algorithm | agreed（Check pass） | 封筒・型検証・導出値計算（FR1–FR4、TeX 非依存） |
| [programs/render-and-cli](programs/render-and-cli.md) | H4 program | agreed（Check pass） | エスケープ・テンプレ組み立て・latexmk・CLI `render`（FR5–FR8、NFR1–2） |
| [programs/pipeline-and-cli](programs/pipeline-and-cli.md) | H4 program | agreed（Check pass） | `entex.pipeline.render_ir()` を導入し CLI を乗せ替え。P6 レビュー W1 / W2 / S1 / S3 を吸収 |
| [programs/api-render](programs/api-render.md) | H4 program | agreed（Check pass） | `POST /v1/render` → PDF、RFC 9457 Problem Details、health / doc-types（着手順 2） |

Rules: `planning`, `plans-content`, `project-lifecycle`
