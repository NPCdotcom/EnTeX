---
chem_doc_id: chem.topic.catalysis_kinetics
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [catalysis, kinetics, langmuir-hinshelwood]
chem_doc_regex_file: ^chem\-doc\-catalysis\-reaction\-kinetics\.md$
---

<!-- CHEM_DOC_ID: chem.topic.catalysis_kinetics -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 触媒化学と反応速度論

---

## 1. 触媒の定義

**触媒** — 反応速度を変えるが自身は反応後も化学的に変化しない物質（オストワルト）。

- 正反応の活性化エネルギーを **同等に** 低下
- **平衡定数 K は変わらない**（熱力学的平衡位置は不変）
- 反応経路（機構）を変える

| 分類 | 例 |
|------|-----|
| 均一触媒 | 酸 · 酵素 · 有機金属錯体 |
| 不均一触媒 | 金属表面 · 酸化物 |
| 生体触媒 | 酵素 |

---

## 2. 触媒性能指標

| 指標 | 定義 |
|------|------|
| TOF | (生成物 mol) / (活性位点 mol · 時間) |
| 転化率 | 反応した基質の割合 |
| 選択性 | 目的生成物 / 全生成物 |
| 安定性 | 活性劣化の遅さ |

---

## 3. 速度論の深化

### 連続反応 A → B → C
dA/dt = −k₁A, dB/dt = k₁A − k₂B

B 濃度最大時刻: t_max = ln(k₁/k₂)/(k₁−k₂)（k₁ ≠ k₂）

### 定常状態近似（SSA）
速い平衡 + 遅い律速段階 → 中間体濃度が定常 → 全体速度は律速段階で決まる

### Arrhenius
k(T) = A exp(−E_a/RT)

---

## 4. 不均一触媒: Langmuir–Hinshelwood

表面吸着した反応物が反応:

r = k K P / (1 + K P)

| 圧力域 | 次数 |
|--------|------|
| 低圧 | r ∝ KP（1 次） |
| 高圧 | r → k（0 次、表面飽和） |

---

## 5. 非等温反応

断熱系では反応熱で温度が上昇:

dT/dt = (−ΔH/C_p)(−dA/dt)

E_a が大きい反応では **温度ランナウェイ** の危険（熱除去設計が重要）。

---

## 6. 工業触媒の例

| プロセス | 触媒 |
|----------|------|
| Haber–Bosch | Fe/K/Al₂O₃（NH₃ 合成） |
| 接触法 | V₂O₅（SO₂ 酸化） |
| 自動車排ガス | Pt/Rh/Pd（三元触媒） |
| オレフィン重合 | Ziegler–Natta / メタロセン |
