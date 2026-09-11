---
cpp_doc_id: cpp.topic.cp_complexity
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [complexity, sort, binary-search, greedy]
cpp_doc_regex_file: ^cpp-doc-cp-complexity\-search\-greedy\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cp_complexity -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# 競技プログラミング — 計算量 · 探索 · 貪欲

**出典**: Competitive Programmer's Handbook (CPH) Ch.2–3, 5–6

---

## 1. 計算量の見積り

### 1.1 基本ルール

| パターン | 計算量 |
|----------|--------|
| $k$ 重ネストループ（各 $O(n)$） | $O(n^k)$ |
| 連続フェーズ | 最大フェーズのオーダー |
| 再帰 1 分岐 $f(n-1)$ | $O(n)$ |
| 再帰 2 分岐 $f(n-1)$ | $O(2^n)$ |

オーダー記法は定数倍を無視する。

### 1.2 よく使うクラス

| 記法 | 典型 |
|------|------|
| $O(1)$ | 公式で直接答え |
| $O(\log n)$ | 毎ステップ半分 |
| $O(n)$ | 配列走査 |
| $O(n \log n)$ | ソート · ヒープ操作 $n$ 回 |
| $O(n^2)$ | 二重ループ |
| $O(2^n)$ | 部分集合 |
| $O(n!)$ | 順列 |

### 1.3 制限時間 1 秒の目安

| $n$ 上限 | 必要な計算量 |
|----------|--------------|
| $\le 20$ | $O(2^n)$ |
| $\le 500$ | $O(n^3)$ |
| $\le 5000$ | $O(n^2)$ |
| $\le 10^6$ | $O(n \log n)$ または $O(n)$ |
| 大きい | $O(\log n)$ または $O(1)$ |

### 1.4 Kadane（最大部分配列和）

```cpp
long long best = LLONG_MIN, sum = 0;
for (int x : a) {
    sum = max<long long>(x, sum + x);
    best = max(best, sum);
}
```

$O(n)$ — 三重ループ $O(n^3)$ からの典型改善例。

---

## 2. ソート

### 2.1 比較ソート

| 種類 | 計算量 | 備考 |
|------|--------|------|
| バブルソート | $\ge O(n^2)$ | 反転理解用 |
| マージ/クイック | $O(n \log n)$ | `std::sort` のイメージ |
| counting sort | $O(n+c)$ | 値域が小さい整数 |

**下界**: 比較のみでは $\Omega(n \log n)$（決定木の葉 $n!$ 個）。

### 2.2 C++ でのソート

```cpp
sort(v.begin(), v.end());                    // 昇順
sort(v.begin(), v.end(), greater<int>());    // 降順
sort(a, a + n);                              // 生配列
```

`pair` / `tuple` は辞書順。構造体は `operator<` またはラムダ。

---

## 3. 二分探索

### 3.1 ソート済み配列

```cpp
auto it = lower_bound(v.begin(), v.end(), x);
if (it != v.end() && *it == x) { /* 見つかった */ }
```

$O(\log n)$。

### 3.2 単調な `ok(x)` — 答えの二分

```text
ok(x): false ... false | true ... true
```

```cpp
long long lo = 0, hi = MAX;
while (lo < hi) {
    long long mid = (lo + hi + 1) / 2;
    if (ok(mid)) lo = mid;
    else hi = mid - 1;
}
```

$O(\log V \cdot T_{ok})$。

### 3.3 単峰関数の最大

$f$ が先増後減のとき、$f(x) < f(x+1)$ が成り立つ最大 $x$ を二分。

---

## 4. 全探索（Complete Search）

| 列挙 | 個数 | 典型 $n$ |
|------|------|----------|
| 部分集合 | $2^n$ | $\le 20$ |
| 順列 | $n!$ | $\le 10$ |
| バックトラック | 枝刈り依存 | — |

```cpp
// ビット全探索
for (int b = 0; b < (1 << n); ++b) {
    for (int i = 0; i < n; ++i)
        if (b & (1 << i)) { /* i を含む */ }
}
```

---

## 5. 貪欲（Greedy）

毎ステップで局所最適を選び取り消さない。**証明が必要** — 反例 1 つで否定可。

### 5.1 区間スケジューリング（最多イベント）

**終了が早い順**にソート → 次に選べる（開始 $\ge$ 前の終了）イベントのうち終了最早を繰り返す。$O(n \log n)$。

### 5.2 コイン問題の反例

硬貨 $\{1,3,4\}$、合計 $6$: 貪欲 $4+1+1=3$ 枚 · 最適 $3+3=2$ 枚。

### 5.3 いつ疑うか

1. 小さい $n$ で反例を手計算
2. ダメなら DP または全探索へ

---

## 6. 技法早見表

| 技法 | いつ | 計算量 |
|------|------|--------|
| 計算量見積り | 実装前 | — |
| `std::sort` | 前処理 · 貪欲キー | $O(n \log n)$ |
| 値の二分 | ソート済み配列 | $O(\log n)$ |
| 答えの二分 | 可行性単調 | $O(\log V \cdot T_{ok})$ |
| ビット全探索 | $n \le 20$ | $O(2^n)$ |
| 終了時刻順貪欲 | 区間スケジューリング | $O(n \log n)$ |
| Kadane | 最大部分配列和 | $O(n)$ |
