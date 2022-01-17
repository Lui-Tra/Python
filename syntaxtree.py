import parser


if __name__ == "__main__":
    formula = parser.parse("(A or F or Q) and (B or C or D)")
    print(formula)
    formula.simplify()
    print(formula)
    formula.simplify()
    print(formula)
    formula.simplify()
    print(formula)
