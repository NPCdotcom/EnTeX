# Project documentation

| Path | Purpose |
|------|---------|
| [FIRST_PROJECT_START.md](FIRST_PROJECT_START.md) | 最初の 1 プロジェクトの起動手順（汎用） |
| [PROJECT_LIFECYCLE.md](PROJECT_LIFECYCLE.md) | Phases P0–P6, scope H0–H5, PDCA rules |
| [project-state.yaml](project-state.yaml) | Current phase / scope focus / gates |
| [TEAM.md](TEAM.md) | Members (NPC / Aster) |
| [design/](design/) | H0–H5 design。製品の正本は [design/product/charter.md](design/product/charter.md) |
| [design/elements/ir-type-vocabulary.md](design/elements/ir-type-vocabulary.md) | IR の型の語彙（月次報告書を題材に精査） |
| [adr/](adr/) | Architecture decisions |
| [glossary/](glossary/) | Terms |
| [evaluations/](evaluations/) | Evaluation records |
| [reviews/](reviews/) | Review records |
| [../schemas/](../schemas/) | Shared schemas（IR / API） |
| [../design/](../design/) | Design artifacts（図・モック） |

未作成（必要になった段階で作る）:

- `requirements/` — Per-topic 要求・要件（P1–P2）
- `LINEAR_PHASE_MAP.md` — Linear states ↔ P/H（optional。`project-state.yaml` の `linear_sync.map_doc` が参照している）

Plans: [.agents/plans/](../.agents/plans/README.md)
Kit: [.agents/README.md](../.agents/README.md)
Agent guide: [../AGENTS.md](../AGENTS.md)

キットから持ち込んだ雛形を本番の成果物にするときは、`sample-*` / `example-*` のスラッグを先に改名する。
