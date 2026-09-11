---
cpp_doc_id: cpp.topic.cp_stl_ds
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [union-find, priority-queue, containers]
cpp_doc_regex_file: ^cpp-doc-cp-stl\-union\-find\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cp_stl_ds -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# 競技プログラミング — STL コンテナと Union-Find

**出典**: CPH Ch.4 · Ch.15.2

---

## 1. コンテナ選択の原則

**問い**: 何回 · どの操作が必要か？

| 操作 | 第一候補 | 計算量 |
|------|----------|--------|
| 末尾追加 · ランダムアクセス | `vector` | push 償却 $O(1)$ · `[]` $O(1)$ |
| 重複なし · 順序付き | `set` | $O(\log n)$ |
| 重複なし · 順序不要 | `unordered_set` | 平均 $O(1)$ |
| キー→値 · 順序付き | `map` | $O(\log n)$ |
| キー→値 · 順序不要 | `unordered_map` | 平均 $O(1)$ |
| LIFO / FIFO | `stack` / `queue` | $O(1)$ |
| 両端操作 | `deque` | 両端 $O(1)$ |
| 最大/最小の繰り返し取出し | `priority_queue` | $O(\log n)$ |
| ビット集合演算 | `bitset` | ビット演算 |

---

## 2. map の注意

```cpp
map<string, int> m;
cout << m["key"];  // キーが無いと 0 で自動 insert
```

存在確認: `m.count(key)` または `m.find(key) != m.end()`。

---

## 3. priority_queue

```cpp
// 最大ヒープ（デフォルト）
priority_queue<int> max_heap;

// 最小ヒープ
priority_queue<int, vector<int>, greater<int>> min_heap;
```

Dijkstra · 貪欲の「常に最小コスト」で頻出。

---

## 4. set vs unordered_set

| | `set` | `unordered_set` |
|---|-------|-------------------|
| 順序 | あり · `lower_bound` 可 | なし |
| 速度 | $O(\log n)$ | 平均 $O(1)$ |
| 使うとき | 順序 · 次要素 | 存在判定のみ |

同じ $O(n \log n)$ でも **sort + 線形走査** の方が速い場合がある。

---

## 5. Union-Find（素集合データ構造）

### 5.1 操作

| 操作 | 意味 |
|------|------|
| `find(v)` | $v$ の属する集合の代表元（根） |
| `unite(u, v)` | 2 集合を併合 |
| `same(u, v)` | `find(u) == find(v)` |

### 5.2 実装

```cpp
struct UnionFind {
    vector<int> parent, size_;
    UnionFind(int n) : parent(n), size_(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int v) {
        if (parent[v] == v) return v;
        return parent[v] = find(parent[v]);  // path compression
    }
    void unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return;
        if (size_[a] < size_[b]) swap(a, b);  // union by size
        parent[b] = a;
        size_[a] += size_[b];
    }
    bool same(int a, int b) { return find(a) == find(b); }
};
```

### 5.3 計算量

path compression + union by size:

$$O(N + Q \cdot \alpha(N))$$

$\alpha$ は逆アッカーマン関数 — 実用上ほぼ定数。

### 5.4 典型用途

- 無向グラフの動的連結性
- **Kruskal MST**（辺を重さ昇順に見て `unite`）
- グルーピング · 等価類の管理

```text
for (edge (u,v,w) in sorted_edges):
    if not same(u,v):
        unite(u,v)
        add to MST
```

---

## 6. 選択フローチャート

```text
順序付きで lower_bound が要る？
  YES → set / map
  NO  → 存在判定だけ？ → unordered_set / unordered_map
動的連結性？ → Union-Find
最値の繰り返し取出し？ → priority_queue
```

---

## 7. グラフの隣接リスト

```cpp
vector<vector<int>> adj(n);
// 無向: adj[u].push_back(v); adj[v].push_back(u);
// 重み付き: vector<vector<pair<int,int>>> adj(n);  // (to, w)
```

`vector` が競プロの標準表現。
