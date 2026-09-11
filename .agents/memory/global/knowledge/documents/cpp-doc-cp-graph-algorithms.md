---
cpp_doc_id: cpp.topic.cp_graphs
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [bfs, dfs, dijkstra, mst]
cpp_doc_regex_file: ^cpp-doc-cp-graph\-algorithms\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cp_graphs -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# 競技プログラミング — グラフアルゴリズム

**出典**: CPH Ch.11–13, 15–16

---

## 1. 用語

| 用語 | 意味 |
|------|------|
| $n$ | 頂点数 · $m$ 辺数 |
| 無向/有向 | 辺の向きの有無 |
| 重み付き | 辺にコスト |
| 単純グラフ | 多重辺なし · 自己ループなし |
| 連結（無向） | 任意 2 頂点間にパス |
| 強連結（有向） | 双方向に到達 |
| 木 | $n$ 頂点 · $n-1$ 辺 · 連結 · 閉路なし |
| 二部グラフ | 2 色着色可能 ⟺ 奇数長サイクルなし |
| DAG | 有向 · サイクルなし |

---

## 2. グラフの表現

| 表現 | 計算量 | 用途 |
|------|--------|------|
| **隣接リスト** | $O(n+m)$ | **デフォルト** |
| 隣接行列 | $O(n^2)$ メモリ | $n \lesssim 5000$ · 密グラフ |
| 辺リスト | $O(m)$ 走査 | Kruskal |

```cpp
vector<vector<int>> adj(n);
// 重み付き
vector<vector<pair<int,int>>> adj(n);  // (to, w)
// 無向: 両方向に追加
```

---

## 3. DFS / BFS

### DFS — 深さ優先

```cpp
void dfs(int v, vector<int>& vis, const vector<vector<int>>& adj) {
    vis[v] = 1;
    for (int u : adj[v])
        if (!vis[u]) dfs(u, vis, adj);
}
```

用途: 連結成分 · サイクル検出 · トポソ（3 色）· 二部判定。

### BFS — 幅優先

```cpp
queue<int> q;
q.push(s); dist[s] = 0;
while (!q.empty()) {
    int v = q.front(); q.pop();
    for (int u : adj[v])
        if (dist[u] < 0) { dist[u] = dist[v]+1; q.push(u); }
}
```

**未加重グラフの単一始点最短路** — $O(n+m)$。

### 二部判定

BFS/DFS で 2 色着色。隣接が同色 → 二部でない。

### サイクル検出（無向）

DFS で親以外の訪問済み隣接があればサイクル。

---

## 4. 最短経路の選択

| 条件 | アルゴリズム | 計算量 |
|------|--------------|--------|
| 未加重 · 単一始点 | BFS | $O(n+m)$ |
| 非負重み · 単一始点 | Dijkstra | $O(n+m\log m)$ |
| 負辺 · 負サイクルなし | Bellman-Ford | $O(nm)$ |
| 全点対 · $n$ 小 | Floyd–Warshall | $O(n^3)$ |
| DAG | トポソ + DP | $O(n+m)$ |

```text
非負？ → Dijkstra
負辺？ → Bellman-Ford
全点対 & n 小？ → Floyd–Warshall
DAG？ → トポソ + DP
```

---

## 5. Dijkstra

```cpp
vector<long long> dist(n, LLONG_MAX);
priority_queue<pair<long long,int>,
    vector<pair<long long,int>>, greater<>> pq;
dist[s] = 0; pq.push({0, s});
while (!pq.empty()) {
    auto [d, v] = pq.top(); pq.pop();
    if (d > dist[v]) continue;
    for (auto [u, w] : adj[v])
        if (dist[v] + w < dist[u]) {
            dist[u] = dist[v] + w;
            pq.push({dist[u], u});
        }
}
```

**負辺 1 本でも誤答** — 非負が前提。

---

## 6. Bellman-Ford

```cpp
dist[s] = 0;
for (int i = 0; i < n - 1; ++i)
    for (auto [a,b,w] : edges)
        if (dist[a] < INF) dist[b] = min(dist[b], dist[a] + w);
// n 回目でも緩和 → 負サイクル
```

---

## 7. Floyd–Warshall

```cpp
for (int k = 0; k < n; ++k)
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
```

---

## 8. トポロジカルソート

**DAG** の頂点順序 — 辺 $a \to b$ なら $a$ が $b$ より前。

### Kahn（入次数 BFS）

```cpp
queue<int> q;
for (int v = 0; v < n; ++v) if (indeg[v] == 0) q.push(v);
vector<int> order;
while (!q.empty()) {
    int v = q.front(); q.pop();
    order.push_back(v);
    for (int u : adj[v])
        if (--indeg[u] == 0) q.push(u);
}
// order.size() < n → サイクルあり
```

### DAG 上の DP

トポソ順に `dp[u] = max/min(dp[u], dp[v] + w)` — 最長/最短路。

---

## 9. 最小全域木（MST）

$n-1$ 本の辺で全頂点を連結 · 重み和最小。

### Kruskal

```text
辺を重さ昇順にソート
for (u,v,w) in edges:
    if not uf.same(u,v):
        uf.unite(u,v)
        add (u,v,w) to MST
```

$O(m \log m)$ — Union-Find 使用。

### Prim

`priority_queue` で未接続頂点への最小辺を繰り返し追加 — Dijkstra と類似。

---

## 10. Union-Find との使い分け

| 問題 | 手法 |
|------|------|
| 静的連結成分 | DFS/BFS 1 回 |
| 動的併合（辺を順に追加） | Union-Find |
| MST | Kruskal + UF |

---

## 11. 技法早見表

| 技法 | いつ | 計算量 |
|------|------|--------|
| 隣接リスト | グラフ入力 | $O(n+m)$ |
| DFS/BFS | 連結 · 未加重最短路 | $O(n+m)$ |
| 二部判定 | 2 色着色 | $O(n+m)$ |
| Dijkstra | 非負重み最短路 | $O(n+m\log m)$ |
| Bellman-Ford | 負辺 | $O(nm)$ |
| Floyd–Warshall | 全点対 · $n$ 小 | $O(n^3)$ |
| トポソ | DAG · 依存順 | $O(n+m)$ |
| Kruskal MST | 最小全域木 | $O(m\log m)$ |
