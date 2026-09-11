---
cpp_doc_id: cpp.topic.cp_dp
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [dp, knapsack, lis]
cpp_doc_regex_file: ^cpp-doc-cp-dynamic\-programming\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cp_dp -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# 競技プログラミング — 動的計画法

**出典**: CPH Ch.7 · AtCoder DP Contest (EDPC)

---

## 1. DP の定義

**全探索の正しさ** と **貪欲の効率** を両立。同じ部分問題を繰り返し解かない。

### 適用条件

1. 問題を **重なる部分問題** に分割できる
2. 各部分問題は **独立に** 解ける

### 用途

| 用途 | 例 |
|------|-----|
| 最適解 | 最小コイン枚数 · 最大価値 |
| 個数 | 経路数 · 作り方の数（mod） |

### 設計手順

```text
1. dp[?] の意味を言葉で定義
2. ベースケース
3. 遷移式
4. 計算順序（反復 or メモ化）
5. 状態数 × 遷移コスト = 計算量
```

---

## 2. メモ化 vs 反復

| | Top-down | Bottom-up |
|---|----------|-----------|
| 書き方 | 再帰 + メモ | for で小→大 |
| 計算する状態 | 必要なものだけ | テーブル全体 |
| 競プロ | 思考しやすい | **定数小 · 実装短** が多い |

---

## 3. 代表問題

### 3.1 コイン問題（最小枚数）

```cpp
const int INF = 1e9;
vector<int> dp(n + 1, INF);
dp[0] = 0;
for (int x = 1; x <= n; ++x)
    for (int c : coins)
        if (x >= c) dp[x] = min(dp[x], dp[x - c] + 1);
```

$O(nk)$。個数版は加算 + mod $10^9+7$。

### 3.2 最長増加部分列（LIS）

```cpp
vector<int> len(n, 1);
for (int k = 0; k < n; ++k)
    for (int i = 0; i < k; ++i)
        if (a[i] < a[k]) len[k] = max(len[k], len[i] + 1);
```

$O(n^2)$。$O(n \log n)$ は patience sorting + 二分。

### 3.3 グリッド経路

右・下のみ: `dp[y][x] = max(dp[y][x-1], dp[y-1][x]) + value[y][x]`。

経路数: 加算 + mod。

### 3.4 ナップサック（0/1）

```cpp
vector<bool> possible(W + 1);
possible[0] = true;
for (int w : weights)
    for (int x = W; x >= 0; --x)  // 降順が重要
        if (possible[x]) possible[x + w] = true;
```

価値最大化版は同型。完全ナップサックは昇順更新。

### 3.5 編集距離

```cpp
vector<vector<int>> dp(n + 1, vector<int>(m + 1));
for (int i = 0; i <= n; ++i) dp[i][0] = i;
for (int j = 0; j <= m; ++j) dp[0][j] = j;
for (int a = 1; a <= n; ++a)
    for (int b = 1; b <= m; ++b) {
        int cost = (s[a-1] != t[b-1]);
        dp[a][b] = min({dp[a-1][b]+1, dp[a][b-1]+1, dp[a-1][b-1]+cost});
    }
```

$O(nm)$。

---

## 4. 発展パターン（EDPC N–Z 系）

| パターン | 状態例 | 典型計算量 |
|----------|--------|------------|
| **区間 DP** | `dp[l][r]` = 区間 $[l,r]$ の最適 | $O(n^3)$ |
| **木 DP** | `dp[v][c]` = 部分木 · 色 $c$ | $O(n)$ |
| **ビットマスク DP** | `dp[S]` = 集合 $S$ の状態 | $O(n 2^n)$ |
| **桁 DP** | `dp[pos][rem]` = 上位桁まで · 剰余 | $O(L \cdot D \cdot 10)$ |
| **行列累乗** | 隣接行列の $K$ 乗 | $O(n^3 \log K)$ |
| **DAG DP** | トポソ順に更新 | $O(n+m)$ |
| **ゲーム DP** | 勝者判定 · Grundy | 問題依存 |

### 区間 DP（例）

```text
dp[l][r] = min_{l<=k<r}(dp[l][k] + dp[k+1][r]) + cost(l,r)
```

### 木 DP（例: 独立集合）

```text
dp[v][0] = Π dp[c][1]           // v を黒
dp[v][1] = Π (dp[c][0]+dp[c][1]) // v を白
```

---

## 5. 復元（reconstruction）

`parent[]` や `choice[]` で遷移を記録し、終端から逆走して解を復元。

---

## 6. mod 演算

個数問題では途中から $10^9+7$ で:

```cpp
dp[i] = (dp[i] + dp[j]) % MOD;
```

減算後は `(x % MOD + MOD) % MOD`。

---

## 7. 技法早見表

| 技法 | いつ | 計算量 |
|------|------|--------|
| メモ化/反復 DP | 重なる部分問題 | 状態×遷移 |
| ナップサック | 重量/価値制約 | $O(NW)$ |
| 2D 文字列 DP | LCS · 編集距離 | $O(nm)$ |
| グリッド DP | 経路 · 最大和 | $O(HW)$ |
| DAG DP | 依存順序あり | $O(n+m)$ |
| 区間/木/ビット/桁 DP | 問題構造に応じ | 各パターン参照 |
