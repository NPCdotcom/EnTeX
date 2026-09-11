# Conditional stages — AI-DLC ↔ キット（G8）

**正本**: skill `adaptive-lifecycle-plan` · `docs/PROJECT_LIFECYCLE.md`  
**監査**: `lifecycle_plan.skipped_stages` に **スキップした** AI-DLC ステージ名を記録（実行した場合は含めない）

---

## 原則

1. **Workflow Planning（本 skill）は常に実行**
2. **スキップは明示** — adaptive 出力で rationale を 1 行以上
3. **スキップ≠省略の隠蔽** — 後工程で必要になったら Recycle してステージを追加
4. **profile 優先** — 下表はデフォルト · ユーザー Go で上書き可

---

## 判定表

| AI-DLC ステージ | キット相当 | 実行（デフォルト） | スキップ可（例） | `skipped_stages` ラベル |
|-----------------|------------|-------------------|------------------|-------------------------|
| Workspace Detection | workspace-detection · adaptive | **常時** | — | — |
| Reverse Engineering | `brownfield-reference` | `brownfield: true` | greenfield · hotfix（inventory のみ） | `Reverse Engineering` |
| Requirements Analysis | P1–P2 · terminology | **ほぼ常時**（depth 可変） | 極小 hotfix（plan に FR 記載済） | `Requirements Analysis` |
| User Stories | P1 要求（ペルソナ・シナリオ） | standard · full · 顧客向け feature | hotfix · infra · doc_only · 内部 CLI | `User Stories` |
| Workflow Planning | **本 skill** | **常時** | — | — |
| Application Design | P3 `docs/design/**` | 新コンポーネント · 新 program | 既存 program 内 patch · hotfix | `Application Design` |
| Units Generation | H4/H5 分解 · `unit_scope` | 複数 unit · 並行候補 | 単一 H5 algorithm · hotfix | `Units Generation` |
| Infrastructure Design | P3 `systems/` テンプレ | IaC / クラウド | 非 IaC プロジェクト | `Infrastructure Design` |
| Functional/NFR Design | P3 program 細部 | per-unit 厚い P3 | spike · hotfix | `Functional Design` |
| Construction | P4–P6 | **常時**（profile で P 省略可） | — | — |
| Operations | `docs/operations/` テンプレ | 出荷後 · 本番あり | ライブラリ · ローカル CLI | `Operations` |

---

## Profile 既定

| Profile | よくスキップするステージ |
|---------|--------------------------|
| **hotfix** | User Stories · Application Design · Units Generation · RE（inventory のみ可） |
| **spike** | Units Generation · Operations · Construction（P5–P6） |
| **standard** | Infrastructure（非クラウド）· Operations |
| **full** | なし（RE は brownfield 時のみ追加） |
| **doc_only** | Units Generation · Construction · Operations |

---

## 出力チェックリスト（adaptive 完了時）

- [ ] 各 COND ステージについて **Run / Skip** と根拠 1 行
- [ ] `skipped_stages` を `project-state.yaml` に記録
- [ ] Skip したが P3/P4 で不足が出た → **Recycle** でステージ復活を提案

---

## 参照

- 学習: `learning/product-dev/notes/terminology/t-03-conditional-stages.md`
- 外部: [awslabs core-workflow](https://github.com/awslabs/aidlc-workflows/blob/main/aidlc-rules/aws-aidlc-rules/core-workflow.md)（丸コピー禁止 · 判定のみ翻訳）
