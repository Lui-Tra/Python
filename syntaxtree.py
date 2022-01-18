import parser


if __name__ == "__main__":
    formula = parser.parse("(((¬q ∧ ¬t) ∨ (p ∨ t)) ∨ (q ∧ ((¬t ∨ p) ∧ (¬p ∨ t)))) ∨ (((q ∨ t) ∧ (¬p ∧ ¬t)) ∧ (¬q ∨ ((t ∧ ¬p) ∨ (p ∧ ¬t))))")
    # formula = parser.parse("(a and b) or not a")
    print(formula)
    formula.simplify()
    print(formula)
