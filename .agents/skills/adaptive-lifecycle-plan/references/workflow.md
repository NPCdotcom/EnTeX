# Adaptive lifecycle plan — workflow

## 1. Gather inputs

| 入力 | 取得元 |
|------|--------|
| ユーザー意図 · 緊急度 | 直近メッセージ · turn-brief |
| **workspace 判定（G6）** | skill `secretary-route` · [`workspace-detection.md`](../../secretary-route/references/workspace-detection.md) |
| brownfield | workspace-detection · 既存 repo / `docs/` 有無 |
| 複雑度 | 影響範囲 · 不明点の数 · 新規 vs 変更 |
| 現状態 | `docs/project-state.yaml` · `nav.yaml` Phase 0 |

## 2. Select profile

| Profile | いつ | 推奨 P | スキップ例 | Cursor |
|---------|------|--------|------------|--------|
| **hotfix** | 単一バグ · 局所修正 | P4→P5→P6（patch） | P0–P3 | Agent |
| **spike** | 不確実性除去 · S0 | P0–P3 部分 · S0 | P5–P6 | Ask→Plan |
| **standard** | 通常 feature（H4/H5） | P1→P2→P3→P4→P5→P6 | P0（既存 charter あり） | Plan→Agent |
| **full** | greenfield · 新製品 | P0→P1→…→P6 | なし | Ask→Plan→Agent |
| **doc_only** | 要求/設計のみ | P0–P2（+P3 任意） | P4–P6 | Plan |

**IaC / クラウド**: P3 で `docs/design/_template/infrastructure/` → `systems/<slug>/`（G9 · o-06）。CI 例は `docs/_example/.github/workflows/iac-checkov.example.yml`。

**brownfield 追加**: Reverse Engineering 相当 → P1 前に **`brownfield-reference`**（`docs/design/reverse-engineering/`）。業界調査のみ `landscape-research`。

## 3. Map AI-DLC stages → kit（監査用ラベル）

| AI-DLC stage | Kit 相当 |
|--------------|----------|
| Workspace Detection | profile + brownfield 判定 |
| Reverse Engineering | brownfield RE（conditional） |
| Requirements Analysis | P1–P2 · terminology-research |
| Workflow Planning | **本 skill** |
| Application Design | P3 |
| Units Generation | H4/H5 分割 · `unit_scope` |
| Functional/NFR/Code | P4–P5 per unit |
| Build and Test | P6 |

`skipped_stages` に AI-DLC ラベルを記録（任意）。**条件付きステージ**の Run/Skip: [`conditional-stages.md`](conditional-stages.md)（G8 · o-09）。

## 4. Recommend output

1. `lifecycle-plan-output-template.md` を埋める
2. **Plan モード**でユーザーに提示
3. 曖昧点が残る → `verification-questions.md` を起票（question-file-template）
4. ユーザー **Go** 後 → `docs/project-state.yaml` の `lifecycle_plan` を更新

```yaml
lifecycle_plan:
  profile: standard
  brownfield: true
  last_planned_at: "2026-06-22T..."
  executed_phases: [P1, P2, P3, P4, P5, P6]
  skipped_phases: [P0]
  skipped_stages: ["User Stories"]
  recommended_cursor_mode: "Plan→Agent"
  requirements_depth: standard
  unit_scope: docs/design/programs/example.md
  notes: "charter 既存のため P0 skip"
```

## 5. Route next

`secretary-route` 表に従い **最初の executed phase** へ。P1–P2 では terminology-research → 質問ファイル Gate。

## 6. Requirements depth（H-P4）

| depth | P1–P2 の厚み | 推奨 profile |
|-------|----------------|--------------|
| **minimal** | 受入条件 · 核心用語のみ | `hotfix` · `spike` |
| **standard** | 要求+要件 · alignment 3–8 語（**デフォルト**） | `standard` · `doc_only` |
| **comprehensive** | 上記 + `docs/requirements/_template/traceability-table.md` | `full` |

1. profile から depth を推薦し `lifecycle_plan.requirements_depth` に記録
2. `terminology-research` は depth に応じた用語数・成果物（`TERMINOLOGY_RESEARCH_POLICY.md`）
3. comprehensive 時は P2 完了までにトレーサビリティ表を埋める
