---
id: lesson-chemistry-p11-synthesis
kind: knowledge
topic: lesson
owner: learning/chemistry
status: active
promoted: 2026-06-20
tags: [chemistry, roadmap, numerical-toy, p11]
linked: [lesson-chemistry-learning-complete, lesson-chemistry-p11-round4]
---

# 教訓 — 化学 P11 深化ロードマップ総括

詳細正本: `learning/chemistry/notes/p11-cycle27-synthesis-lessons.md`  
長期記憶: `chemistry-learning-complete.md`

## 要点（2026-06-20 · P11 第 1 期完走）

| 領域 | フック |
|------|--------|
| ロードマップ | Wikipedia 分野一覧 → 26 サイクル × 2+ Python toy · P0–P10 完走後の反復深化 |
| 3 ラウンド | 01–10 初期走査 · 11–20 応用（電池·薬·固体·光触媒）· 21–26 接続（CO2RR·フロー·MD） |
| 横断軸 | 対象スケール（核→環境）と親フェーズ（P4–P10）でサイクルを位置づける |
| 定式索引 | 触媒 TOF → Nernst → BET → AQY → MSD 等、各分野 1 代表式を toy で固定 |

## 数値 toy の再発防止

1. **次元解析を先に** — Wh/kg · m²/g · % 等は手計算でオーダー確認
2. **参照値 1 点** — 文献代表値と 1 点比較してから一般化
3. **アンサンブル** — MSD · 確率過程は単一軌道不可（N≳100）
4. **命名・索引** — `p11-cycleNN-<slug>.md` + `experiments/p11_cycleNN/` を正本 1 つに

## 修正履歴（代表）

| サイクル | 問題 |
|----------|------|
| 11 | 比容量単位 |
| 17 | 劣化 k スケール |
| 18 | 非等温発散 |
| 19 | BET 変換式 |
| 25 | Boltzmann 占有率 |
| 26 | MSD→D 統計 |

## 次に深掘りする候補（Cycle 37+ · 未計画）

1. 第 5 ラウンド — 分野一覧から未触分野（ユーザー選定）
2. RDKit / ASE / pymbar 等ライブラリ接続（`.venv` 整備後）
3. `manifest.status` 更新（`exploring` → 初期ロードマップ完走）

**第 4 ラウンド（C28–36）**: 完了 — [p11-cycle36-round4-synthesis-lessons.md](../learning/chemistry/notes/p11-cycle36-round4-synthesis-lessons.md)

## Related

- lesson-chemistry-p11-round4 (Cycle 36)
