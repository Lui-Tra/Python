import parser

if __name__ == "__main__":
    form = parser.parse("ITE(z, d, q) xor e and not f")
    form.simple_cnf()
    clause_list = form.to_clause_list()
    print(clause_list)

    form.dpll()
