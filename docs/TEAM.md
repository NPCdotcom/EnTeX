# Team

| Nickname | GitHub | Notes |
|----------|--------|-------|
| NPC | [`NPCdotcom`](https://github.com/NPCdotcom) | リポジトリオーナー |
| Aster | [`Astel-isk`](https://github.com/Astel-isk) | 共同開発メンバー |

協業の正本は GitHub `main`。ドキュメント・スキーマ・デザイン・`.agents/` はコミットして共有する。

## 担当領域

2026/9/12 決定（[#15](https://github.com/NPCdotcom/EnTeX/issues/15)。分担案の初出は [#14](https://github.com/NPCdotcom/EnTeX/issues/14) §4）。

| 領域 | 主なパス | 担当 |
|------|----------|------|
| 本体（IR の検証・導出、renderer、pipeline、CLI、API） | `src/entex/` | NPC |
| 文書種パッケージ | `packages/` | Aster |
| 文書種の要求・要件 | `docs/requirements/` | Aster |
| 設計・ADR | `docs/design/` ・ `docs/adr/` | 起票した側。もう一方のレビューを経てマージする |
| 共有ハーネス | `AGENTS.md` ・ `.agents/` ・ `.github/` ・ `.githooks/` ・ `Makefile` | 双方 |

分ける理由は charter §6 にある。文書種を1つ増やすのに本体のコードを1行も変えずに済むか、という合否判定は、**判定する側と本体を書いた側が別でないと機能しない**。本体を書いた側は、詰まったときに `src/entex/` を1行直して解決してしまうためである。

境界をまたぐ変更は、実装の前に issue で合意する。次の2つが該当する。

- 型の語彙（[ir-type-vocabulary.md](design/elements/ir-type-vocabulary.md)）に型・フィールド属性を足す
- charter を改定する

相手の領域を直す必要が出たときは、自分で直さずに issue を立てる。
