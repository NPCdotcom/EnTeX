# Reverse engineering templates（brownfield）

**用途**: 既存コードベース初回把握。コピー先: `docs/design/reverse-engineering/`

| ファイル | 内容 |
|----------|------|
| `workspace-inventory.md` | リポジトリ構造 · ビルド · 実行方法 |
| `architecture-overview.md` | コンポーネント · データフロー · 境界 |
| `dependencies-and-integrations.md` | 依存 · 外部サービス |
| `api-surface.md` | 公開 API · エンドポイント |
| `data-model.md` | 永続化 · スキーマ |
| `tech-debt-risks.md` | 負債 · リスク · テストギャップ |

**手順**: skill `brownfield-reference` · `adaptive-lifecycle-plan`（brownfield: true）

**Monorepo**: 複数パッケージ repo は `monorepo-scoping.md` — パッケージ単位で RE · 全体は inventory のみ。

**非採用**: AI-DLC 8–9 ファイルセットの丸コピー — 本 6 件に圧縮（a-06 · o-05）。
