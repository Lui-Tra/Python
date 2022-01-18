import parser


if __name__ == "__main__":
    formula = parser.parse("¬(s ↔ t) ⊕ ((q ↔ t) → ¬s)")
    print(formula)
    formula.simplify()
    print(formula)
    formula.kv()
