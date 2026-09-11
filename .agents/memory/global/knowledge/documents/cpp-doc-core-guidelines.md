---
cpp_doc_id: cpp.topic.core_guidelines
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [guidelines, design]
cpp_doc_regex_file: ^cpp-doc-core\-guidelines\.md$
---

<!-- CPP_DOC_ID: cpp.topic.core_guidelines -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ Core Guidelines

**出典**: [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — Stroustrup / Sutter

---

## 1. 目的

現代 ISO C++ で **静的型安全** · **リソース安全** · **ロジックエラー低減** を達成しつつ **ゼロオーバーヘッド** を維持するためのルール集。チュートリアルではなく **索引・レビュー・静的解析** 向け。

---

## 2. Philosophy（P セクション）— 13 原則

| ルール | 要約 |
|--------|------|
| **P.1** | 意図をコードに直接表現する |
| **P.2** | ISO Standard C++ を書く |
| **P.3** | 意図を明示（range-for · アルゴリズム） |
| **P.4** | 静的型安全を目指す |
| **P.5** | コンパイル時チェックを優先 |
| **P.6** | コンパイル不可なら実行時チェック |
| **P.7** | 実行時エラーを早期検出 |
| **P.8** | リソースを漏らさない |
| **P.9** | 時間・空間を無駄にしない |
| **P.10** | mutable より immutable |
| **P.11** | 複雑さはインターフェース裏に隠す |
| **P.12–13** | ツール · サポートライブラリを使う |

### P.1 の対比

```cpp
// 悪い: 手書きループで find を再発明
int index = -1;
for (int i = 0; i < v.size(); ++i)
    if (v[i] == val) { index = i; break; }

// 良い
auto it = std::find(v.begin(), v.end(), val);
```

---

## 3. Interfaces（I セクション）

| ルール | 要約 |
|--------|------|
| **I.1** | インターフェースと実装を分離 |
| **I.2** | インターフェースは不変条件を表現 |
| **I.4** | インターフェースは具体的で汎用的 |
| **I.11** | 所有権をポインタで渡さない — `unique_ptr` 等 |
| **I.13** | 配列をポインタで渡さない — `span` / `vector` |

---

## 4. Functions（F セクション）

| ルール | 要約 |
|--------|------|
| **F.16** | in 引数: 小→値 · 大→`const&` |
| **F.20** | out 引数より **戻り値** |
| **F.21** | 複数戻り値は `tuple` / `struct` |
| **F.43** | 戻り値の型は `auto` 禁止（意図の明示） |
| **F.52–53** | ラムダは短く · キャプチャは最小限 |

---

## 5. Resource management（R セクション）

| ルール | 要約 |
|--------|------|
| **R.1** | RAII — スコープでリソース管理 |
| **R.11** | `new`/`delete` を避ける |
| **R.20** | 生ポインタより `unique_ptr` / `vector` |
| **R.21** | `shared_ptr` は本当に共有が必要なとき |
| **R.22** | `make_shared` / `make_unique` を使う |

---

## 6. Expressions and statements（ES セクション）

| ルール | 要約 |
|--------|------|
| **ES.20** | 常にオブジェクトを初期化 |
| **ES.23** | `{}` 初期化 |
| **ES.47** | `NULL` より `nullptr` |
| **ES.48–49** | C スタイルキャスト禁止 · named cast |
| **ES.56** | `std::move` は必要時のみ |
| **ES.71** | range-for を優先 |

---

## 7. Classes（C セクション）

| ルール | 要約 |
|--------|------|
| **C.2** | 不変条件をクラスで表現 |
| **C.20–21** | Rule of Zero / Five |
| **C.35** | 多態の基底は virtual dtor |
| **C.120** | 継承よりコンポジション |
| **C.131** | raw リソースを持つなら Rule of Five |

---

## 8. Standard library（SL セクション）

| ルール | 要約 |
|--------|------|
| **SL.1** | ライブラリを使う |
| **SL.con.1** | C 配列より `array` / `vector` |
| **SL.con.2** | 順序コンテナの既定は `vector` |
| **SL.con.3** | 範囲外アクセス禁止 |

---

## 9. Concurrency（CP セクション）

| ルール | 要約 |
|--------|------|
| **CP.2–3** | 共有データを最小化 |
| **CP.20–21** | `lock_guard` / `scoped_lock` |
| **CP.25** | スレッドは join する（RAII） |
| **CP.26** | `detach` しない |
| **CP.50** | mutex とデータをセットで |
| **CP.60–61** | `async` + `future` でタスク |

---

## 10. Enforcement

各ルールに **Enforcement** 節（レビュー · clang-tidy · コンパイラ · 実行時）。

**Profiles**: `type` · `bounds` · `lifetime` — 静的解析のプリセット。

```cpp
[[gsl::suppress("bounds")]]  // 抑制（理由をコメントで）
```

---

## 11. 実装パターン例

### RAII ファイルハンドル

```cpp
class FileHandle {
public:
    explicit FileHandle(const char* path) : f_{std::fopen(path, "r")} {
        if (!f_) throw std::runtime_error("open failed");
    }
    ~FileHandle() { if (f_) std::fclose(f_); }
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
private:
    std::FILE* f_;
};
```

### ESF（Expressions and statements — 関数インターフェース）

- 入力は `const&` · 出力は戻り値
- `const` をデフォルトに
- 早期 return でネストを浅く
