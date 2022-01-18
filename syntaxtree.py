import parser


if __name__ == "__main__":
    formula = parser.parse("c or d and f")
    print(formula)
    formula.to_nand()
    print(formula)
