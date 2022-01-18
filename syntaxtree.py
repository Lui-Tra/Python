import parser

if __name__ == "__main__":
    form = parser.parse("(a and b) or (a and c) or (c and halloFlo)")
    form.simplify()
    print(form)

    form = parser.parse("(a and b and e) or (b and a and d) or (a and f)")
    form.simplify()
    print(form)
    form.simplify()
    print(form)
    form.simplify()
    print(form)
    form.simplify()
    print(form)
    form.simplify()
    print(form)
