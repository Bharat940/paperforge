# Math & Formula block types showcase
import engrapha_notes as en

# Setup a clean default textbook theme
en.set_theme(en.TEXTBOOK)

en.cover_card(
    title="Mathematical Analysis",
    subtitle="Formulas & Theorem Proofs Showcase",
    author="Bharat Dangi",
    date="July 2026",
)
en.br()

en.section("1. Mathematical Notation")
sum_val = en.formula(r'\sum_{i=1}^{n} i')
en.body(
    "Mathematical symbols can be rendered inline using standard LaTeX syntax. "
    f"For instance, we can refer to a function {en.formula('f(x) = x^2 + 2x + 1')} or "
    f"the sum {sum_val}. "
    "Equations use matplotlib's mathtext parser."
)

en.section("2. Block Equations")
en.body("Large equations can be highlighted using dedicated formula blocks:")

en.formula_block(r"f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}")

en.formula_block(r"\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = e")

en.section("3. Theorems and Proofs")
en.body("For educational notes, theorems and proofs have dedicated styled blocks:")

en.theorem(
    "Fundamental Theorem of Calculus: If f is continuous on [a, b] and F is an "
    "antiderivative of f, then the integral of f from a to b is F(b) - F(a)."
)

en.proof(
    "By partitioning [a, b] into subintervals and applying the Mean Value Theorem to F "
    "on each subinterval, we sum the increments to obtain the total integral."
)

en.build_doc("formulas.pdf")
print("Successfully generated formulas.pdf")
