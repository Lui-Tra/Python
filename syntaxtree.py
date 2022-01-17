import parser


if __name__ == "__main__":
    formula = parser.parse("((q ∨ t) → (p ∨ t)) ∨ (q ∧ (t ↔ p))")
    formula.simplify().nnf()
    print(formula)
