# Project documentation

| Path | Purpose |
|------|---------|
| [FIRST_PROJECT_START.md](FIRST_PROJECT_START.md) | 最初の 1 プロジェクトの起動手順（汎用） |
| [PROJECT_LIFECYCLE.md](PROJECT_LIFECYCLE.md) | Phases P0–P6, scope H0–H5, PDCA rules |
| [project-state.yaml](project-state.yaml) | Current phase / scope focus / gates |
| [TEAM.md](TEAM.md) | Members (NPC / Aster) |
| [design/](design/) | H0–H5 design。製品の正本は [design/product/charter.md](design/product/charter.md) |
| [design/elements/ir-type-vocabulary.md](design/elements/ir-type-vocabulary.md) | IR の型の語彙（月次報告書を題材に精査。[ADR-0001](adr/0001-first-doc-type-pivot-to-meeting-log.md)によりAssumptionsは要再判定） |
| [requirements/circle-monthly-report/要求.md](requirements/circle-monthly-report/要求.md) | P1 要求 — サークル月次活動報告書。**参考資料**（[ADR-0001](adr/0001-first-doc-type-pivot-to-meeting-log.md)で最初の文書種を部会ログのフォーマット化へ差し替え済み） |
| [requirements/circle-monthly-report/要件.md](requirements/circle-monthly-report/要件.md) | P2 要件 — 同上、検証可能な機能・非機能要件。**参考資料**（同上） |
| [adr/0001-first-doc-type-pivot-to-meeting-log.md](adr/0001-first-doc-type-pivot-to-meeting-log.md) | 最初の文書種をサークル月次報告書から部会ログのフォーマット化へ差し替えた決定（issue #11） |
| [design/programs/renderer.md](design/programs/renderer.md) | P3 基本設計（H4）— renderer のモジュール分割・インターフェース・エラー方針・仮レイアウト方針 |
| [design/programs/api.md](design/programs/api.md) | P3 基本設計（H4、draft）— 着手順 2 API 化。共通パイプライン関数・`POST /v1/render`・RFC 9457 エラー応答・実行モデル |
| [reviews/2026-09-12-renderer-cli-p6-review.md](reviews/2026-09-12-renderer-cli-p6-review.md) | P6 レビュー — renderer / CLI 実装（PR #8）の V-model RTM と判定（pass） |
| [adr/](adr/) | Architecture decisions |
| [glossary/](glossary/) | Terms |
| [evaluations/](evaluations/) | Evaluation records |
| [reviews/](reviews/) | Review records |
| [../schemas/](../schemas/) | Shared schemas（IR / API） |
| [../design/](../design/) | Design artifacts（図・モック） |

P4 実装計画（renderer.md「次」の分割案どおり）:

- [.agents/plans/algorithms/ir-validate-and-derive.md](../.agents/plans/algorithms/ir-validate-and-derive.md) — FR1–FR4（H5。TeX 非依存）
- [.agents/plans/programs/render-and-cli.md](../.agents/plans/programs/render-and-cli.md) — FR5–FR8・NFR1–2（H4）

未作成（必要になった段階で作る）:

- `LINEAR_PHASE_MAP.md` — Linear states ↔ P/H（optional。`project-state.yaml` の `linear_sync.map_doc` が参照している）

Plans: [.agents/plans/](../.agents/plans/README.md)
Kit: [.agents/README.md](../.agents/README.md)
Agent guide: [../AGENTS.md](../AGENTS.md)

キットから持ち込んだ雛形を本番の成果物にするときは、`sample-*` / `example-*` のスラッグを先に改名する。
