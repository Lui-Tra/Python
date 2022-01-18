import parser


if __name__ == "__main__":
    form = parser.parse("a nand b").to_nand()
    print(form)
    form = parser.parse("a nand a nand b nand b nand b").to_nand()
    print(form)
