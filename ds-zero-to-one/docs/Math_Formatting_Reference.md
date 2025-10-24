# 🧮 Math Formatting Reference (for Jupyter & GitHub Markdown)

This quick guide shows how to write math equations and include dollar signs in Jupyter Notebook Markdown or GitHub README files.  

---

## 1️⃣ Inline Math
Use single dollar signs `$ ... $` for short equations inside sentences.

```markdown
The slope $m = 0.12$ means each \$1 increase in the bill adds \$0.12 to the tip.
```

**Displays as →**  
The slope *m = 0.12* means each $1 increase in the bill adds $0.12 to the tip.

---

## 2️⃣ Display (Centered) Math
Use double dollar signs `$$ ... $$` for large, centered formulas.

```markdown
$$
\text{Adjusted R}^2 = 1 - (1 - R^2)\frac{n - 1}{n - p - 1}
$$
```

**Displays as →**

$$
\text{Adjusted R}^2 = 1 - (1 - R^2)\frac{n - 1}{n - p - 1}
$$

---

## 3️⃣ Escaping the Dollar Sign
If you just want to show a literal dollar sign (not math mode), **escape it** with a backslash `\`.

```markdown
Each meal costs about \$25 on average.
```

**Displays as →**  
Each meal costs about $25 on average.

---

## 4️⃣ Mixing Text and Math
You can mix math and normal text easily:

```markdown
If $R^2 = 0.47$, then the Adjusted $R^2$ may drop slightly after accounting for extra predictors.
```

**Displays as →**  
If *R² = 0.47*, then the Adjusted *R²* may drop slightly after accounting for extra predictors.

---

## 5️⃣ Common LaTeX Symbols

| Symbol | Code | Output |
|:-------|:------|:-------|
| Superscript | `x^2` | x² |
| Subscript | `x_1` | x₁ |
| Greek letters | `\alpha`, `\beta`, `\mu` | α, β, μ |
| Fraction | `\frac{a}{b}` | 𝑎⁄𝑏 |
| Summation | `\sum_{i=1}^{n}` | ∑ᵢ₌₁ⁿ |
| Mean / expected value | `\bar{x}`, `E[X]` | x̄ , E[X] |
| Equation text | `\text{Tip percent}` | Tip percent |

---

## 6️⃣ Example Combo Block

```markdown
### Linear Regression Formula

$$
\text{Tip} = \beta_0 + \beta_1(\text{Bill Total}) + \epsilon
$$

If $\beta_1 = 0.12$, then each \$1 increase in the bill adds about \$0.12 to the tip.
```

**Displays as →**

### Linear Regression Formula

$$
\text{Tip} = \beta_0 + \beta_1(\text{Bill Total}) + \epsilon
$$

If $\beta_1 = 0.12$, then each $1 increase in the bill adds about $0.12 to the tip.

---

## 7️⃣ Notes for GitHub vs. Jupyter

- 🧠 **Jupyter Notebooks** automatically render LaTeX using MathJax (no setup needed).
- 🌐 **GitHub** supports inline `$...$` and block `$$...$$` math, but only in `.ipynb` or `.md` previews (not READMEs inside subfolders yet).
- 📄 If you want perfect rendering everywhere (including PDF exports), use **nbconvert** or **VS Code’s Markdown preview**.

---

✅ **File Info**
- **Filename:** `Math_Formatting_Reference.md`
- **Location:** `ds-zero-to-one/docs/`
- **Purpose:** Quick visual guide for Markdown and math notation during your study sessions.

---
