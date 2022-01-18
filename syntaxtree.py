import parser


if __name__ == "__main__":
    form = parser.parse("(a and b) or c")
    print(form)
    form.simplify()
    print(form)
    form = parser.parse("(a and b) or (c and a)").simplify()
    print(form)

    form.to_nand()
    print(form)
