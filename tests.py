from dpll_tree import create_dpll_tree, display_dpll_tree
import parser

if __name__ == "__main__":
    form = parser.parse("{{u},{p, ¬y},{y, ¬t, ¬u, ¬q},{¬y, ¬q},{y, p, ¬t, ¬u},{y, q, ¬p},{t},{q, ¬t, ¬y, ¬u, ¬p}}")

    form.dpll()
