import parser


if __name__ == "__main__":
    formula = parser.parse("(A or F) and (B or C or D)")
    print(formula)
    formula.simplify()
    print(formula)
    formula.simplify()
    print(formula)
    formula.simplify()
    print(formula)
