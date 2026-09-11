---
cpp_doc_id: cpp.topic.cp_range_queries
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [segment-tree, fenwick, sparse-table]
cpp_doc_regex_file: ^cpp-doc-cp-range\-queries\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cp_range_queries -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# 競技プログラミング — 区間クエリ

**出典**: CPH Ch.9 Range queries

---

## 1. データ構造の選択

| 要件 | 第一候補 | 構築 | クエリ | 更新 |
|------|----------|------|--------|------|
| 静的 · 区間和 | **累積和** | $O(n)$ | $O(1)$ | 不可 |
| 静的 · min/max/gcd | **スパーステーブル** | $O(n\log n)$ | $O(1)$ | 不可 |
| 動的 · 区間和 | **Fenwick (BIT)** | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| 動的 · 一般 | **セグメント木** | $O(n)$ | $O(\log n)$ | $O(\log n)$ |

```text
配列は変わらない？
  YES → 和は累積和 · min/max はスパーステーブル
  NO  → 和は Fenwick · 汎用はセグメント木
```

---

## 2. 累積和

```cpp
vector<long long> pref(n + 1);
for (int i = 0; i < n; ++i) pref[i + 1] = pref[i] + a[i];
// sum[l, r] (0-indexed, inclusive)
long long sum = pref[r + 1] - pref[l];
```

2D: 包含除外 $S(A) - S(B) - S(C) + S(D)$。

---

## 3. スパーステーブル（静的 RMQ）

`table[k][i]` = 区間 $[i, i+2^k)$ の min。

```cpp
int LOG = 20;
vector<vector<int>> st(LOG, vector<int>(n));
for (int i = 0; i < n; ++i) st[0][i] = a[i];
for (int k = 1; (1 << k) <= n; ++k)
    for (int i = 0; i + (1 << k) <= n; ++i)
        st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))]);

int query(int l, int r) {  // [l, r]
    int k = __lg(r - l + 1);
    return min(st[k][l], st[k][r - (1 << k) + 1]);
}
```

- **べき等** 演算（min, max, gcd, and, or）に一般化可
- 静的のみ

---

## 4. Fenwick 木（Binary Indexed Tree）

```cpp
struct Fenwick {
    int n;
    vector<long long> bit;
    Fenwick(int n) : n(n), bit(n + 1) {}
    void add(int i, long long x) {  // 0-indexed
        for (++i; i <= n; i += i & -i) bit[i] += x;
    }
    long long sum(int i) {  // prefix [0, i]
        long long s = 0;
        for (++i; i > 0; i -= i & -i) s += bit[i];
        return s;
    }
    long long range(int l, int r) { return sum(r) - sum(l - 1); }
};
```

- 区間和 + 点更新に最適
- 1-indexed 内部が実装しやすい
- **区間 max** には変形 BIT またはセグ木

---

## 5. セグメント木

```cpp
struct SegTree {
    int n;
    vector<long long> tree;
    SegTree(const vector<long long>& a) {
        n = 1;
        while (n < (int)a.size()) n <<= 1;
        tree.assign(2 * n, 0);
        for (int i = 0; i < (int)a.size(); ++i) tree[n + i] = a[i];
        for (int i = n - 1; i > 0; --i) tree[i] = tree[2*i] + tree[2*i+1];
    }
    void update(int i, long long x) {
        i += n; tree[i] = x;
        for (i /= 2; i; i /= 2) tree[i] = tree[2*i] + tree[2*i+1];
    }
    long long query(int l, int r) {  // [l, r)
        long long res = 0;
        for (l += n, r += n; l < r; l /= 2, r /= 2) {
            if (l & 1) res += tree[l++];
            if (r & 1) res += tree[--r];
        }
        return res;
    }
};
```

- 結合可能な演算（sum · min · max · gcd · xor）に汎用
- **遅延伝播**: 区間更新 + 区間クエリ
- **永続セグ木**: 過去バージョンへのクエリ（発展）

---

## 6. 差分配列

区間 $[a,b]$ に $+x$:

```cpp
diff[a] += x;
diff[b + 1] -= x;
// 前缀和で元配列を復元
```

「区間加算 · 点参照」パターン。

---

## 7. 座標圧縮

値域が大きいが distinct が少ないとき:

```cpp
vector<int> xs = a;
sort(xs.begin(), xs.end());
xs.erase(unique(xs.begin(), xs.end()), xs.end());
auto id = [&](int x) { return lower_bound(xs.begin(), xs.end(), x) - xs.begin(); };
```

Fenwick/セグ木のインデックスに使用。

---

## 8. 技法早見表

| 技法 | いつ | クエリ | 更新 |
|------|------|--------|------|
| 累積和 | 静的区間和 | $O(1)$ | — |
| スパーステーブル | 静的 RMQ | $O(1)$ | — |
| Fenwick | 動的区間和 | $O(\log n)$ | $O(\log n)$ |
| セグメント木 | 動的汎用 | $O(\log n)$ | $O(\log n)$ |
| 差分配列 | 区間加算 | — | 一括 |
