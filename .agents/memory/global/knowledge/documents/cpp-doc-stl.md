---
cpp_doc_id: cpp.topic.stl
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [containers, algorithms, iterators]
cpp_doc_regex_file: ^cpp-doc-stl\.md$
---

<!-- CPP_DOC_ID: cpp.topic.stl -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ 標準ライブラリ（STL）

**出典**: cppreference · C++ Core Guidelines SL セクション · Learn C++ Ch16–18, 28

---

## 1. STL の三要素

| 要素 | 役割 |
|------|------|
| **コンテナ** | データの格納 |
| **イテレータ** | コンテナ要素への汎用アクセス |
| **アルゴリズム** | イテレータ経由の汎用操作 |

**方針**: 手書きより標準ライブラリ（SL.1–2）。順序コンテナの既定は `vector`（SL.con.2）。

---

## 2. シーケンスコンテナ

| 型 | いつ使う | 典型計算量 |
|----|----------|------------|
| **`vector<T>`** | **デフォルト** · ランダムアクセス · 末尾追加 | push_back 償却 O(1) · `[]` O(1) |
| `array<T,N>` | 固定長 · スタック | 全操作 O(1) |
| `deque<T>` | 両端 push/pop | 両端 O(1) |
| `list<T>` | 中間挿入多 · ランダムアクセス不要 | insert O(1) · find O(n) |
| `forward_list<T>` | 単方向リスト | メモリ節約 |

### vector 初期化の注意

```cpp
std::vector<int> v1(20);   // 20 要素、値 0
std::vector<int> v2{20};   // 1 要素、値 20
```

---

## 3. 連想コンテナ

| 型 | 内部 | 順序 | 典型計算量 |
|----|------|------|------------|
| `map<K,V>` | 赤黒木 | あり | O(log n) |
| `set<K>` | 赤黒木 | あり | O(log n) |
| `unordered_map<K,V>` | ハッシュ | なし | 平均 O(1) |
| `unordered_set<K>` | ハッシュ | なし | 平均 O(1) |
| `multimap` / `multiset` | — | — | 重複キー可 |

小規模データでは sorted `vector` + 二分探索が `map` より速いこともある。

---

## 4. コンテナアダプタ

| 型 | 意味 | イテレータ |
|----|------|------------|
| `stack<T>` | LIFO | **なし** |
| `queue<T>` | FIFO | なし |
| `priority_queue<T>` | ヒープ（デフォルト最大） | なし |

```cpp
std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
```

---

## 5. イテレータ

| カテゴリ | 能力 |
|----------|------|
| 入力 | 読み取り · 単方向 `++` |
| 出力 | 書き込み · 単方向 |
| 前方 | 読み/書き · 複数回読める |
| 双方向 | `++` と `--` |
| ランダムアクセス | `+n`, `[]`, `<` |

```cpp
auto it = std::begin(v);
auto it2 = std::end(v);
for (auto it = v.begin(); it != v.end(); ++it) { /* *it */ }
for (auto& x : v) { /* range-for */ }
```

**無効化**: `vector` の再割当 · insert/erase 後はイテレータが無効になることがある。

---

## 6. よく使うアルゴリズム

| アルゴリズム | 用途 | 計算量 |
|--------------|------|--------|
| `std::sort` | ソート | O(n log n) |
| `std::stable_sort` | 安定ソート | O(n log n) |
| `std::find` / `find_if` | 線形探索 | O(n) |
| `std::lower_bound` | ソート済み二分探索 | O(log n) |
| `std::upper_bound` | 上側境界 | O(log n) |
| `std::binary_search` | 存在判定 | O(log n) |
| `std::accumulate` | 畳み込み | O(n) |
| `std::for_each` | 各要素に副作用 | O(n) |
| `std::count_if` | 条件カウント | O(n) |
| `std::min_element` / `max_element` | 最値位置 | O(n) |
| `std::next_permutation` | 辞書順次順列 | O(n) |
| `std::swap` | 交換 | O(1) |

```cpp
std::sort(v.begin(), v.end());
auto it = std::lower_bound(v.begin(), v.end(), key);
if (it != v.end() && *it == key) { /* 見つかった */ }
```

---

## 7. 文字列とビュー

| 型 | 所有 | 用途 |
|----|------|------|
| `std::string` | あり | 既定の文字列 |
| `std::string_view` | なし | 引数 · 部分文字列参照（C++17） |
| `std::wstring` | あり | ワイド文字 |

C 文字列 (`char*`) はレガシー API との境界のみ。

---

## 8. ユーティリティ型

| 型 | 用途 |
|----|------|
| `std::pair<T,U>` | 2 値の組 |
| `std::tuple<...>` | 任意個の値 |
| `std::optional<T>` | 値の有無 |
| `std::variant<Ts...>` | 型の和（C++17） |
| `std::any` | 任意型（C++17） |

```cpp
auto [key, value] = *map.begin();  // structured binding (C++17)
```

---

## 9. その他の重要ヘッダ

| ヘッダ | 用途 |
|--------|------|
| `<chrono>` | 時間 · ベンチマーク |
| `<random>` | 乱数生成 |
| `<bitset>` | 固定長ビット列 |
| `<numeric>` | `iota`, `gcd` (C++17) 等 |
| `<thread>` `<mutex>` `<future>` | 並行（別文書） |

---

## 10. 選択フローチャート

```text
連続メモリ · ランダムアクセス？
  YES → vector（固定長なら array）
連想 · 順序付きキー？
  YES → map / set
  NO  → unordered_map / unordered_set
LIFO / FIFO / ヒープ？
  → stack / queue / priority_queue
```
