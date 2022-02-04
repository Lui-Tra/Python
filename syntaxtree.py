import parser

if __name__ == "__main__":
    form = parser.parse("a and (not a or b)")
    print(form.to_clause_list())

    form.dpll()
