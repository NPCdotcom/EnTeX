---
id: lesson-math-learning-p9-cross-review
kind: knowledge
topic: lesson
owner: learning/math
status: active
created: 2026-06-22
promoted: 2026-06-22
tags: [math, learning, roadmap, p0-p9, p9, cross-review, hyperbolic, game-theory]
sources:
  - learning/math/notes/p9-cycle32-cross-review.md
  - learning/math/notes/p9-cycle30-hyperbolic-summary.md
  - learning/math/notes/p9-cycle31-game-tracks-synthesis.md
  - learning/math/notes/p9-cycle31-coordination-summary.md
trace: traces/2026-06-22-math-full-promotion.md
linked: [lesson-math-learning-complete, lesson-math-p9-synthesis]
---

# 数学 P9 横断レビュー — 詳細 archive

**正本（全体）**: `math-learning-complete.md`  
**本ファイル**: Cycle 32 横断レビューの詳細記録（archive）

---

## Principle

Wikipedia / MSC2020 ベースの数学ロードマップ（P0–P8 完走済み）において、P9 深化は **毎サイクル 1 双曲系 + 1 ゲーム学習** の並行 track で Cycle 11–31 を実施し、Cycle 32 で横断レビューした。  
横断再利用は **global lessons** と本ファイルを参照し、chat 履歴に依存しない。

---

## Facts

| 項目 | 値 |
|------|-----|
| トピック ID | `math` |
| 基礎層 | P0–P8 完了 |
| P9 サイクル | **32**（深化 01–31 + 横断レビュー 32） |
| 並行 track | Cycle 11–31: 双曲系 Euler + ゲーム学習 |
| 総括サイクル | 30（双曲）· 31（ゲーム）· 32（横断） |
| P9 実験ディレクトリ | 32（`experiments/p9_cycle01/` … `p9_cycle32/`） |
| 索引 | `learning/math/notes/00-index.md` |
| ロードマップ | `notes/wiki-roadmap.md` · `notes/p9-deepening-roadmap.md` |
| 学習索引 | `learning/index.yaml` |
| manifest | `learning/math/manifest.yaml` |
| 横断レビュー再現 | `experiments/p9_cycle32/p9_cross_review.py` |

### 双曲 track 確定結果（Sod nx=200 t=0.2 · エントロピー波 nx=100 t=0.5）

| 方式 | 結果 |
|------|------|
| **1st HLLC** | Sod L1 rho ~0.012 · grid 収束 OK · 内部ベンチマークとして信頼可 |
| MUSCL-HLLC | 1st より悪化（~1.7x） |
| primitive / conserved PP WENO-Z | 1st 未達（3.7–5.5x 悪化） |
| Char WENO（周期波） | 爆発 |
| **scalar WENO-Z**（decoupled） | 厳密解で勝利（L1 ~0.005） |
| Clawpack | pip 導入失敗 · 外部 gold 未確立 |

**因果**: ボトルネックは WENO 重みではなく **系 Euler 結合パイプライン**。スカラー移流では WENO-Z 有効。

### ゲーム track 確定結果

| ゲーム構造 | 最良手法 | 備考 |
|------------|----------|------|
| 零和 2x2 / 3x3 | **OMD**（定数 eta） | eta decay は優位喪失 |
| 協調 / Stag Hunt | **FP**（BR 型） | Hedge は NE 未到達が典型 |
| NE 選択（協調） | init / 構造化バイアス / ノイズが支配 | global games 完全モデルは未実装 |

**横断教訓**: 「汎用高次 / 汎用 no-regret」より **問題構造に合わせた手法選択** が結果を決める。

---

## Decisions

1. **Cycle 33 以降は未着手** — ユーザー次指示まで新サイクル・MSC 転換を開始しない
2. **status** — `manifest.yaml` を `p9_cross_review_complete` に更新（`exploring` から）
3. **応答規約** — Cycle 19 以降は完了内容と次の手のみ（詳細はノート参照）
4. **次の任意作業** — Clawpack conda 導入 · global games 完全モデル · MSC 別分野 P9 転換（ユーザー選定）

---

## Lessons learned（数値 toy · 再発防止）

1. **参照を先に** — 厳密解（Toro Sod）· fine grid · scalar gold で自前実装を検証
2. **系結合を分離** — スカラー WENO の成功は系パイプライン成功を意味しない
3. **算法は構造依存** — 零和 OMD 優位は協調に移植不可 · FP >> Hedge（協調）
4. **NE 選択** — 动力学より初期条件・ペイオフ構造（バイアス init / 構造化ノイズ）
5. **eta decay** — 本実験設定（零和 MP · 協調 Stag）では推奨されない
6. **命名固定** — `p9-cycleNN-<slug>.md` + `experiments/p9_cycleNN/`
7. **Windows print** — ASCII のみ（cp932 で em dash 等が UnicodeEncodeError）

---

## 未解決 · 保留

| 項目 | Track | 優先度 |
|------|-------|--------|
| Clawpack conda 導入 | 双曲 | 高 |
| 特性 WENO + conserved PP（検証済み実装） | 双曲 | 高 |
| global games 完全モデル | ゲーム | 中 |
| 最適 eta スケジュール理論 | ゲーム | 低 |
| MSC 別分野への P9 転換 | P9 全体 | ユーザー指示待ち |

---

## Related index ids

- lesson-math-learning-complete（正本）
- lesson-math-p9-synthesis

## Related paths

- `~/.agents/memory/global/knowledge/lessons/math-learning-complete.md`
- `learning/math/notes/p9-cycle32-cross-review.md`
