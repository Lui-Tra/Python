import parser


if __name__ == "__main__":
    formula = parser.parse("A and (A and B)")
    formula.simplify()
    print(formula)
