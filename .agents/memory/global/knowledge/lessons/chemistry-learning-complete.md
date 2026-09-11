---
id: lesson-chemistry-learning-complete
kind: knowledge
topic: lesson
owner: learning/chemistry
status: active
created: 2026-06-20
promoted: 2026-06-20
tags: [chemistry, learning, roadmap, p0-p11, p11, complete]
sources:
  - learning/chemistry/notes/wiki-roadmap.md
  - learning/chemistry/notes/p11-cycle27-synthesis-lessons.md
  - learning/chemistry/notes/p11-cycle36-round4-synthesis-lessons.md
linked: [lesson-learning-complete-index]
---

# 化学学習ロードマップ — 長期記憶（正本）

**正本パス**: `~/.agents/learning/chemistry/`  
**昇格日**: 2026-06-20 · **状態**: P11 計画分完走 · **一旦停止**

---

## Principle

Wikipedia 分類ベースの化学ロードマップ（P0–P11）を **ノート + 最小 Python toy + 索引** で完走した。  
横断再利用は **global lessons** と本ファイルを参照し、chat 履歴に依存しない。

---

## Facts

| 項目 | 値 |
|------|-----|
| トピック ID | `chemistry` |
| 基礎層 | P0–P3 完了 |
| 分野層 | P4–P10 完了 |
| P11 サイクル | **36**（分野 34 + 総括 2） |
| 第 1–3 期 | Cycle 01–26 + Cycle 27 総括 |
| 第 4 期 | Cycle 28–35 + Cycle 36 総括 |
| 索引 | `learning/chemistry/notes/00-index.md` |
| ロードマップ | `notes/wiki-roadmap.md` · `notes/p11-deepening-roadmap.md` |
| 学習索引 | `learning/index.yaml` |
| manifest | `learning/chemistry/manifest.yaml` |

### 第 4 ラウンド（Cycle 28–35）系列

FEP/TI -> Umbrella/PMF -> BAR/MBAR -> Marcus ET -> ML ポテンシャル -> MetaD -> Forster/Dexter -> 能動学習

### 成果物規模（2026-06-20）

- P11 ノート: 36
- P11 実験ディレクトリ: 36（Cycle 01–36）
- global lessons: 3 件（本ファイル + synthesis + round4）

---

## Decisions

1. **Cycle 37 以降は未計画** — ユーザー指示まで新サイクルを開始しない
2. **status** — `manifest.yaml` を `roadmap_complete` に更新（`exploring` から）
3. **次の任意作業** — 第 5 ラウンド選定 · `.venv` + RDKit/ASE/pymbar · manifest を `maintained` 等へ

---

## Lessons learned（統合）

### 数値 toy（全期）

1. 次元解析を先に（Wh/kg · m²/g · %）
2. 参照値 1 点で sanity check
3. 確率量はアンサンブル（MSD 等 N≳100）
4. 命名固定: `p11-cycleNN-<slug>.md` + `experiments/p11_cycleNN/`

### 第 4 ラウンド追加分

1. ΔG 符号: ln(k_B/k_A) = F_B − F_A
2. PMF: 密度比正規化 · 窓 stitch
3. 三重項 ET: Forster 禁止 · Dexter 経路
4. 能動学習: 井戸のみ初期データでは障壁 query 必須

### 代表修正（Cycle 11–26）

比容量単位 · 食品劣化 k · 非等温発散 · BET 式 · Boltzmann 占有率 · MSD 統計

---

## Related index ids

- lesson-chemistry-p11-synthesis（Cycle 27 · 第 1–3 期）
- lesson-chemistry-p11-round4（Cycle 36 · 第 4 期）
- learning/index.yaml → `id: chemistry`

## Related paths

- `~/.agents/memory/global/knowledge/lessons/chemistry-p11-synthesis.md`
- `~/.agents/memory/global/knowledge/lessons/chemistry-p11-round4-synthesis.md`
- `~/.agents/memory/global/knowledge/documents/chem-doc-meta-INDEX.md`（エージェント用単体完結文書 20 件）
