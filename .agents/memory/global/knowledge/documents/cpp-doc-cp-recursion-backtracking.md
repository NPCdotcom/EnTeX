---
cpp_doc_id: cpp.topic.cp_search
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [backtracking, meet-in-middle]
cpp_doc_regex_file: ^cpp-doc-cp-recursion\-backtracking\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cp_search -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# 競技プログラミング — 再帰 · バックトラック · Meet in the Middle

**出典**: CPH Ch.5 Complete search

---

## 1. Complete Search

全候補を生成して最良解を選ぶか個数を数える。実装は簡単で常に正しいが、候補爆発で TLE。

| 候補 | 個数 | 目安 $n$ |
|------|------|----------|
| 部分集合 | $2^n$ | $\le 20$ |
| 順列 | $n!$ | $\le 10$ |
| バックトラック | 枝刈り依存 | — |

---

## 2. 再帰の共通構造

| フェーズ | 役割 |
|----------|------|
| ベースケース | 葉で解を記録 |
| 選択 | 次に何を置くか試す |
| 進む | 状態変更して再帰 |
| 戻す | 状態を元に戻す（バックトラック） |

---

## 3. 部分集合（再帰）

```cpp
vector<int> subset;
void search(int k, const vector<int>& a) {
    if (k == (int)a.size()) { /* 処理 */ return; }
    search(k + 1, a);                    // k を含まない
    subset.push_back(a[k]);
    search(k + 1, a);                    // k を含む
    subset.pop_back();                   // 戻す
}
```

ビット列挙と同型:

```cpp
for (int b = 0; b < (1 << n); ++b) { /* ... */ }
```

---

## 4. 順列

```cpp
vector<int> perm, chosen(n, 0);
void gen() {
    if (perm.size() == n) { /* 処理 */ return; }
    for (int i = 0; i < n; ++i) {
        if (chosen[i]) continue;
        chosen[i] = 1; perm.push_back(i);
        gen();
        chosen[i] = 0; perm.pop_back();
    }
}
```

`next_permutation` でも可（$n \le 10$）。

---

## 5. バックトラック

空の解から一段ずつ伸ばし、ダメなら直前の選択を取り消す。

### N クイーン

- 1 行 1 女王
- `column[]`, `diag1[]`, `diag2[]` で $O(1)$ 衝突判定
- 枝刈り: 衝突したら `continue`

| | バックトラック | ビット全探索 |
|---|----------------|--------------|
| 枝刈り | 途中打切り可 | ほぼ全列挙 |
| 典型 | 制約付き配置 | 部分集合総当たり |

---

## 6. 枝刈り（Pruning）

部分解が完成解に伸びないと分かった時点で打ち切る。

典型: グリッド全マス訪問経路 — 対称性除去 · 終点に早く着きすぎたら打切 · 残りマス数と残り歩数の比較。

効果は問題依存 — 最悪計算量は変わらないが実効大幅削減。

---

## 7. Meet in the Middle

$2^n$ が厳しいとき（$n \approx 20$–$40$）、集合を半分に分けて $2^{n/2}$ ずつ列挙し、結果をマージ。

```text
左半分の全部分和 → ソート
右半分の全部分和 → ターゲット - 右 を左で二分探索
```

計算量 $O(2^{n/2} \cdot \log 2^{n/2}) = O(2^{n/2} \cdot n)$。

典型: 部分和が $T$ になる組 · 4 分割（$n \approx 40$）等。

---

## 8. DFS とグラフ探索

再帰 DFS はグラフ探索（P7-6）と同型:

```cpp
void dfs(int v, vector<int>& visited, const vector<vector<int>>& adj) {
    visited[v] = 1;
    for (int u : adj[v])
        if (!visited[u]) dfs(u, visited, adj);
}
```

スタック版 BFS/DFS も可 — 深さが大きいときはスタックオーバーフローに注意。

---

## 9. 技法早見表

| 技法 | いつ | 計算量 |
|------|------|--------|
| バックトラック + 枝刈り | 制約付き探索 | 実効削減 |
| Meet in the middle | $n \approx 20$–$40$ | $O(2^{n/2})$ |
| 順列全探索 | $n \le 10$ | $O(n!)$ |
| ビット全探索 | $n \le 20$ | $O(2^n)$ |
