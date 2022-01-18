import parser


if __name__ == "__main__":
    form = parser.parse("a and b or c").to_nand()
    print(form)
    form.simplify()
    print(form)
