---
math_doc_id: math.topic.calculus_ode
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [calculus, ode]
math_doc_regex_file: ^math-doc-calculus\-differential\-equations\.md$
---

<!-- MATH_DOC_ID: math.topic.calculus_ode -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# 微積分と常微分方程式

**出典**: [数学（Wikipedia）](https://ja.wikipedia.org/wiki/数学)「解析」「量（微積分 · 微分方程式）」

---

## 1. 関数

**関数** f: A → B は、定義域 A の各要素 a に対し **唯一の** 値 f(a) ∈ B を対応させる写像。

| 概念 | 記号 · 説明 |
|------|-------------|
| 定義域 | dom(f) = A |
| 値域 | { f(a) : a ∈ A } ⊆ B |
| 合成 | (g ∘ f)(x) = g(f(x)) |
| 逆関数 | f⁻¹ が存在 ⇔ f は全単射 |

### 初等関数（ の主対象）

| 種類 | 例 |
|------|-----|
| 多項式 | x² − 3x + 1 |
| 有理関数 | 1/(x+1) |
| 指数·対数 | eˣ , ln x |
| 三角関数 | sin x , cos x , tan x |

---

## 2. 極限

**直観**: x が a に近づくとき、f(x) が L に近づく → lim_{x→a} f(x) = L

**ε-δ 定義**（厳密化 · 後で再訪可）:
∀ε>0, ∃δ>0, 0<|x−a|<δ ⇒ |f(x)−L|<ε

### 基本極限

| 極限 | 値 |
|------|-----|
| lim_{x→0} sin x / x | 1 |
| lim_{x→∞} (1 + 1/x)^x | e |
| lim_{x→0} (eˣ − 1)/x | 1 |

### 連続

f が x=a で **連続** ⇔ lim_{x→a} f(x) = f(a)

---

## 3. 微分

**導関数**: f'(x) = lim_{h→0} [f(x+h) − f(x)] / h

**幾何的意味**: 接線の傾き
**物理的意味**: 変化率（速度 = 位置の時間微分）

### 基本公式

| 関数 | 導関数 |
|------|--------|
| xⁿ | n x^{n−1} |
| eˣ | eˣ |
| ln x | 1/x |
| sin x | cos x |
| cos x | −sin x |

### 合成関数の微分（連鎖律）

(g ∘ f)'(x) = g'(f(x)) · f'(x)

**例**: (sin(x²))' = cos(x²) · 2x

### 積·商の微分

- (fg)' = f'g + fg'
- (f/g)' = (f'g − fg') / g² （g≠0）

---

## 4. 積分

### 不定積分

F'(x) = f(x) なら ∫ f(x) dx = F(x) + C（積分定数）

| 被積分関数 | 原始関数 |
|------------|----------|
| xⁿ (n≠−1) | x^{n+1}/(n+1) |
| 1/x | ln\|x\| |
| eˣ | eˣ |
| cos x | sin x |
| sin x | −cos x |

### 定積分

∫_a^b f(x) dx = **曲線 y=f(x) と x 軸で囲まれた符号付き面積**

### 微積分の基本定理

F' = f なら **∫_a^b f(x) dx = F(b) − F(a)**

→ 微分と積分は **互いの逆操作**（解析学の中核）

---

## 5. 級数（入口）

**テイラー級数**（x=0 周り）:

f(x) = Σ_{n=0}^∞ [f^{(n)}(0) / n!] xⁿ

| 関数 | 級数（|x| 小） |
|------|----------------|
| eˣ | 1 + x + x²/2! + x³/3! + … |
| sin x | x − x³/3! + x⁵/5! − … |
| 1/(1−x) | 1 + x + x² + … （\|x\|<1） |

詳細: analysis.md

---

## 6. 常微分方程式（ODE）

**常微分方程式**: 未知関数 y(x) とその導関数の関係式。

### 6.1 変数分離形

dy/dx = g(x) h(y) → ∫ dy/h(y) = ∫ g(x) dx

**例**: dy/dx = xy
→ dy/y = x dx → ln|y| = x²/2 + C → y = Ce^{x²/2}

### 6.2 1 階線形

y' + p(x)y = q(x)

積分因子 μ(x) = exp(∫ p(x) dx) を用いる。

**例**: y' + y = e^x
→ y = e^{−x}(∫ e^{2x} dx + C) = e^x/2 + Ce^{−x}

### 6.3 数値解法（Euler 法）

y_{n+1} = y_n + h · f(x_n, y_n)

簡単だが精度は低い → で Runge-Kutta 等

---

## 7. 演習

### 7.1 微分

f(x) = x³ − 3x → f'(x) = 3x² − 3
**停留点**: f'(x)=0 → x=±1

### 7.2 定積分

∫_0^1 x² dx = [x³/3]_0^1 = **1/3**

### 7.3 ODE

y' = −y, y(0)=1 → **y = e^{−t}**

---
