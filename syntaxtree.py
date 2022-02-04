import parser

if __name__ == "__main__":
    form = parser.parse("a or (not a and b)")
    form.canonical_cnf()
    print(form.to_clause_list())

    form.dpll()
