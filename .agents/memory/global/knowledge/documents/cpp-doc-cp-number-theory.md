---
cpp_doc_id: cpp.topic.cp_number_theory
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [modular, gcd, crt]
cpp_doc_regex_file: ^cpp-doc-cp-number\-theory\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cp_number_theory -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# 競技プログラミング — 整数論

**出典**: CPH Ch.21 Number theory

---

## 1. 合同式

$a \equiv b \pmod{m}$ ⟺ $m \mid (a - b)$。

剰余 $a \bmod m$ は $[0, m)$ の代表元。

### 競プロの鉄則

**加算 · 減算 · 乗算 · 累乗** は各ステップで $\bmod m$ してよい。

### 一般に成り立たない操作

| 操作 | 注意 |
|------|------|
| 除法 | **逆元** が必要 |
| 指数の合同置換 | 一般に不可 |
| 階乗の合同置換 | 不可 |

### C++ の `%`

負数の剰余は実装依存（`(-10) % 3 == -1`）。正の代表に直す:

```cpp
long long mod(long long x, long long m) {
    x %= m;
    if (x < 0) x += m;
    return x;
}
```

---

## 2. 素数 · 因数分解

| 操作 | 方法 | 計算量 |
|------|------|--------|
| 素数判定 | $2..\lfloor\sqrt{n}\rfloor$ で試し割り | $O(\sqrt{n})$ |
| 因数分解 | 同上 · 割れたら割り続け | $O(\sqrt{n})$ |
| $[2,n]$ の素数表 | エラトステネス | $O(n \log\log n)$ |

```cpp
vector<bool> sieve(int n) {
    vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i * i <= n; ++i)
        if (is_prime[i])
            for (int j = i * i; j <= n; j += i)
                is_prime[j] = false;
    return is_prime;
}
```

**唯一分解定理**: 正整数は素因数の積として一意（順序除く）。

$\tau(n)$: 約数の個数 · $\phi(n)$: オイラー関数（$1..n$ で $n$ と互いに素な個数）— 因数分解から公式で計算。

---

## 3. Euclid の互除法

```cpp
long long gcd(long long a, long long b) {
    while (b) { a %= b; swap(a, b); }
    return a;
}
```

$\gcd(a,b) = \gcd(b, a \bmod b)$ · **$O(\log \min(a,b))$**。

```cpp
long long lcm(long long a, long long b) { return a / gcd(a, b) * b; }
```

**拡張 Euclid**: $ax + by = \gcd(a,b)$ を満たす $(x,y)$ を求める — 不定方程式 · 逆元計算に使用。

---

## 4. 高速累乗 mod

```cpp
long long modpow(long long x, long long n, long long m) {
    long long res = 1 % m;
    x %= m;
    while (n > 0) {
        if (n & 1) res = res * x % m;
        x = x * x % m;
        n >>= 1;
    }
    return res;
}
```

$x^n \bmod m$ を **$O(\log n)$**。

---

## 5. 逆元

$m$ が素数 · $\gcd(x, m) = 1$ のとき:

$$x^{-1} \equiv x^{m-2} \pmod{m}$$（Fermat の小定理）

一般（Euler）:

$$x^{-1} \equiv x^{\phi(m)-1} \pmod{m}$$

```cpp
long long inv(long long x, long long m) { return modpow(x, m - 2, m); }  // m 素数
```

$\gcd(x, m) \neq 1$ なら逆元は **存在しない**。

### 逆元の一括計算（$1..n \bmod p$、$p$ 素数）

```cpp
vector<long long> inv_table(int n, long long p) {
    vector<long long> inv(n + 1);
    inv[1] = 1;
    for (int i = 2; i <= n; ++i)
        inv[i] = p - (p / i) * inv[p % i] % p;
    return inv;
}
```

---

## 6. 中国剰余定理（CRT）

互いに素な法 $m_1, \ldots, m_k$ の連立:

$$x \equiv a_i \pmod{m_i}$$

解は $\bmod M = m_1 \cdots m_k$ で **一意**。

```cpp
// 2 法の場合
long long crt2(long long a1, long long m1, long long a2, long long m2) {
    // extgcd で m1 * t ≡ (a2 - a1) (mod m2) の t を求め
    // x = a1 + m1 * t
}
```

用途: 大きな数の周期性 · 複合法での計算 · modint の合成。

---

## 7. 組み合わせ mod

$n!$ · 逆元テーブルで:

```cpp
// C(n,k) mod p（p 素数 · n < p）
C = fact[n] * inv_fact[k] % p * inv_fact[n-k] % p;
```

Lucas の定理 · ガウスの補題は $n$ が大きい場合に使用。

---

## 8. 技法早見表

| 技法 | いつ | 計算量 |
|------|------|--------|
| 試し割り | 素数判定 · 因数分解 | $O(\sqrt{n})$ |
| エラトステネス | 素数表 | $O(n \log\log n)$ |
| Euclid gcd | 最大公約数 | $O(\log n)$ |
| 高速累乗 mod | $x^n \bmod m$ | $O(\log n)$ |
| 逆元 mod | $\gcd(x,m)=1$ の除算 | $O(\log m)$ |
| CRT | 互いに素な法の連立 | — |

---

## 9. 定数

競プロで頻出: `const int MOD = 1'000'000'007;`（素数）

途中計算は `long long` でオーバーフローを防ぎ、各ステップで mod する。
