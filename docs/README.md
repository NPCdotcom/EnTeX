# Project documentation

| Path | Purpose |
|------|---------|
| [FIRST_PROJECT_START.md](FIRST_PROJECT_START.md) | 最初の 1 プロジェクトの起動手順（汎用） |
| [PROJECT_LIFECYCLE.md](PROJECT_LIFECYCLE.md) | Phases P0–P6, scope H0–H5, PDCA rules |
| [project-state.yaml](project-state.yaml) | Current phase / scope focus / gates |
| [TEAM.md](TEAM.md) | Members (NPC / Aster) |
| [design/](design/) | H0–H5 design。製品の正本は [design/product/charter.md](design/product/charter.md) |
| [design/elements/ir-type-vocabulary.md](design/elements/ir-type-vocabulary.md) | IR の型の語彙（12型。§1〜§5 は月次報告書、§2.8 の `document` と §7 は部会ログの実物47本に基づく）。`schema.json` の形式と `schema_version` を上げる基準もここ |
| [requirements/club-meeting-log/要求.md](requirements/club-meeting-log/要求.md) | P1 要求 — サークル部会ログ。最初の文書種（charter §5 の MVP）。実物47本の全数集計だけを材料にしている |
| [requirements/circle-monthly-report/要求.md](requirements/circle-monthly-report/要求.md) | P1 要求 — サークル月次活動報告書。**参考資料**（[ADR-0001](adr/0001-first-doc-type-pivot-to-meeting-log.md)で最初の文書種を部会ログのフォーマット化へ差し替え済み） |
| [requirements/circle-monthly-report/要件.md](requirements/circle-monthly-report/要件.md) | P2 要件 — 同上、検証可能な機能・非機能要件。**参考資料**（同上） |
| [adr/0001-first-doc-type-pivot-to-meeting-log.md](adr/0001-first-doc-type-pivot-to-meeting-log.md) | 最初の文書種をサークル月次報告書から部会ログのフォーマット化へ差し替えた決定（issue #11） |
| [design/programs/renderer.md](design/programs/renderer.md) | P3 基本設計（H4）— renderer のモジュール分割・インターフェース・エラー方針・仮レイアウト方針 |
| [design/programs/api.md](design/programs/api.md) | P3 基本設計（H4、draft）— 着手順 2 API 化。共通パイプライン関数・`POST /v1/render`・RFC 9457 エラー応答・実行モデル |
| [reviews/2026-09-12-renderer-cli-p6-review.md](reviews/2026-09-12-renderer-cli-p6-review.md) | P6 レビュー — renderer / CLI 実装（PR #8）の V-model RTM と判定（pass） |
| [reviews/2026-09-12-api-and-pipeline-p6-review.md](reviews/2026-09-12-api-and-pipeline-p6-review.md) | P6 レビュー — pipeline-and-cli（PR #10）+ api-render（PR #12）の V-model RTM と判定（pass。Warning 1 / Suggestion 6） |
| [reviews/2026-09-12-charter-schema-alignment-review.md](reviews/2026-09-12-charter-schema-alignment-review.md) | charter・IR型語彙・renderer設計と実装の整合レビュー。**PR #8 時点のツリーに対するもの**で、ADR-0001 以前の記述（型語彙11型など）を含む |
| [adr/](adr/) | Architecture decisions |
| [glossary/](glossary/) | Terms |
| [evaluations/](evaluations/) | Evaluation records |
| [reviews/](reviews/) | Review records |
| [../schemas/](../schemas/) | Shared schemas（IR / API） |
| [../design/](../design/) | Design artifacts（図・モック） |

P4 実装計画（renderer.md「次」の分割案どおり）:

- [.agents/plans/algorithms/ir-validate-and-derive.md](../.agents/plans/algorithms/ir-validate-and-derive.md) — FR1–FR4（H5。TeX 非依存）
- [.agents/plans/programs/render-and-cli.md](../.agents/plans/programs/render-and-cli.md) — FR5–FR8・NFR1–2（H4）
- [.agents/plans/programs/pipeline-and-cli.md](../.agents/plans/programs/pipeline-and-cli.md) — 着手順2。`entex.pipeline` 共通入口と CLI の乗せ替え（H4）
- [.agents/plans/programs/api-render.md](../.agents/plans/programs/api-render.md) — 着手順2。`POST /v1/render` ほか FastAPI（H4）

未作成（必要になった段階で作る）:

- `LINEAR_PHASE_MAP.md` — キット側 `.agents/docs/LINEAR_PHASE_MAP.md` にある（optional。`project-state.yaml` の `linear_sync.map_doc` は `docs/LINEAR_PHASE_MAP.md` を指しているが、consumer 側には複製していない）

Plans: [.agents/plans/](../.agents/plans/README.md)
Kit: [.agents/README.md](../.agents/README.md)
Agent guide: [../AGENTS.md](../AGENTS.md)

キットから持ち込んだ雛形を本番の成果物にするときは、`sample-*` / `example-*` のスラッグを先に改名する。
