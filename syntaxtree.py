import parser

if __name__ == "__main__":
    form = parser.parse("(A ↔ (B → C))")
    print(form.canonical_cnf())
    form.simple_cnf()
    print(form)
