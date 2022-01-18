import parser


if __name__ == "__main__":
    form = parser.parse("(a and b and e) or (c and a and d)").simplify()
    print(form)