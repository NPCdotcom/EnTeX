# Roles & Governance（役割分担・PM のあり方）

Web 調査に基づく **業界標準の役割** とキット（**PM + Cursor role**）の対応正本。

関連: [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md) · [role-skill-catalog](../skills/role-skill-catalog/references/full-catalog.md) · [CURSOR_ROLES.md](./CURSOR_ROLES.md) · [PM_ROUTING.md](./PM_ROUTING.md)

## 調査ソース（抜粋）

| 領域 | 参照 |
|------|------|
| PM 一般 | [PMI — What is a Project Manager](https://www.pmi.org/about/what-is-a-project-manager) |
| IT PM | [O*NET IT Project Managers](https://www.onetonline.org/link/summary/15-1299.09) · [Prosci IT PM](https://www.prosci.com/blog/it-project-management) · [Atlassian PM](https://www.atlassian.com/work-management/project-management/project-manager) |
| ゲート | [PMI Gate Philosophy](https://www.pmi.org/learning/library/contemporary-gate-philosophy-implemented-outcome-7786) · [monday.com Gate Review](https://monday.com/blog/project-management/gate-review/) · [OCM Stage-Gate](https://www.ocmsolution.com/stage-gate-process/) |
| 日本 SI 工程 | [リンプレス 要求/要件](https://www.linpress.co.jp/blog/c38) · [CIN GROUP 7工程](https://its.cin-group.com/tips/development-process/) · [DCR 上流/下流](https://www.dcr.co.jp/column/system-development-process/) |
| PM / PL / PMO | [パーソル PM/PL](https://staff.persol-xtech.co.jp/corporate/security/article.html?id=286) · [ラクス PM/PL/PMO](https://www.rakus-partners.co.jp/column/pm%E3%83%BBpl%E3%83%BBpmo%E3%81%A8%E3%81%AF%EF%BC%9F%E5%BD%B9%E5%89%B2%E3%81%AE%E9%81%95%E3%81%84%E3%82%84%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AE%E7%AE%A1%E7%90%86%E4%BD%93/) |
| アジャイル役割 | [Atlassian Scrum Roles](https://www.atlassian.com/agile/scrum/roles) · [Scrum.org Product Owner](https://www.scrum.org/resources/what-product-owner) |
| Discovery/Delivery | [Atlassian Jira Discovery](https://www.atlassian.com/software/jira/product-discovery/guides/delivery/overview) · [Mind the Product 不確実性](https://www.mindtheproduct.com/product-discovery-or-product-delivery-how-do-you-decide/) |
| EM vs PM | [DX EM vs PM](https://getdx.com/blog/engineering-management-vs-project-management/) · [CodePulse EM vs PM](https://codepulsehq.com/guides/engineering-management-vs-project-management-guide) |
| Tech Lead | [Pat Kua Tech Leads in Scrum](https://www.patkua.com/blog/tech-leads-in-scrum/) |
| V字・トレーサビリティ | [Wikipedia V-model](https://en.wikipedia.org/wiki/V-model_(software_development)) · [Yuri Kan SDLC V-Model](https://yrkan.com/course/module-01-fundamentals/sdlc-v-model/) |
| AIDD / HITL | [Code on Grass HITL gates](https://codeongrass.com/blog/how-to-build-human-in-the-loop-approval-gates-ai-coding-agents/) · [Speakeasy Agent Hooks](https://www.speakeasy.com/resources/ai-agent-hooks) |

---

## 1. プロジェクトマネージャー（PM）のあり方 — 本キットでの定義

### 業界で共通する PM の責務

複数ソースで繰り返される PM の中核:

| 責務 | 内容 |
|------|------|
| **スコープ・計画** | 目標・範囲・WBS・マイルストーンの明確化（PMI, Atlassian, O*NET） |
| **QCD / トリプル制約** | 品質・コスト・納期のバランス（日本 SI: PM が QCD 責任） |
| **ステークホルダー** | 期待値調整・コミュニケーション計画・報告（Prosci, Atlassian） |
| **リスク** | 早期特定・緩和・エスカレーション（Coursera IT PM, PMI gates） |
| **ゲート判断** | 工程間で **Go / 保留 / 巻き戻し / 中止** を証拠に基づき決める（Stage-Gate, PMI） |
| **ブロッカー除去** | チームの障害を取り除くが、**日常の技術実装は担わない**（EM vs PM 系文献） |

### PM が **担わない** こと（役割分離）

| 担当外 | 理由 | 本キットでの委譲先 |
|--------|------|-------------------|
| 技術アーキテクチャの最終決定 | EM / Tech Lead 領域（CodePulse, Pat Kua） | `spec_designer`（戦略）+ ユーザー |
| コード実装本体 | Developer 領域 | `builder` |
| コードレビュー本文 | Reviewer 領域 | `reviewer` |
| ルーティング・ゲート判定の起草 | Router 領域 | `router` |
| ゲートの **独立レビュー** | PM 単独では利益相反（monday.com: PM は gate 実施者にしない） | **ユーザー（ステアリング）** |

### 本キットにおける PM（メインエージェント）

PM は **オーケストレーター** であり **実装者ではない**:

```
ユーザー発話
  → router（毎ターン: P/H/gate・role 割当）
  → PM が role-execute で role 行を実行
  → PM が統合・未決提示・ゲート確認依頼
  → ユーザー（ステアリング）が Go / Conditional / Recycle / Hold / Kill
```

| PM がやる | PM がやらない |
|-----------|---------------|
| router ゲートの遵守 | router brief の代行 |
| role 実行順の統制 | `implement-conduct` の独力実行 |
| 工程 P? / スコープ H? の明示 | 設計・計画正本の独力大規模編集 |
| ゲート前の **確認依頼** | ゲートの独断通過 |
| 運用証跡の付与 | Subagent 起動 |

---

## 2. 業界役割 ↔ Cursor role 対応

### 2.1 日本 SI（PM / PL / 上流 SE）

| 業界役割 | 主な視点 | Cursor role | キット P |
|----------|----------|-------------|----------|
| **PM** | 全体 QCD・ステークホルダー | **PM（メイン）** + router | 横断 |
| **PL** | 現場推進・タスク分解・技術課題 | `plan_slicer` + `builder` 調整 | P4–P5 |
| **上流 SE** | 要求・要件・基本設計 | `spec_designer` | P1–P3 |
| **PMO** | 標準・横断支援・可視化 | `kit_maintainer` + `lifecycle-reference` | 横断 |

出典: [パーソル PM/PL](https://staff.persol-xtech.co.jp/corporate/security/article.html?id=286), [ラクス PM/PL/PMO](https://www.rakus-partners.co.jp/column/pm%E3%83%BBpl%E3%83%BBpmo%E3%81%A8%E3%81%AF%EF%BC%9F%E5%BD%B9%E5%89%B2%E3%81%AE%E9%81%95%E3%81%84%E3%82%84%E3%83%97%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AE%E7%AE%A1%E7%90%86%E4%BD%93/)

### 2.2 アジャイル（Scrum + Tech Lead）

| 業界役割 | 責務 | Cursor role |
|----------|------|-------------|
| **Product Owner** | 価値最大化・バックログ・受入 | `spec_designer`（P1–P2）+ ユーザー |
| **Scrum Master** | プロセス・障害除去・コーチ | `router`（ブロッカー整理）※ SM 単独役は持たない |
| **Developers** | インクリメント交付 | `builder` |
| **Tech Lead** | 技術方針・品質・負債のビジネス翻訳 | `spec_designer`（P3）+ `builder`（P5） |

出典: [Atlassian Scrum](https://www.atlassian.com/agile/scrum/roles), [Pat Kua Tech Lead](https://www.patkua.com/blog/tech-leads-in-scrum/)

**注意**: Tech Lead と Scrum Master の兼任は文献上非推奨。本キットでも **router（プロセス）と builder（実装）を同一ターンで混線させない**。

### 2.3 EM vs PM（英語圏）

| | Engineering Manager | Project Manager | 本キット |
|--|---------------------|-----------------|----------|
| 焦点 | 人・システム・技術卓越 | 計画・納期・スコープ | PM=計画側、spec/builder=技術側 |
| メトリクス | サイクルタイム・品質文化 | マイルストーン・予算 | plan status + review |

出典: [getdx EM vs PM](https://getdx.com/blog/engineering-management-vs-project-management/)

---

## 3. 工程 P0–P6 — 業界照合

### 3.1 ウォーターフォール / 日本 7 工程

| 日本一般工程 | キット P | 主担当（業界） | Hermes |
|--------------|----------|----------------|--------|
| 要求定義 | P1 | PM・上流 SE | spec_designer |
| 要件定義 | P2 | PM・上流 SE | spec_designer |
| 基本設計（外部） | P3 | 上流 SE・PL | spec_designer |
| 詳細設計（内部） | P4（plan に内包） | SE・PL | plan_slicer |
| 実装 | P5 | エンジニア | builder |
| 単体〜受入テスト | P6 | QA・PL・ユーザー | reviewer |
| リリース・運用 | P6 Act / P5+ | PM・運用 | evaluator / hotfixer |

出典: [CIN GROUP](https://its.cin-group.com/tips/development-process/), [リンプレス](https://www.linpress.co.jp/blog/c38)

### 3.2 PMI 5 工程との対応

| PMI | キット P |
|-----|----------|
| Initiating | P0 |
| Planning | P1–P4 |
| Executing | P5 |
| Monitoring & Controlling | P6 + router 毎ターン |
| Closing | P6 Act（plan 完了・教訓） |

### 3.3 Discovery / Delivery（重なり）

Atlassian・Mind the Product 等: **Discovery と Delivery はフェーズ分離ではなく連続**。

| 活動 | キットでの置き場 |
|------|------------------|
| Discovery（不確実性の除去） | P0–P2、`S0` スパイク（P3 まで） |
| Delivery（構築・検証） | P4–P6 |
| 不確実性が高い | `plan-record` / `implement-conduct` **禁止** → S0 へ |

出典: [Atlassian Discovery→Delivery](https://www.atlassian.com/software/jira/product-discovery/guides/delivery/overview), [Mind the Product](https://www.mindtheproduct.com/product-discovery-or-product-delivery-how-do-you-decide/)

### 3.4 V字モデル — テストと工程の対応（P6）

| 左（開発） | 右（検証） | キット |
|------------|------------|--------|
| 要件 | 受入（UAT） | P2 受入条件 ↔ P6 criteria |
| 基本設計 | 総合（ST） | P3 design ↔ P6 review |
| 詳細設計 | 結合（IT） | P4 plan scope ↔ P6 review |
| 実装 | 単体（UT） | P5 TDD ↔ P6 review |

**トレーサビリティ**: plan の Acceptance criteria は要件・設計へリンク（RTM 相当）。

出典: [V-model Wikipedia](https://en.wikipedia.org/wiki/V-model_(software_development)), [Yuri Kan](https://yrkan.com/course/module-01-fundamentals/sdlc-v-model/)

---

## 4. ステージゲート（工程間の意思決定）

### 4.1 ゲートの原則（PMI / Stage-Gate）

- 投資・コミットが増える境界にゲートを置く（PMI gates）
- 設計未完了で実装開始しない（PMI: coding until design completion criteria）
- スコープ変更とリスクを毎ゲートで再評価

### 4.2 判定結果（monday.com 準拠）

| 判定 | 意味 | PM の動き |
|------|------|-----------|
| **Go** | 次工程へ | role 実行を進める |
| **Conditional Go** | 条件付き前進 | 条件を plan / issue に記録 |
| **Recycle** | 現工程のやり直し | 同 P で spec/plan を修正 |
| **Hold** | 一時停止 | `project-state` を hold |
| **Kill** | 中止 | plan `superseded`、理由を記録 |

**Gate Keeper**: **ユーザー**（ステアリング）。PM は証拠を揃え **提案** するのみ。

`docs/project-state.yaml` の `gate_status` を更新する:

| フィールド | 用途 |
|------------|------|
| `current` | `pending` / `passed` / `conditional` / `recycled` / `hold` / `killed` |
| `proposal` | router が提案する Go / Conditional Go / … |
| `last_decision` | 確定したゲート ID（例 `P4-plan-foo-go`） |
| `conditions` | Conditional Go の未消化条件 |
| `gate_keeper` | 常に `user` |

ユーザーが Go を明示したら `current: passed` と `last_gate_passed` を同期する。

### 4.3 本キットの必須ゲート（既存 + 調整）

| ゲート | タイミング | Gate Keeper |
|--------|------------|-------------|
| P4 `plan-record` | 実装計画確定前 | **ユーザー** |
| P5 `implement-conduct` | plan `agreed` 後 | router + **ユーザー**（agreed 時点） |
| P6 → Act 巻き戻し | 受入未達 | **ユーザー** + evaluator 提案 |

---

## 5. AIDD / AI エージェント運用への当てはめ

| 原則 | 実装 |
|------|------|
| Human-in-the-loop | P4/P5 前の **ユーザー確認**（HITL gate） |
| 高リスク操作の intercept | `secretary-gate`（毎ターン router） |
| ツール実行前の policy | Rules + `no-subagents` · [CURSOR_SUBAGENT_POLICY.md](./CURSOR_SUBAGENT_POLICY.md) |
| 監査証跡 | 応答末尾 **運用証跡**；`docs/project-state.yaml` の **`gate_status`** |

出典: [Speakeasy Agent Hooks](https://www.speakeasy.com/resources/ai-agent-hooks), [Code on Grass HITL](https://codeongrass.com/blog/how-to-build-human-in-the-loop-approval-gates-ai-coding-agents/)

---

## 6. 小規模プロジェクトでの兼任

日本 SI・Scrum 文献共通: **小規模では PM/PL 兼任可**。本キットでも:

- ユーザーが少人数なら PM が plan 確認まで兼ねる
- ただし **同一ターンで router 省略 + builder 実装** は禁止（利益相反）

---

## 関連ファイル

| ファイル | 用途 |
|----------|------|
| `rules/secretary-gate.mdc` | PM gate (alwaysApply) |
| `rules/secretary-gate.mdc` | 毎ターン HITL |
| `rules/phase-index.mdc` | 工程インデックス |
| `skills/role-skill-catalog` | role × skill 表 |
