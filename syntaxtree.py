import parser


if __name__ == "__main__":
    formula = parser.parse("(((¬q ∧ ¬t) ∨ (p ∨ t)) ∨ (q ∧ ((¬t ∨ p) ∧ (¬p ∨ t)))) ∨ (((q ∨ t) ∧ (¬p ∧ ¬t)) ∧ (¬q ∨ ((t ∧ ¬p) ∨ (p ∧ ¬t))))")
    print(formula)
    formula.simplify()
    print(formula)
