# Monorepo brownfield — RE スコープ（o-10）

**When**: 単一 repo に **複数アプリ / パッケージ**（monorepo · multi-package）  
**原則**: RE は **リポジトリ全体を一度に埋めない** — **スコープ単位**で反復

---

## 1. スコープの切り方

| 粒度 | いつ | `unit_scope` 例 |
|------|------|-----------------|
| **リポジトリ全体** | 初回 onboarding · 移行計画のみ | `docs/design/reverse-engineering/`（索引のみ） |
| **パッケージ / アプリ** | 変更対象が明確 | `packages/shared/` · `apps/api/` |
| **単一 program** | standard feature | `docs/design/programs/<slug>.md` |

初回は **workspace-inventory をリポジトリ全体** → 以降は **対象パッケージのみ** architecture/api/debt を更新。

---

## 2. workspace-inventory 追記（monorepo）

`workspace-inventory.md` に **パッケージマップ** 節を追加:

```markdown
## パッケージマップ（monorepo）

| パス | 種別 | 責務 | ビルド | テスト |
|------|------|------|--------|--------|
| apps/web | app | | | |
| apps/api | app | | | |
| packages/shared | lib | | | |
```

ツール例: npm/pnpm workspaces · Turborepo · Bazel（記載のみ · キットはツール非依存）

---

## 3. profile と RE の厚み

| profile | monorepo での RE |
|---------|------------------|
| **hotfix** | 対象パッケージの inventory + api-surface のみ |
| **standard** | 対象パッケージ 6 テンプレ · 依存は `dependencies` で横断 |
| **full** | 全パッケージ inventory + 変更予定パッケージは厚く |

---

## 4. 横断依存

- `dependencies-and-integrations.md` に **パッケージ間依存** を表で記録
- 内部 lib 変更は **依存元アプリ**を IT 層で確認（P6）

---

## 5. Cursor / workspace

- multi-root は `workspace-detection` + ユーザー指定 root
- RE 正本は **git ルートの `docs/design/reverse-engineering/`**（パッケージ別サブディレクトリ可）

例: `docs/design/reverse-engineering/apps-api/architecture-overview.md`

---

## 6. 検証（o-10）

学習層デスク演習: `learning/product-dev/experiments/o-10-monorepo-brownfield/`  
実 repo 大規模検証は **利用先**で実施。

---

## 参照

- 学習: `t-06-monorepo-workspace.md`
- 評価: `evaluations/o-10-monorepo-brownfield-desk.md`
