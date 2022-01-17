import parser


if __name__ == "__main__":
    formula = parser.parse("(A or (A and C) or D) and A")
    print(formula)
    formula.root = formula.root.absorption()
    print(formula)
