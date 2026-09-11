---
id: npcdotcom-philosophy
kind: knowledge
topic: design-philosophy
owner: NPCdotcom
status: active
promoted_from: learning/npcdotcom
promoted_at: 2026-06-18
updated: 2026-06-18
core_confirmed_at: 2026-06-18
core_evidence: E-15
promotion_gate:
  critique_path: learning/npcdotcom/.agents/memory/evaluations/2026-06-18-promotion-critique.yaml
  passed: true
  retroactive: true
  verified_at: 2026-06-18
tags: [npcdotcom, philosophy, registry, oop, simulation, design]
sources:
  - learning/npcdotcom/notes/evidence-log.md
  - learning/npcdotcom/notes/design-principles.md
  - learning/npcdotcom/sources/landscape-dev-reference.md
---

# NPCdotcom — 設計思想（global 正本）

> **NPC / NPCdotcom** = オーナーのニックネーム（ゲーム NPC ではない）。  
> Historia / Project6A 等は **打ち切り済み · 核心に最も近いプロジェクト一例**（正本ではない）。

## 核心（E-15 · 確定 · 2026-06-18）

> **理想の設計** = 何もないこと × 何でもできること  
> **好きなこと** = そこからすべてを作ること

| 軸 | 意味 |
|----|------|
| **何もない** | コアに **既定世界を持たない**（P3 · メタレジストリ · defer） |
| **何でもできる** | **登録**で拡張面を無限に足せる（P1–P2 · OCP · P7） |
| **すべてを作る** | 動機の本流は **結果** — **現実世界への無限近似**。その **過程** として捉えてよい |

### 層の距離（核心との関係）

| 層 | 位置づけ |
|----|----------|
| レジストリ / メタレジストリ / OCP | **核心に最も近い設計層** |
| C++ / CUDA / Vulkan（低レイヤー自前） | 核心ではないが **核心に最も近い実装層**（**許容**） |
| Historia / Project6A 等 | **打ち切り済み** · 核心に最も近い **プロジェクト一例** |
| 商用エンジン丸投げ · 発行者依存ライブラリ | 避ける — コアに **何か** を持ち込む |

**North Star** は核心の運用表現: 空の統一枠（レジストリ）から、登録の中身で **現実に近い** 専門性を足す。

## 美しさ（North Star）

**美しいプログラム** = オブジェクト・属性・イベント・アルゴリズムを可能な限り **レジストリで規格統一**し、**使い回し**で汎用性を保ちながら、登録の中身で **専門性・独自性** を持たせること。

- **メタレジストリ**: 何が存在するかをシステム自身が認知
- **段階的構築**: 空から登録を足すだけで世界が増える（終始一貫）

## コア原則（P1–P10）

| ID | 原則 |
|----|------|
| P1 | レジストリ中心の柔軟設計 — 拡張は登録で |
| P2 | メタレジストリ — 存在の認知 |
| P3 | 段階的構築（空 → 登録） |
| P4 | 開放閉鎖原則（OCP）— 拡張に開き変更に閉じる |
| P5 | GoF · 合成優先の OOP |
| P6 | **アルゴリズム最小単位**のカプセル化 — 数式に限らず kernel を登録・再利用 |
| P7 | 規格統一 · 汎用設計 |
| P8 | 物理エンジン ∥ 科学（化学）エンジン — 状態媒介・データ駆動 |
| P9 | **低レイヤー並列・描画** — CUDA / Vulkan。**核心に最も近い実装層**（許容）。商用エンジン委譲は非志向 |
| P10 | 数学的一般論 · Policy/Strategy による差し替え |

## 思考の型（要約 · E-13）

**イメージ駆動** — ウォーターフォールではなく **「考えたこと」⇄「知っていること（調べたこと）」の反復**。

```text
全体イメージ言語化 → 分解 → 調査
  ⇄ 既知+調査で評価・推論（反復）
→ メタレジストリで存在認識 → アーキ具体像を詰める
→ 最小単位から積み上げ実装 → 振り返り
```

- **判断軸**: 拡張性 > 正しさ > 理解可能性
- **表象**: 頭内シミュ（俯瞰/当事者）· 図的 · 存在は並列平等
- **失敗パターン**: イメージ未定・未伝達のまま進めてずれる

詳細: `learning/npcdotcom/notes/thinking-process.md`

## ドメイン・技術関心（一例）

- 主に **ゲーム**、特に **シミュレーション**
- **CUDA**: 高スレッド化が続く前提で大規模 sim に期待（GPU バッチ ECS 等が業界トレンド）
- **Vulkan**: 低レイヤー graphics の明示制御
- 調査メモ: `learning/npcdotcom/sources/landscape-dev-reference.md`（learning 層 · 更新可）

## 反パターン

- プロジェクト手順・スタックを思想と混同
- アルゴリズムのコピペ（→ kernel 登録へ昇格すべき）
- コアの `switch` 肥大化（OCP 違反）
- 物理と化学の直接結合（P8 違反）

## エージェントへの指示

- 設計・実装・計画前に **本ファイルを recall**（核心 E-15 を最優先）
- 提案は **空の段階に何を登録するか** から。既定コンテンツ・高レベル依存を持ち込まない
- 動機は **現実近似という結果** を忘れない。最小単位積み上げはその手段
- 用語・技術調査は **広く浅く網羅 → 搾って深掘り**（`landscape-research` / `terminology-research`）
- 学習層の詳細・証跡: `~/.agents/learning/npcdotcom/`

## Related index ids

- npcdotcom-preferences
