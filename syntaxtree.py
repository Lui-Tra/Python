import parser

if __name__ == "__main__":
    form = parser.parse("(A and B and C) or (A and B and (not C) and D)")
    print(form.canonical_dnf())
    form.simple_dnf()
    print(form)
