import parser

if __name__ == "__main__":
    form = parser.parse("{{p, ¬w}, {p, y}, {¬p, ¬r, ¬w, y}, {r}, {¬r, w, ¬y}, {w, y}, {¬w, ¬y}}")

    form.dpll()
