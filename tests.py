import parser

if __name__ == "__main__":
    form = parser.parse("{{A, ¬B, ¬C},{A, B, D},{A, ¬C, ¬D},{¬A, B},{¬A, ¬B}}")

    form.dpll(scale=1)
