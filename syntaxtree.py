import parser


if __name__ == "__main__":
    formula = parser.parse("a nand b")
    print(formula)
    formula.to_nand()
    print(formula)
    formula.to_nand()
    print(formula)
    formula.to_nand()
    print(formula)
