import parser

if __name__ == "__main__":
    form = parser.parse("{{a,b},{c},{¬d}}")
    print(form)
    print(form.to_clause_list_f())
    print(form.dpll_f())