import parser

if __name__ == "__main__":
    form = parser.parse("{{u},{p, ¬y},{y, ¬t, ¬u, ¬q},{¬y, ¬q},{y, p, ¬t, ¬u},{y, q, ¬p},{t},{q, ¬t, ¬y, ¬u, ¬p}}")

    form.dpll(2)
