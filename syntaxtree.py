import parser


if __name__ == "__main__":
    formula = parser.parse("A and (B or C or D)")
    print(formula)
    formula.simplify()
    formula.simplify()
    formula.simplify()
    print(formula)
